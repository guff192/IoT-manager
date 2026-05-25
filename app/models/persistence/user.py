import uuid
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.device import Device as DeviceTable


class UserTable(SQLModel, table=True):
    __tablename__ = "user"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    hashed_password: str

    devices: list["DeviceTable"] = Relationship(back_populates="user", cascade_delete=True)
