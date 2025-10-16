from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.api.exceptions.user import ErrNotEnoughPrivileges, ErrUserExists
from app.crud import users as user_crud
from app.models.user import (
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
)


class UserService:
    def __init__(self, session: AsyncSession):
        """Injects the database session into the service instance."""
        self.session = session

    async def list_users_service(self, skip: int = 0, limit: int = 100) -> UsersPublic:
        count = await user_crud.count_users(session=self.session)
        if not count:
            return UsersPublic(data=[], count=0)

        users = await user_crud.list_users(session=self.session, skip=skip, limit=limit)

        return UsersPublic(data=users, count=count)

    async def create_user_service(self, user_in: UserCreate) -> UserPublic:
        user = await user_crud.create_user(session=self.session, user_create=user_in)
        return UserPublic.model_validate(user)

    async def read_user_me_service(self, user: User) -> UserPublic:
        user_public = UserPublic.model_validate(user)
        logger.debug(user)
        return user_public

    async def update_user_me_service(self, user: User, user_in: UserUpdate) -> UserPublic:
        if user_in.is_superuser and not user.is_superuser:
            raise ErrNotEnoughPrivileges("You should be superuser to change is_superuser.")

        user = await user_crud.update_user(
            session=self.session, db_user=user, user_in=user_in
        )
        return UserPublic.model_validate(user)

    async def register_user_service(self, user_in: UserRegister) -> UserPublic:
        user = await user_crud.get_user_by_email(
            session=self.session, email=user_in.email
        )
        if user:
            raise ErrUserExists

        user_create = UserCreate.model_validate(user_in)
        user = await user_crud.create_user(
            session=self.session, user_create=user_create
        )
        return UserPublic.model_validate(user)
