from typing import TYPE_CHECKING

from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.models import Base

if TYPE_CHECKING:
    from .role import Role
    from .group import Group


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    surname: Mapped[str] = mapped_column(String(128), nullable=False)
    username: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    password: Mapped[bytes] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), )
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    image_path: Mapped[str] = mapped_column(String(128))
    is_blocked: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[str] = mapped_column(nullable=False, default=func.CURRENT_TIMESTAMP(),
                                            server_default=func.CURRENT_TIMESTAMP())
    modified_at: Mapped[str] = mapped_column(nullable=False, default=func.CURRENT_TIMESTAMP(),
                                             server_default=func.CURRENT_TIMESTAMP())
    active: Mapped[bool] = mapped_column(default=True, server_default='True')

    role: Mapped['Role'] = relationship(back_populates="users")
    group: Mapped['Group'] = relationship(back_populates="users")
