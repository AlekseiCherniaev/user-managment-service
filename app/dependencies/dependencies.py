from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import or_

from app.adapters.utils import decode_jwt, validate_password, TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from app.config.exceptions import InvalidTokenException, UserNotFoundException, WrongPasswordException, \
    UserBlockedException
from app.config.logger_config import logger
from app.dependencies.db_helper import db_helper
from app.domain.models import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login/",
)

http_bearer = HTTPBearer(auto_error=False)


def get_current_token_payload(
        token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise InvalidTokenException
    return payload


def validate_token_type(
        payload: dict,
        token_type: str,
) -> bool:
    try:
        current_token_type = payload.get(TOKEN_TYPE_FIELD)
        if current_token_type == token_type:
            return True
        raise InvalidTokenException
    except InvalidTokenException as e:
        logger.error(f"Invalid token type: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Exception in validating token type: {str(e)}")


async def get_user_by_token_sub(payload: dict, session: AsyncSession) -> User:
    try:
        username: str | None = payload.get("sub")
        statement = select(User).where(User.username == username)
        result: Result = await session.execute(statement)
        user = result.scalar_one_or_none()
        if user:
            return user
        raise UserNotFoundException
    except UserNotFoundException as e:
        logger.error(f"User not found: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Exception in getting user by token: {str(e)}")


def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(
            payload: dict = Depends(get_current_token_payload),
            session: AsyncSession = Depends(db_helper.session_dependency),
    ) -> User:
        validate_token_type(payload, token_type)
        return await get_user_by_token_sub(payload, session)

    return get_auth_user_from_token


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)

get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)


async def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    try:
        statement = select(User).where(or_(User.username == username, User.email == username,
                                           User.phone_number == username))
        result: Result = await session.execute(statement)
        user = result.scalar_one_or_none()
        if not user:
            raise WrongPasswordException

        if not validate_password(
                password=password,
                hashed_password=user.password,
        ):
            raise WrongPasswordException

        if user.is_blocked:
            raise UserBlockedException

        return user
    except WrongPasswordException as e:
        logger.error(f"Wrong password: {str(e)}")
        raise e
    except UserNotFoundException as e:
        logger.error(f"User not found: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Exception in validating user: {str(e)}")


async def get_current_user_from_token(payload: dict, session: AsyncSession) -> User:
    username = payload.get("sub")
    statement = select(User).where(User.username == username)
    result: Result = await session.execute(statement)
    user = result.scalar_one_or_none()
    return user
