from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from app.core.security import get_password_hash, verify_password
from app.models.persistence.user import UserTable


async def create_user(*, session: AsyncSession, email: str, hashed_password: str, full_name: str | None = None, is_superuser: bool = False) -> UserTable:
    db_obj = UserTable(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        is_superuser=is_superuser,
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def count_users(*, session: AsyncSession) -> int | None:
    statement = select(func.count()).select_from(UserTable)
    result = await session.execute(statement)
    return result.scalar()


async def list_users(
    *, session: AsyncSession, skip: int = 0, limit: int = 100
) -> list[UserTable]:
    statement = select(UserTable).offset(skip).limit(limit)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_user_by_email(*, session: AsyncSession, email: str) -> UserTable | None:
    statement = select(UserTable).where(UserTable.email == email)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def update_user(
    *, session: AsyncSession, db_user: UserTable, update_data: dict
) -> UserTable:
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def authenticate(
    *, session: AsyncSession, email: str, password: str
) -> UserTable | None:
    db_user = await get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
