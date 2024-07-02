from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db_helper import db_helper
from app.use_cases.user_usecases import UserUseCases

user_router = APIRouter(
    prefix="/users", tags=["users"]
)


@user_router.get("/all/")
async def get(user_id: UUID, user_use_cases: UserUseCases = Depends(),
              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await user_use_cases.get_user(user_id, session)
