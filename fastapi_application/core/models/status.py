from sqlalchemy.orm import Mapped

from core.models import Base


class Status(Base):
    __tablename__ = "statuses"

    name: Mapped[str]