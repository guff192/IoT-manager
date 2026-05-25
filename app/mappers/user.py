import uuid
from app.models.persistence.user import UserTable
from app.models.domain.user import User
from app.schemas.user import UserPublic, UserCreate


def to_domain(user_table: UserTable) -> User:
    return User(
        id=user_table.id,
        email=user_table.email,
        is_superuser=user_table.is_superuser,
        full_name=user_table.full_name,
    )


def to_persistence(user_domain: User, user_table: UserTable | None = None) -> UserTable:
    if user_table is None:
        return UserTable(
            id=user_domain.id,
            email=user_domain.email,
            is_superuser=user_domain.is_superuser,
            full_name=user_domain.full_name,
            hashed_password="",  # Password should be handled by the service/security layer
        )
    
    user_table.email = user_domain.email
    user_table.is_superuser = user_domain.is_superuser
    user_table.full_name = user_domain.full_name
    return user_table


def to_public(user_domain: User) -> UserPublic:
    return UserPublic(
        id=user_domain.id,
        email=user_domain.email,
        is_superuser=user_domain.is_superuser,
        full_name=user_domain.full_name,
    )


def to_domain_from_create(user_create: UserCreate) -> User:
    # Note: id is usually generated in persistence or service. 
    # Using a placeholder UUID as User domain model requires it.
    return User(
        id=uuid.uuid4(),
        email=user_create.email,
        is_superuser=user_create.is_superuser,
        full_name=user_create.full_name,
    )
