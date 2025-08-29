from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select
from sqlalchemy.orm import selectinload

from core.models import Order, Product, OrderItem
from crud.product import get_product_by_id


async def create_orders_item(
    session: AsyncSession,
    order: Order,
    product: Product,
    quantity: int
):
    rest_product_quantity = product.stock_quantity
    if rest_product_quantity < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Too much quantity. Quantity of product is {rest_product_quantity}"
        )

    product.stock_quantity = rest_product_quantity - quantity

    orders_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        quantity=quantity,
        price_at_moment=product.price_per_unit
    )
    session.add(orders_item)
    await session.commit()

    return orders_item


async def get_all_items(
    session: AsyncSession,
    customer_id: int,
):
    stmt = select(OrderItem).join(OrderItem.orders).filter_by(customer_id=customer_id)
    all_items = await session.scalars(stmt)
    return all_items.all()


async def get_order_id_items(
    session: AsyncSession,
    order_id: int,
):
    stmt = select(OrderItem).filter_by(order_id=order_id).order_by(OrderItem.id)
    all_items =  await session.scalars(stmt)
    return all_items.all()
