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


async def get_all_products(session: AsyncSession):
    stmt = select(Product).order_by(Product.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_supplier_products(session: AsyncSession, supplier_id: int):
    stmt = select(Product).filter_by(supplier_id=supplier_id).order_by(Product.id)
    result = await session.scalars(stmt)
    return result.all()

