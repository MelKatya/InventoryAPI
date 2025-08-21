from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.models import Base
from .mixin_id import IdPKMixin

if TYPE_CHECKING:
    from .users_roles import UserRole


class Role(IdPKMixin, Base):
    name: Mapped[str]

    users_roles: Mapped[list["UserRole"]] = relationship(back_populates="roles")