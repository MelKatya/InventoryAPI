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



