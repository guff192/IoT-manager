from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import async_engine


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_db)]
