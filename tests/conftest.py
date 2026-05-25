from typing import AsyncGenerator
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import settings


@pytest_asyncio.fixture(scope="function", autouse=True)
async def session() -> AsyncGenerator[AsyncSession]:
    test_engine = create_async_engine(
        "postgresql+asyncpg://user:password@localhost:5432/db"
    )
    async with AsyncSession(test_engine) as session:
        yield session
