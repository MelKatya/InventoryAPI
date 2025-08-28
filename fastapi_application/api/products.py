from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependency.product import product_by_id
from api.validation import validate_roles, validate_access_token
from core.models import db_helper, Product
from core.schemas.product import ProductCreate, ProductBase, ProductUpdatePartial
from crud import product as prod

router = APIRouter(tags=["Products"])


@router.post("/create")
@validate_roles({"admin", "supplier"})
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


@router.get("")
async def get_all_products(
    session: AsyncSession = Depends(db_helper.session_getter),
    token: dict = Depends(validate_access_token),
):
    all_product = await prod.get_all_products(session)
    return all_product


@router.get("/me")
@validate_roles({"admin", "supplier"})
async def get_all_supplier_products(
    session: AsyncSession = Depends(db_helper.session_getter),
    token: dict = Depends(validate_access_token),
):
    supplier_id = int(token.get("sub"))
    all_product = await prod.get_supplier_products(session, supplier_id)
    return all_product


@router.put("/{product_id}")
@validate_roles({"admin", "supplier"})
async def update_product(
    product_update: ProductBase,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
    token: dict = Depends(validate_access_token),
):
    creator_id = product.supplier_id
    supplier_id = int(token.get("sub"))
    roles = token.get("roles")

    if creator_id != supplier_id or "admin" not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to modify the product is denied"
        )

    product_update = ProductCreate(**product_update.model_dump(), supplier_id=creator_id)
    return await prod.update_product(session, product, product_update)


@router.patch("/{product_id}")
@validate_roles({"admin", "supplier"})
async def update_product_partial(
    product_update: ProductUpdatePartial,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
    token: dict = Depends(validate_access_token),
):
    creator_id = product.supplier_id
    supplier_id = int(token.get("sub"))
    roles = token.get("roles")

    if creator_id != supplier_id or "admin" not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to modify the product is denied"
        )

    product_update = ProductCreate(**product_update.model_dump(), supplier_id=creator_id)
    return await prod.update_product(session, product, product_update, partial=True)

@router.delete("/{product_id}")
@validate_roles({"admin", "supplier"})
async def delete_product(
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
    payload: dict = Depends(validate_access_token),
):
    creator_id = product.supplier_id
    check_creator(creator_id, payload, "product")

    return await prod.delete_product(session, product)


