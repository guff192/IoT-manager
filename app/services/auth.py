from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.user import ErrUnauthorized, ErrUserNotFound
from app.core import security
from app.core.config import settings
from app.crud import users as user_crud
from app.models import Token
from app.models.user import User


class AuthService:
    def __init__(self, session: AsyncSession):
        """Injects the database session into the service instance."""
        self.session = session

    def _generate_user_token(self, user: User) -> Token:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=security.create_access_token(
                str(user.id), expires_delta=access_token_expires
            )
        )

    async def authenticate_with_email(self, email: str, password: str) -> Token:
        user = await user_crud.get_user_by_email(session=self.session, email=email)
        if not user:
            raise ErrUserNotFound
        if not security.verify_password(password, user.hashed_password):
            raise ErrUnauthorized(detail="Wrong credentials!")

        return self._generate_user_token(user)
