from uuid import UUID
from sqlalchemy import select, Result
from app.config.logger_config import logger
from app.adapters.utils import password_check_complexity, hash_password, make_statement
from app.dependencies.dependencies import get_current_user_from_token, get_role_from_user
from app.domain.entities.pagination import PaginationInfo
from app.domain.entities.user import UserUpdate, UserCreate, CurrentUser
from app.domain.models import Role, RoleEnum
from app.domain.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import or_
from app.config.exceptions import PasswordNotValidException, UserAlreadyExistsException, UserNotFoundException, \
    InvalidTokenException, PermissionDeniedException


class UserUseCases:

    async def create(self, user_in: UserCreate, session: AsyncSession) -> User:
        try:
            statement = select(User).where(or_(User.username == user_in.username, User.email == user_in.email,
                                               User.phone_number == user_in.phone_number))
            user = (await session.execute(statement)).scalar_one_or_none()
            if user:
                raise UserAlreadyExistsException

            user_data = user_in.model_dump()
            if not password_check_complexity(user_data["password"]):
                raise PasswordNotValidException
            user_data["password"] = hash_password(user_data["password"])

            statement = select(Role).where(Role.name == RoleEnum.USER)
            role = (await session.execute(statement)).scalar_one_or_none()
            user_data["role_id"] = role.id

            user = User(**user_data)
            session.add(user)
            await session.commit()
            return user

        except UserAlreadyExistsException as e:
            logger.error(f"User already exists: {str(e)}")
            raise e
        except PasswordNotValidException as e:
            logger.error(f"Password not valid: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")

    async def get_by_id(self, user_id: UUID, session: AsyncSession) -> User | None:
        try:
            statement = select(User).where(User.id == user_id)
            result: Result = await session.execute(statement)
            user = result.scalar_one_or_none()

            if not user:
                raise UserNotFoundException
            return user

        except UserNotFoundException as e:
            logger.error(f"User not found: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error fetching user by ID {user_id}: {str(e)}")

    async def update(self, user: User, user_update: UserUpdate, session: AsyncSession) -> User:
        if user_update.password:
            if not password_check_complexity(user_update.password):
                raise PasswordNotValidException
            user_data = user_update.model_dump(exclude_unset=True)
            user_data["password"] = hash_password(user_data["password"])
        else:
            user_data = user_update.model_dump(exclude_unset=True)

        for key, value in user_data.items():
            if user_data.get(key):
                setattr(user, key, value)
        await session.commit()
        return user

    async def get_current_user(self, payload: dict, user: User) -> CurrentUser:
        try:
            if user:
                iat = payload.get("iat")
                user_schema = CurrentUser.from_orm(user)
                user_schema.iat = iat
                return user_schema

        except Exception as e:
            logger.error(f"Error getting current user: {str(e)}")

    async def update_current_user(self, payload: dict, user_update: UserUpdate, session: AsyncSession) -> User:
        try:
            user = await get_current_user_from_token(payload=payload, session=session)
            if not user:
                raise UserNotFoundException

            return await self.update(user=user, user_update=user_update, session=session)

        except PasswordNotValidException as e:
            logger.error(f"Password not valid: {str(e)}")
            raise e
        except UserNotFoundException as e:
            logger.error(f"User not found: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error updating current user: {str(e)}")

    async def delete_current_user(self, payload: dict, session: AsyncSession) -> None:
        try:
            user = await get_current_user_from_token(payload=payload, session=session)
            if not user:
                raise UserNotFoundException

            await session.delete(user)
            await session.commit()

        except UserNotFoundException as e:
            logger.error(f"User not found: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error deleting current user: {str(e)}")

    async def current_get_by_id(self, payload: dict, user_id: UUID, session: AsyncSession) -> User | None:
        try:
            current_user = await get_current_user_from_token(payload=payload, session=session)
            if not current_user:
                raise InvalidTokenException

            user = await self.get_by_id(user_id=user_id, session=session)
            if not user:
                raise UserNotFoundException

            role = await get_role_from_user(user=current_user, session=session)

            if role.name is RoleEnum.ADMIN or (
                    role.name is RoleEnum.MODERATOR and current_user.group_id == user.group_id):
                return user
            else:
                raise PermissionDeniedException

        except InvalidTokenException as e:
            logger.error(f"Invalid token: {str(e)}")
            raise e
        except PermissionDeniedException as e:
            logger.error(f"Permission denied: {str(e)}")
            raise e
        except UserNotFoundException as e:
            logger.error(f"User not found: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error fetching current user by ID {user_id}: {str(e)}")

    async def current_update_user(self, payload: dict, user_id: UUID, user_update: UserUpdate,
                                  session: AsyncSession) -> User:
        try:
            current_user = await get_current_user_from_token(payload=payload, session=session)
            if not current_user:
                raise InvalidTokenException

            role = await get_role_from_user(user=current_user, session=session)

            if role.name is RoleEnum.ADMIN:
                user = await self.get_by_id(user_id=user_id, session=session)
                if not user:
                    raise UserNotFoundException

                return await self.update(user=user, user_update=user_update, session=session)

        except InvalidTokenException as e:
            logger.error(f"Invalid token: {str(e)}")
            raise
        except UserNotFoundException as e:
            logger.error(f"User not found: {str(e)}")
            raise e
        except PasswordNotValidException as e:
            logger.error(f"Password not valid: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error updating current user by ID {user_id}: {str(e)}")

    async def get_all(self, pagination: PaginationInfo, payload: dict, session: AsyncSession) -> list[User]:
        try:
            current_user = await get_current_user_from_token(payload=payload, session=session)
            if not current_user:
                raise InvalidTokenException

            role = await get_role_from_user(user=current_user, session=session)

            if role.name in (RoleEnum.ADMIN, RoleEnum.MODERATOR):
                statement = make_statement(pagination)
                result: Result = await session.execute(statement)
                users = result.scalars().all()

                if role.name is RoleEnum.MODERATOR:
                    users = [user for user in users if user.group_id == current_user.group_id]

                return users
            else:
                raise PermissionDeniedException

        except PermissionDeniedException as e:
            logger.error(f"Permission denied: {str(e)}")
            raise e
        except InvalidTokenException as e:
            logger.error(f"Invalid token: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error fetching all users: {str(e)}")
