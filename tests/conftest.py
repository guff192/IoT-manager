from typing import AsyncGenerator
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_engine


@pytest_asyncio.fixture(scope="function", autouse=True)
async def session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSession(async_engine) as session:
        yield session
