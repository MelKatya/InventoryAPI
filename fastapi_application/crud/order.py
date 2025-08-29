from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from core.config import settings
from core.models import Order


async def create_order(session: AsyncSession, customer_id: int) -> Order:
    order = Order(
        customer_id=customer_id,
        status_id=settings.mappings.statuses.get("new")
    )
    session.add(order)

    await session.commit()
    return order


async def get_order_by_id(session: AsyncSession, order_id: int) -> Order | None:
    stmt = select(Order).filter_by(id=order_id)
    order = await session.scalars(stmt)
    return order.one_or_none()


async def update_order_status(
    session: AsyncSession,
    order: Order,
    new_status: str
) -> Order:
    order.status_id = settings.mappings.statuses.get(new_status)
    await session.commit()
    return order


async def get_all_orders(session: AsyncSession, customer_id: int):
    stmt = select(Order).filter_by(customer_id=customer_id).order_by(Order.id)
    orders = await session.scalars(stmt)
    return orders.all()
