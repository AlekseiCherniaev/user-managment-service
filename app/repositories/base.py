import uuid
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User, UserUpdate


class BaseRepo(ABC):
    db: AsyncSession

    @abstractmethod
    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        ...

    @abstractmethod
    def get_all(self) -> list[User]:
        ...

    @abstractmethod
    def create(self, user: User) -> User | None:
        ...

    @abstractmethod
    def update(self, user_id: uuid.UUID, user_update: UserUpdate) -> User:
        ...

    @abstractmethod
    def delete(self, user_id: uuid.UUID):
        ...
