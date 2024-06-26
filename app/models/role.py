from typing import TYPE_CHECKING
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.models import Base

if TYPE_CHECKING:
    from .user import User


class RoleEnum(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Enum(RoleEnum), unique=True, nullable=False)

    users: Mapped[list['User']] = relationship(back_populates="roles")
