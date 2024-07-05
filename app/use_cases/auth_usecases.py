from fastapi import Response
from pydantic import EmailStr

from app.adapters.utils import create_access_token, create_refresh_token
from app.config.logger_config import logger
from app.domain.entities.token import Token
from app.domain.models.user import User


class AuthUseCases:
    async def login(self, user: User) -> Token:
        try:
            return Token(access_token=create_access_token(user),
                         refresh_token=create_refresh_token(user),
                         token_type="Bearer",
                         )

        except Exception as e:
            logger.error(f"Error logining in: {str(e)}")

    async def signup(self, user: User) -> Token:
        try:
            return Token(access_token=create_access_token(user),
                         refresh_token=create_refresh_token(user),
                         token_type="Bearer",
                         )

        except Exception as e:
            logger.error(f"Error signing up: {str(e)}")

    async def refresh_jwt(self, user: User) -> Token:
        try:
            access_token = create_access_token(user=user)
            return Token(
                access_token=access_token,
            )

        except Exception as e:
            logger.error(f"Error refreshing JWT: {str(e)}")

    async def logout(self, response: Response) -> None:

        # TODO: Implement logout with adding into Blacklist
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

    async def reset_password(self, email: EmailStr) -> None:
        # # TODO: Implement reset password with publishing message to RabbitMQ
        pass
