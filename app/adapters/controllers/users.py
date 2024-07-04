from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db_helper import db_helper
from app.dependencies.dependencies import get_current_token_payload, get_current_auth_user, http_bearer
from app.domain.entities.user import UserCreate, UserUpdate, User
from app.repositories.user_repo import UserRepo

user_router = APIRouter(
    prefix="/users", tags=["users"]
)


@user_router.get("/")
async def get(user_id: UUID, user_repo: UserRepo = Depends(),
              session: AsyncSession = Depends(db_helper.session_dependency)) -> User:
    return await user_repo.get_user(user_id, session)


@user_router.get("/all/")
async def get_all(user_repo: UserRepo = Depends(),
                  session: AsyncSession = Depends(db_helper.session_dependency)) -> list[User]:
    return await user_repo.get_all_users(session)


@user_router.post("/create/")
async def create(user_in: UserCreate, user_repo: UserRepo = Depends(),
                 session: AsyncSession = Depends(db_helper.session_dependency)) -> User:
    return await user_repo.create_user(user_in, session)


@user_router.patch("/update/")
async def update(user: UserUpdate, user_id: UUID, user_repo: UserRepo = Depends(),
                 session: AsyncSession = Depends(db_helper.session_dependency)) -> User:
    return await user_repo.update_user(user_id, user, session)


@user_router.delete("/delete/")
async def delete(user_id: UUID, user_repo: UserRepo = Depends(),
                 session: AsyncSession = Depends(db_helper.session_dependency)) -> None:
    return await user_repo.delete_user(user_id, session)


@user_router.get("/me/", dependencies=[Depends(http_bearer)])
async def get_current_user(payload: dict = Depends(get_current_token_payload),
                           user: User = Depends(get_current_auth_user),
                           user_repository: UserRepo = Depends()) -> dict:
    return await user_repository.get_current_user(payload, user)


@user_router.patch("/me/update/", dependencies=[Depends(http_bearer)])
async def update_current_user(payload: dict = Depends(get_current_token_payload),
                              user_repository: UserRepo = Depends(), user_update: UserUpdate = Depends(),
                              session: AsyncSession = Depends(db_helper.session_dependency)) -> User:
    return await user_repository.update_current_user(payload, user_update, session)


@user_router.delete("/me/delete/", dependencies=[Depends(http_bearer)])
async def delete_current_user(payload: dict = Depends(get_current_token_payload),
                              user_repository: UserRepo = Depends(),
                              session: AsyncSession = Depends(db_helper.session_dependency)) -> None:
    return await user_repository.delete_current_user(payload, session)
