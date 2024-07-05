from fastapi import APIRouter, Depends, Response

from app.adapters.controllers.users import create
from app.dependencies.dependencies import validate_auth_user, get_current_auth_user_for_refresh, http_bearer
from app.domain.entities.token import Token
from app.domain.entities.user import User
from app.repositories.user_repo import UserRepo

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(http_bearer)],
)


@auth_router.post("/login/")
async def login(
        user: User = Depends(validate_auth_user),
        user_repository: UserRepo = Depends(), ) -> Token:
    return await user_repository.login_user(user=user)


@auth_router.post("/refresh-token/", response_model=Token, response_model_exclude_none=True, )
async def auth_refresh_jwt(
        user: User = Depends(get_current_auth_user_for_refresh),
        user_repository: UserRepo = Depends()) -> Token:
    return await user_repository.refresh_jwt(user=user)


@auth_router.post("/signup")
async def signup(
        user: User = Depends(create),
        user_repository: UserRepo = Depends()) -> Token:
    return await user_repository.signup_user(user=user)


@auth_router.get("/logout/")
async def logout(
        response: Response,
        user_repository: UserRepo = Depends()) -> None:
    return await user_repository.logout_user(response=response)
