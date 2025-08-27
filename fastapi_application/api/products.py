from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.validation import validate_roles, validate_access_token
from core.models import db_helper, Product
from core.schemas.product import ProductCreate, ProductBase
from crud import product as prod

router = APIRouter(tags=["Products"])


@router.post("/create")
@validate_roles({"admin", "suppliers"})
async def create_new_product(
    new_product: ProductBase,
    session: AsyncSession = Depends(db_helper.session_getter),
    token: dict = Depends(validate_access_token),
):
    supplier_id = int(token.get("sub"))
    product_create = ProductCreate(
        **new_product.model_dump(),
        supplier_id=supplier_id,
    )
    product = await prod.create_new_product(
        session=session,
        new_product=product_create,
    )
    return product

