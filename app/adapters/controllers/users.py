from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db_helper import db_helper
from app.dependencies.dependencies import get_current_token_payload, get_current_auth_user, http_bearer
from app.domain.entities.pagination import PaginationInfo
from app.domain.entities.user import UserCreate, UserUpdate, User, CurrentUser
from app.repositories.user_repo import UserRepo

user_router = APIRouter(
    prefix="/user", tags=["user"], dependencies=[Depends(http_bearer)],
)


@user_router.post("/create/")
async def create(
        user_in: UserCreate,
        session: AsyncSession = Depends(db_helper.session_dependency),
        user_repo: UserRepo = Depends(),
) -> User:
    return await user_repo.create_user(user_in=user_in, session=session)


@user_router.get("/me/")
async def get_current_user(
        payload: dict = Depends(get_current_token_payload),
        user: User = Depends(get_current_auth_user),
        user_repository: UserRepo = Depends(),
) -> CurrentUser:
    return await user_repository.get_current_user(payload=payload, user=user)


@user_router.patch("/me/update/")
async def update_current_user(
        payload: dict = Depends(get_current_token_payload),
        user_update: UserUpdate = Depends(),
        session: AsyncSession = Depends(db_helper.session_dependency),
        user_repository: UserRepo = Depends(),
) -> User:
    return await user_repository.update_current_user(payload=payload, user_update=user_update, session=session)


@user_router.delete("/me/delete/")
async def delete_current_user(
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(db_helper.session_dependency),
        user_repository: UserRepo = Depends(),
) -> None:
    return await user_repository.delete_current_user(payload=payload, session=session)


@user_router.get("/")
async def get(
        user_id: UUID,
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(db_helper.session_dependency),
        user_repo: UserRepo = Depends(),
) -> User:
    return await user_repo.get_user(user_id=user_id, session=session, payload=payload)


@user_router.patch("/")
async def update(
        user_id: UUID,
        user_update: UserUpdate,
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(db_helper.session_dependency),
        user_repo: UserRepo = Depends(),
) -> User:
    return await user_repo.update_user(user_id=user_id, user_update=user_update, payload=payload, session=session)


@user_router.get("/all/")
async def get_all(
        pagination: PaginationInfo = Depends(),
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(db_helper.session_dependency),
        user_repo: UserRepo = Depends(),
) -> list[User]:
    return await user_repo.get_all_users(pagination=pagination, payload=payload, session=session)
