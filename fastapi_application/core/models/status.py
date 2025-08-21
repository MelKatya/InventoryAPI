from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.models import Base

if TYPE_CHECKING:
    from .order import Order


class Status(Base):
    __tablename__ = "statuses"

    name: Mapped[str]

    orders: Mapped[list["Order"]] = relationship(back_populates="statuses")
