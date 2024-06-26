from typing import TYPE_CHECKING

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from .user import User


class Group(Base):
    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(String(52), nullable=False)
    created_at: Mapped[str] = mapped_column(nullable=False, default=func.CURRENT_TIMESTAMP(),
                                            server_default=func.CURRENT_TIMESTAMP())

    users: Mapped[list['User']] = relationship(back_populates="groups")
