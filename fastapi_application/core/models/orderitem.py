from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from .mixin_id import IdPKMixin

if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class OrderItem(IdPKMixin, Base):
    __tablename__ = "orders_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]
    price_at_moment: Mapped[int]

    orders: Mapped["Order"] = relationship(back_populates="orders_items")
    products: Mapped["Product"] = relationship(back_populates="orders_items")