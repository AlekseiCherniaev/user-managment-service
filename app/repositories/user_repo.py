from uuid import UUID

from sqlalchemy import select, Result
from app.config.logger_config import setup_logger as logger
from app.adapters.utils import password_check_complexity, hash_password
from app.domain.entities.user import UserUpdate, UserCreate
from app.domain.models.user import User
from app.repositories.base import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.exceptions import PasswordNotValidException, UserAlreadyExistsException, UserNotFoundException


class UserRepo(BaseRepo):

    async def get_by_id(self, user_id: UUID, session: AsyncSession) -> User | None:
        try:
            statement = select(User).where(User.id == user_id)
            result: Result = await session.execute(statement)
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            logger().error(e)

    async def get_all(self, session: AsyncSession) -> list[User] | None:
        try:
            statement = select(User).order_by(User.username)
            result: Result = await session.execute(statement)
            users = result.scalars().all()
            return list(users)
        except Exception as e:
            logger().error(e)

    async def create(self, user_in: UserCreate, session: AsyncSession) -> User:
        try:
            user = await self.get_by_id(user_in.id, session=session)
            if not user:
                user_data = user_in.model_dump()
                if not password_check_complexity(user_data["password"]):
                    raise PasswordNotValidException
                user_data["password"] = hash_password(user_data["password"])
                user = User(**user_data)
                session.add(user)
                await session.commit()
                return user
            else:
                raise UserAlreadyExistsException
        except Exception as e:
            logger().error(e)

    async def update(self, user_id: UUID, user_update: UserUpdate, session: AsyncSession) -> User:
        try:
            user = await self.get_by_id(user_id, session=session)
            if user:
                for key, value in user_update.model_dump(exclude_unset=True).items():
                    setattr(user, key, value)
                await session.commit()
                return user
            else:
                raise UserNotFoundException
        except Exception as e:
            logger().error(e)

    async def delete(self, user_id: UUID, session: AsyncSession) -> None:
        user = await self.get_by_id(user_id, session=session)
        if user:
            await session.delete(user)
            await session.commit()
        else:
            raise UserNotFoundException
