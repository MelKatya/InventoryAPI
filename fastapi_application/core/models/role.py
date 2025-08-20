from sqlalchemy.orm import Mapped

from core.models import Base


class Role(Base):
    name: Mapped[str]