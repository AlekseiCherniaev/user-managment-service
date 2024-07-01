from uuid import UUID

from fastapi import Depends
from sqlalchemy import select, Result
from app.config.logger_config import setup_logger as logger
from app.adapters.utils import password_check_complexity, hash_password
from app.dependencies.db_helper import db_helper
from app.domain.entities.user import UserUpdate, UserCreate
from app.domain.models.user import User
from app.repositories.base import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.exceptions import PasswordNotValidException, UserAlreadyExistsException, UserNotFoundException


class UserRepo(BaseRepo):

    def __init__(
            self, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
    ) -> None:
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        try:
            statement = select(User).where(User.id == user_id)
            result: Result = await self.session.execute(statement)
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            logger().error(e)

    async def get_all(self) -> list[User] | None:
        try:
            statement = select(User).order_by(User.username)
            result: Result = await self.session.execute(statement)
            users = result.scalars().all()
            return list(users)
        except Exception as e:
            logger().error(e)

    async def create(self, user_in: UserCreate) -> User:
        try:
            user = await self.get_by_id(user_in.id)
            if not user:
                user_data = user_in.model_dump()
                if not password_check_complexity(user_data["password"]):
                    raise PasswordNotValidException
                user_data["password"] = hash_password(user_data["password"])
                user = User(**user_data)
                self.session.add(user)
                await self.session.commit()
                return user
            else:
                raise UserAlreadyExistsException
        except Exception as e:
            logger().error(e)

    async def update(self, user_id: UUID, user_update: UserUpdate) -> User:
        try:
            user = await self.get_by_id(user_id)
            if user:
                for key, value in user_update.model_dump(exclude_unset=True).items():
                    setattr(user, key, value)
                await self.session.commit()
                return user
            else:
                raise UserNotFoundException
        except Exception as e:
            logger().error(e)

    async def delete(self, user_id: UUID) -> None:
        user = await self.get_by_id(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
        else:
            raise UserNotFoundException
