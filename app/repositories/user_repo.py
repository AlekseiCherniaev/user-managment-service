from uuid import UUID
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.token import Token
from app.domain.entities.user import UserCreate, UserUpdate, User
from app.repositories.base import BaseRepo
from app.use_cases.auth_usecases import AuthUseCases
from app.use_cases.user_usecases import UserUseCases


class UserRepo(BaseRepo):
    user_use_cases: UserUseCases = UserUseCases()
    auth_use_cases: AuthUseCases = AuthUseCases()

    async def create_user(self, user_in: UserCreate,
                          session: AsyncSession) -> User:
        return await self.user_use_cases.create(user_in, session)

    async def get_all_users(self, session: AsyncSession) -> list[User]:
        return await self.user_use_cases.get_all(session)

    async def get_current_user(self, payload: dict, user: User) -> dict:
        return await self.user_use_cases.get_current_user(payload, user)

    async def update_current_user(self, payload: dict, user_update: UserUpdate, session: AsyncSession) -> User:
        return await self.user_use_cases.update_current_user(payload, user_update, session)

    async def delete_current_user(self, payload: dict, session: AsyncSession) -> None:
        return await self.user_use_cases.delete_current_user(payload, session)

    async def login_user(self, user: User) -> Token:
        return await self.auth_use_cases.login(user)

    async def signup_user(self, user: User) -> Token:
        return await self.auth_use_cases.signup(user)

    async def refresh_jwt(self, user: User) -> Token:
        return await self.auth_use_cases.refresh_jwt(user)

    async def logout_user(self, response: Response) -> None:
        return await self.auth_use_cases.logout(response)

    async def get_user(self, user_id: UUID, payload: dict,
                       session: AsyncSession) -> User | None:
        return await self.user_use_cases.current_get_by_id(user_id=user_id, session=session, payload=payload)

    async def update_user(self, payload: dict, user_update: UserUpdate, user_id: UUID,
                          session: AsyncSession) -> User:
        return await self.user_use_cases.current_update_user(user_id=user_id, session=session, user_update=user_update,
                                                             payload=payload)
