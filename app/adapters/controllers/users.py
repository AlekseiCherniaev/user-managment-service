from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db_helper import db_helper
from app.domain.entities.user import UserCreate, UserUpdate
from app.repositories.user_repo import UserRepo

user_router = APIRouter(
    prefix="/users", tags=["users"]
)


@user_router.get("/")
async def get(user_id: UUID, user_use_cases: UserRepo = Depends(),
              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await user_use_cases.get_user(user_id, session)


@user_router.get("/all/")
async def get_all(user_use_cases: UserRepo = Depends(),
                  session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await user_use_cases.get_all_users(session)


@user_router.post("/create/")
async def create(user_in: UserCreate, user_use_cases: UserRepo = Depends(),
                 session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await user_use_cases.create_user(user_in, session)


@user_router.patch("/update/")
async def update(user: UserUpdate, user_id: UUID, user_use_cases: UserRepo = Depends(),
                 session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await user_use_cases.update_user(user_id, user, session)


@user_router.delete("/delete/")
async def delete(user_id: UUID, user_use_cases: UserRepo = Depends(),
                 session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await user_use_cases.delete_user(user_id, session)
