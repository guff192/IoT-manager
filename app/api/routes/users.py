from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.deps import AsyncSessionDep, CurrentUser, get_current_active_superuser
from app.api.exceptions.user import ErrUserExists
from app.crud import users as user_crud
from app.models import UserCreate, UserPublic, UserRegister, UsersPublic, UserUpdate
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


async def user_service_dependency(session: AsyncSessionDep) -> UserService:
    """Dependency that creates and provides a UserService instance, injecting the DB session."""
    return UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(user_service_dependency)]


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
async def list_users(
    user_service: UserServiceDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve users. Requires superuser privileges.
    """

    users = await user_service.list_users_service(skip, limit)
    return users


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user_service: UserServiceDep, user_in: UserCreate) -> Any:
    """
    Create new user. Requires superuser privileges.
    """
    user = await user_service.create_user_service(user_in=user_in)
    return user


@router.get("/me/", response_model=UserPublic)
async def read_user_me(user_service: UserServiceDep, user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return await user_service.read_user_me_service(user)


@router.patch("/me/", response_model=UserPublic)
async def update_user_me(
    user_service: UserServiceDep, user: CurrentUser, user_update: UserUpdate
) -> Any:
    """
    Update own user.
    """
    return await user_service.update_user_me_service(user=user, user_in=user_update)


@router.post("/signup", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(user_service: UserServiceDep, user_in: UserRegister) -> Any:
    """
    Create new user with credentials.
    """
    user = await user_service.register_user_service(user_in=user_in)
    return user
