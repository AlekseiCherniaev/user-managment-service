import uuid
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User, UserUpdate


class BaseRepo(ABC):
    db: AsyncSession

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID, session: AsyncSession) -> User | None:
        ...

    @abstractmethod
    async def get_all(self, session: AsyncSession) -> list[User]:
        ...

    @abstractmethod
    async def create(self, user: User, session: AsyncSession) -> User | None:
        ...

    @abstractmethod
    async def update(self, user_id: uuid.UUID, user_update: UserUpdate, session: AsyncSession) -> User:
        ...

    @abstractmethod
    async def delete(self, user_id: uuid.UUID, session: AsyncSession):
        ...
