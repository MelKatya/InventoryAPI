from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from api.dependency.order import order_by_id
from api.dependency.product import product_by_id
from api.dependency.validation import validate_roles, validate_access_token
from api.utils import check_creator
from core.models import db_helper, Order, Product
from crud import order_item as ord_itm

router = APIRouter(tags=["OrdersItems"])


@router.post("/create")
@validate_roles({"admin", "customer"})
async def create_item(
    quantity: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    payload: dict = Depends(validate_access_token),
    order: Order = Depends(order_by_id),
    product: Product = Depends(product_by_id),
):
    creator_id = order.customer_id
    check_creator(creator_id, payload, "order")

    orders_items = await ord_itm.create_orders_item(
        session=session,
        order=order,
        product=product,
        quantity=quantity,
    )

    return orders_items


