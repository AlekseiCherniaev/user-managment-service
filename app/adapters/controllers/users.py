from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db_helper import db_helper
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
