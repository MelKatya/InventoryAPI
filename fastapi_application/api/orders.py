from typing import Literal, Annotated

from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from api.dependency.order import order_by_id
from api.dependency.validation import validate_roles, validate_access_token
from api.utils import check_creator
from core.models import db_helper, Order
from crud import order as ord

router = APIRouter(tags=["Orders"])


@router.post("/create")
@validate_roles({"admin", "customer"})
async def create_order(
    session: AsyncSession = Depends(db_helper.session_getter),
    payload: dict = Depends(validate_access_token)
):
    customer_id = int(payload.get("sub"))
    order = await ord.create_order(session=session, customer_id=customer_id)
    return order


@router.get("")
@validate_roles({"admin", "customer"})
async def get_all_orders(
    session: AsyncSession = Depends(db_helper.session_getter),
    payload: dict = Depends(validate_access_token)
):
    return await ord.get_all_orders(session=session, customer_id=int(payload.get("sub")))


@router.patch("/{order_id}/update_status")
@validate_roles({"admin", "customer"})
async def update_status(
    new_status: Annotated[str, Literal["new", "confirmed", "cancelled"]],
    session: AsyncSession = Depends(db_helper.session_getter),
    payload: dict = Depends(validate_access_token),
    order: Order = Depends(order_by_id),
):
    creator_id = order.customer_id
    check_creator(creator_id, payload, "order")
    return await ord.update_order_status(session=session, order=order, new_status=new_status)

