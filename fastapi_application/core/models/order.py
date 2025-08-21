from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from .mixin_id import IdPKMixin

if TYPE_CHECKING:
    from .user import User
    from .status import Status
    from .orderitem import OrderItem


class Order(IdPKMixin, Base):
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(),
        server_default=func.now(),
    )
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"))

    statuses: Mapped["Status"] = relationship(back_populates="orders")
    users: Mapped["User"] = relationship(back_populates="orders")
    orders_items: Mapped[list["OrderItem"]] = relationship(back_populates="orders")
