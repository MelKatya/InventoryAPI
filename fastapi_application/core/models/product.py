from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from .user import User
    from .orderitem import OrderItem


class Product(Base):
    name: Mapped[str]
    describe: Mapped[str | None] = mapped_column(nullable=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    price_per_unit: Mapped[int]
    stock_quantity: Mapped[int]

    users: Mapped["User"] = relationship(back_populates="products")
    orders_items: Mapped[list["OrderItem"]] = relationship(back_populates="products")