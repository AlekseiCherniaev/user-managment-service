import uuid
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User, UserUpdate, UserCreate


class BaseRepo(ABC):

    @abstractmethod
    async def create_user(self, user: UserCreate, session: AsyncSession) -> User:
        ...

    @abstractmethod
    async def get_user(self, user_id: uuid.UUID, session: AsyncSession) -> User | None:
        ...

    @abstractmethod
    async def get_all_users(self, session: AsyncSession) -> list[User]:
        ...

    @abstractmethod
    async def update_user(self, user_id: uuid.UUID, user_update: UserUpdate, session: AsyncSession) -> User:
        ...

    @abstractmethod
    async def delete_user(self, user_id: uuid.UUID, session: AsyncSession) -> None:
        ...
