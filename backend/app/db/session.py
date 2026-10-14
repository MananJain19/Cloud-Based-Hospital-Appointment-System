
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.core.config import settings

_is_sqlite = settings.database_url.startswith("sqlite")

engine_options = {
    "pool_pre_ping": True,
    "poolclass": NullPool,
}

if not _is_sqlite:
    engine_options["connect_args"] = {
        "statement_cache_size": 0,
    }

engine = create_async_engine(
    settings.database_url,
    **engine_options,
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session
