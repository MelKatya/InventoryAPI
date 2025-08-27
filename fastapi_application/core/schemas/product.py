from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    describe: str
    price_per_unit: int
    stock_quantity: int


class ProductCreate(ProductBase):
    supplier_id: int

