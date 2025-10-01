from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.exceptions.server import ErrServiceUnavailable


async def get_async_engine(request: Request) -> AsyncEngine:
    engine = getattr(request.app.state, "db_async_engine", None)
    if engine is None:
        raise ErrServiceUnavailable(detail="Database service is unavailable")
    return engine


async def get_async_db(
    engine: AsyncEngine = Depends(get_async_engine),
) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_db)]
