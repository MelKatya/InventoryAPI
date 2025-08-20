from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from .role import Role


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    id_role: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    roles: Mapped["Role"] = relationship(back_populates="users")