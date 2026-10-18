from collections.abc import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import DATABASE_URL, ECHO_SQL


def create_database_resources() -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    engine = create_async_engine(DATABASE_URL, echo=ECHO_SQL, pool_pre_ping=True)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    return engine, session_maker


async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with request.app.state.session_maker() as session:
        yield session
