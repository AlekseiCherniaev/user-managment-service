from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.user import UserCreate, UserUpdate
from app.domain.models import User
from app.repositories.user_repo import UserRepo


class UserUseCases:
    user_repository: UserRepo = UserRepo()

    async def create_user(self, user_in: UserCreate,
                          session: AsyncSession) -> User:
        return await self.user_repository.create(user_in, session)

    async def get_user(self, user_id: UUID,
                       session: AsyncSession) -> User:
        return await self.user_repository.get_by_id(user_id, session)

    async def get_all_users(self, session: AsyncSession) -> list[User]:
        return await self.user_repository.get_all(session)

    async def update_user(self, user_id: UUID, user: UserUpdate,
                          session: AsyncSession) -> User:
        return await self.user_repository.update(user_id, user, session)

    async def delete_user(self, user_id: UUID,
                          session: AsyncSession) -> None:
        return await self.user_repository.delete(user_id, session)
