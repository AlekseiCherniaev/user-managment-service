from uuid import UUID
from fastapi import Response
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.pagination import PaginationInfo
from app.domain.entities.token import Token
from app.domain.entities.user import UserCreate, UserUpdate, User, CurrentUser
from app.repositories.base import BaseRepo
from app.use_cases.auth_usecases import AuthUseCases
from app.use_cases.user_usecases import UserUseCases


class UserRepo(BaseRepo):
    user_use_cases: UserUseCases = UserUseCases()
    auth_use_cases: AuthUseCases = AuthUseCases()

    async def create_user(self, user_in: UserCreate,
                          session: AsyncSession) -> User:
        return await self.user_use_cases.create(user_in=user_in, session=session)

    async def get_current_user(self, payload: dict, user: User) -> CurrentUser:
        return await self.user_use_cases.get_current_user(payload=payload, user=user)

    async def update_current_user(self, payload: dict, user_update: UserUpdate, session: AsyncSession) -> User:
        return await self.user_use_cases.update_current_user(payload=payload, user_update=user_update, session=session)

    async def delete_current_user(self, payload: dict, session: AsyncSession) -> None:
        return await self.user_use_cases.delete_current_user(payload=payload, session=session)

    async def login_user(self, user: User) -> Token:
        return await self.auth_use_cases.login(user=user)

    async def signup_user(self, user: User) -> Token:
        return await self.auth_use_cases.signup(user=user)

    async def refresh_jwt(self, user: User) -> Token:
        return await self.auth_use_cases.refresh_jwt(user=user)

    async def logout_user(self, response: Response) -> None:
        return await self.auth_use_cases.logout(response=response)

    async def reset_password(self, email: EmailStr) -> None:
        return await self.auth_use_cases.reset_password(email=email)

    async def get_user(self, user_id: UUID, payload: dict,
                       session: AsyncSession) -> User | None:
        return await self.user_use_cases.current_get_by_id(user_id=user_id, session=session, payload=payload)

    async def update_user(self, payload: dict, user_update: UserUpdate, user_id: UUID,
                          session: AsyncSession) -> User:
        return await self.user_use_cases.current_update_user(user_id=user_id, session=session, user_update=user_update,
                                                             payload=payload)

    async def get_all_users(self, pagination: PaginationInfo, payload: dict, session: AsyncSession) -> list[User]:
        return await self.user_use_cases.get_all(pagination=pagination, payload=payload, session=session)
