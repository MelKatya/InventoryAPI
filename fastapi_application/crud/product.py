from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from core.schemas.product import ProductCreate


async def create_new_product(
    session: AsyncSession,
    new_product: ProductCreate,
):
    product = Product(**new_product.model_dump())
    session.add(product)
    await session.commit()
    return product


