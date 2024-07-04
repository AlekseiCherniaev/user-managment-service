from fastapi import Response

from app.adapters.utils import create_access_token, create_refresh_token
from app.config.exceptions import UserNotFoundException, WrongPasswordException
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
        except UserNotFoundException as e:
            logger.error(f"User not found: {str(e)}")
            raise e
        except WrongPasswordException as e:
            logger.error(f"Wrong password: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error logging in user: {str(e)}")

    async def refresh_jwt(self, user: User) -> Token:
        try:
            access_token = create_access_token(user)
            return Token(
                access_token=access_token,
            )
        except Exception as e:
            logger.error(f"Error refreshing JWT: {str(e)}")

    async def signup(self, user: User) -> Token:
        try:
            return Token(access_token=create_access_token(user),
                         refresh_token=create_refresh_token(user),
                         token_type="Bearer",
                         )
        except UserNotFoundException as e:
            logger.error(f"User not found: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error signing up: {str(e)}")

    async def logout(self, response: Response) -> None:

        # TODO: Implement logout with adding into Blacklist
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
