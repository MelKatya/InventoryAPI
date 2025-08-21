from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from .mixin_id import IdPKMixin

if TYPE_CHECKING:
    from .product import Product
    from .order import Order
    from .users_roles import UserRole


class User(IdPKMixin, Base):
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    products: Mapped[list["Product"]] = relationship(back_populates="users")
    orders: Mapped[list["Order"]] = relationship(back_populates="users")
    users_roles: Mapped[list["UserRole"]] = relationship(back_populates="users")