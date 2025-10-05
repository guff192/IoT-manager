from collections.abc import AsyncGenerator
from typing import Annotated

import jwt
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.exceptions.server import ErrServiceUnavailable
from app.api.exceptions.user import ErrNotEnoughPrivileges, ErrUnauthorized, ErrUserNotFound
from app.core import security
from app.core.config import settings
from app.models import TokenPayload
from app.models import User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


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
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(session: AsyncSessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise ErrUnauthorized(detail="Could not validate credentials")

    user = await session.get(User, token_data.sub)
    if not user:
        raise ErrUserNotFound

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise ErrNotEnoughPrivileges
    return current_user
