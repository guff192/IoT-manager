from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import AsyncSessionDep
from app.models import Token
from app.services.auth import AuthService

router = APIRouter(tags=["login"])


async def auth_service_dependency(session: AsyncSessionDep) -> AuthService:
    """Dependency that creates and provides an AuthService instance, injecting the DB session."""
    return AuthService(session=session)


AuthServiceDep = Annotated[AuthService, Depends(auth_service_dependency)]


@router.post("/login/access-token")
async def login_access_token(
    auth_service: AuthServiceDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    token = await auth_service.authenticate_with_email(
        email=form_data.username, password=form_data.password
    )
    return token
