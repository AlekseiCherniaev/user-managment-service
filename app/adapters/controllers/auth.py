from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app.adapters.controllers.users import create
from app.dependencies.dependencies import validate_auth_user, get_current_auth_user_for_refresh, \
    get_current_token_payload, get_current_auth_user
from app.domain.entities.token import Token
from app.domain.entities.user import User
from app.repositories.user_repo import UserRepo

http_bearer = HTTPBearer(auto_error=False)

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(http_bearer)],
)


@auth_router.post("/login/")
async def login(user: User = Depends(validate_auth_user), user_repository: UserRepo = Depends(), ) -> Token:
    return await user_repository.login_user(user)


@auth_router.post("/refresh/", response_model=Token, response_model_exclude_none=True, )
async def auth_refresh_jwt(user: User = Depends(get_current_auth_user_for_refresh),
                           user_repository: UserRepo = Depends()):
    return await user_repository.refresh_jwt(user)


@auth_router.get("/me/")
async def current_user(payload: dict = Depends(get_current_token_payload), user: User = Depends(get_current_auth_user),
                       user_repository: UserRepo = Depends()) -> dict:
    return await user_repository.current_user(payload, user)


@auth_router.post("/signup")
async def signup(user: User = Depends(create), user_repository: UserRepo = Depends()) -> Token:
    return await user_repository.signup_user(user)
