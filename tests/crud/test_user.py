import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserCreate
from app.crud import users as user_crud
from tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_create_user_with_valid_data(session: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_create = UserCreate(email=email, password=password)
    user = await user_crud.create_user(session=session, user_create=user_create)
    assert user.email == email
    assert hasattr(user, "hashed_password")
