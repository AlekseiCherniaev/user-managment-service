

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.user import UserCreate, UserUpdate
from app.domain.models import User
from app.repositories.base import BaseRepo
from app.use_cases.user_usecases import UserUserCases


class UserRepo(BaseRepo):
    user_user_cases: UserUserCases = UserUserCases()

    async def create_user(self, user_in: UserCreate,
                          session: AsyncSession) -> User:
        return await self.user_user_cases.create(user_in, session)

    async def get_user(self, user_id: UUID,
                       session: AsyncSession) -> User | None:
        return await self.user_user_cases.get_by_id(user_id, session)

    async def get_all_users(self, session: AsyncSession) -> list[User]:
        return await self.user_user_cases.get_all(session)

    async def update_user(self, user_id: UUID, user: UserUpdate,
                          session: AsyncSession) -> User:
        return await self.user_user_cases.update(user_id, user, session)

    async def delete_user(self, user_id: UUID,
                          session: AsyncSession) -> None:
        return await self.user_user_cases.delete(user_id, session)
