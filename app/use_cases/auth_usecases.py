from app.adapters.utils import create_access_token, user_to_dict, create_refresh_token
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

    async def current_user(self, payload: dict, user: User) -> dict:
        try:
            if user:
                iat = payload.get("iat")
                user_dict = user_to_dict(user)
                user_dict["iat"] = iat
                return user_dict

        except UserNotFoundException as e:
            logger.error(f"User not found: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error getting current user: {str(e)}")

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
