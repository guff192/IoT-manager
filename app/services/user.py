from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.api.exceptions.user import ErrNotEnoughPrivileges, ErrUserExists
from app.crud import users as user_crud
from app.models.domain.user import User
from app.schemas.user import (
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
)
from app.mappers.user import to_domain, to_public, to_domain_from_create
from app.core.security import get_password_hash


class UserService:
    def __init__(self, session: AsyncSession):
        """Injects the database session into the service instance."""
        self.session = session

    async def list_users_service(self, skip: int = 0, limit: int = 100) -> UsersPublic:
        count = await user_crud.count_users(session=self.session)
        if not count:
            return UsersPublic(data=[], count=0)

        user_tables = await user_crud.list_users(session=self.session, skip=skip, limit=limit)
        
        # Map Persistence -> Domain -> Schema
        users_public = [to_public(to_domain(ut)) for ut in user_tables]

        return UsersPublic(data=users_public, count=count)

    async def create_user_service(self, user_in: UserCreate) -> UserPublic:
        hashed_password = get_password_hash(user_in.password)
        user_table = await user_crud.create_user(
            session=self.session,
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
            is_superuser=user_in.is_superuser,
        )
        return to_public(to_domain(user_table))

    async def read_user_me_service(self, user: User) -> UserPublic:
        logger.debug(f"Reading user: {user.email}")
        return to_public(user)

    async def update_user_me_service(self, user: User, user_in: UserUpdate) -> UserPublic:
        if user_in.is_superuser is True and not user.is_superuser:
            raise ErrNotEnoughPrivileges("You should be superuser to change is_superuser.")

        # Prepare update data
        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data:
            password = update_data.pop("password")
            update_data["hashed_password"] = get_password_hash(password)

        # We need the persistence model to update
        user_table = await user_crud.get_user_by_email(session=self.session, email=user.email)
        if not user_table:
            # This shouldn't happen if the domain user exists
            raise Exception("User not found in database during update")

        updated_table = await user_crud.update_user(
            session=self.session, 
            db_user=user_table, 
            update_data=update_data
        )
        return to_public(to_domain(updated_table))

    async def register_user_service(self, user_in: UserRegister) -> UserPublic:
        user_table = await user_crud.get_user_by_email(
            session=self.session, email=user_in.email
        )
        if user_table:
            raise ErrUserExists

        hashed_password = get_password_hash(user_in.password)
        user_table = await user_crud.create_user(
            session=self.session,
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
            is_superuser=False,
        )
        return to_public(to_domain(user_table))
