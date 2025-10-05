from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import AsyncSessionDep
from app.api.exceptions.user import ErrUserNotFound
from app.core import security
from app.core.config import settings
from app.crud import users as user_crud
from app.models.jwt import Token

router = APIRouter(tags=["login"])


@router.post("/login/access-token")
async def login_access_token(
    session: AsyncSessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await user_crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise ErrUserNotFound
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            str(user.id), expires_delta=access_token_expires
        )
    )
