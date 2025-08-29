from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio.session import AsyncSession

from core.models import Order, Product, OrderItem


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
