from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from app.config.config import settings


class DBHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False, expire_on_commit=False
        )

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session


db_helper = DBHelper(url=settings.get_db_url(), echo=settings.db_echo)
