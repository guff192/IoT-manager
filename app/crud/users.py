from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate
from app.models.user import UserPublic, UserUpdate


async def create_user(*, session: AsyncSession, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def count_users(*, session: AsyncSession) -> int | None:
    statement = select(func.count()).select_from(User)
    result = await session.execute(statement)
    return result.scalar()


async def list_users(
    *, session: AsyncSession, skip: int = 0, limit: int = 100
) -> list[UserPublic]:
    statement = select(User).offset(skip).limit(limit)
    result = await session.execute(statement)
    return [UserPublic.model_validate(user) for user in result.scalars().all()]


async def get_user_by_email(*, session: AsyncSession, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def update_user(
    *, session: AsyncSession, db_user: User, user_in: UserUpdate
) -> User:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password

    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def authenticate(
    *, session: AsyncSession, email: str, password: str
) -> User | None:
    db_user = await get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
