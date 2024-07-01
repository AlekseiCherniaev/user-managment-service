from sqlalchemy import select, Result

from app.adapters.utils import password_check_complexity, hash_password
from app.domain.entities.user import UserUpdate
from app.domain.models.user import User
from app.repositories.base import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.exceptions import PasswordNotValidException, UserAlreadyExistsException, UserNotFoundException


class UserRepo(BaseRepo):
    async def get_by_id(self, session: AsyncSession, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        result: Result = await session.execute(statement)
        user = result.scalar_one_or_none()
        return user

    async def create(self, session: AsyncSession, user: User) -> User:
        user = await self.get_by_id(session, user.id)
        if not user:
            user_data = user.model_dump()
            if not password_check_complexity(user_data["password"]):
                raise PasswordNotValidException
            user_data["password"] = hash_password(user_data["password"])
            user = User(**user_data)
            session.add(user)
            await session.commit()
            return user
        else:
            raise UserAlreadyExistsException

    async def list(self, session: AsyncSession) -> list[User] | None:
        statement = select(User).order_by(User.id)
        result: Result = await session.execute(statement)
        users = result.scalars().all()
        return list(users)

    async def update(self, session: AsyncSession, user_id: int, user_update: UserUpdate) -> User:
        statement = select(User).where(User.id == user_id)
        result: Result = await session.execute(statement)
        user = result.scalar_one_or_none()
        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        await session.commit()
        return user

    async def delete(self, session: AsyncSession, user_id):
        user = await self.get_by_id(session, user_id)
        if user:
            await session.delete(user)
            await session.commit()
        else:
            raise UserNotFoundException
