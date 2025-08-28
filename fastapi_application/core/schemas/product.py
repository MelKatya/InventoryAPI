from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    describe: str
    price_per_unit: int
    stock_quantity: int


class ProductCreate(ProductBase):
    supplier_id: int


class ProductUpdatePartial(ProductBase):
    name: str | None = None
    describe: str | None = None
    price_per_unit: int | None = None
    stock_quantity: int | None = None
