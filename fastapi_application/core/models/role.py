from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.models import Base

if TYPE_CHECKING:
    from .user import User


class Role(Base):
    name: Mapped[str]

    users: Mapped[list["User"]] = relationship(back_populates="roles")