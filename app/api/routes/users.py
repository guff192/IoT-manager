from typing import Any
from fastapi import APIRouter, Depends, status

from app.api.deps import AsyncSessionDep, CurrentUser, get_current_active_superuser
from app.api.exceptions.user import ErrUserExists
from app.crud import users as user_crud
from app.models import UserCreate, UserPublic, UserRegister
from app.models.user import UserUpdate, UsersPublic

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
async def list_users(session: AsyncSessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users. Requires superuser privileges.
    """

    count = await user_crud.count_users(session=session)
    if not count:
        return UsersPublic(data=[], count=0)

    users = await user_crud.list_users(session=session, skip=skip, limit=limit)

    return UsersPublic(data=users, count=count)


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(session: AsyncSessionDep, user_in: UserCreate) -> Any:
    """
    Create new user. Requires superuser privileges.
    """
    user = await user_crud.create_user(session=session, user_create=user_in)
    return user


@router.get("/me/", response_model=UserPublic)
async def read_user_me(user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return user


@router.patch("/me/", response_model=UserPublic)
async def update_user_me(
    session: AsyncSessionDep, user: CurrentUser, user_update: UserUpdate
) -> Any:
    """
    Update own user.
    """
    return await user_crud.update_user(
        session=session, db_user=user, user_in=user_update
    )


@router.post("/signup", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(session: AsyncSessionDep, user_in: UserRegister) -> Any:
    """
    Create new user with credentials.
    """
    user = await user_crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise ErrUserExists

    user_create = UserCreate.model_validate(user_in)
    user = await user_crud.create_user(session=session, user_create=user_create)
    return user
