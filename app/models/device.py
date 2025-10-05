from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.models import User


class DeviceTypeBase(SQLModel):
    """Scheme for device type"""

    name: str = Field(
        index=True,
        description="A type of device (e.g. 'Light', 'Humidity', 'Thermostat')",
    )


class DeviceType(DeviceTypeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    devices: list["Device"] = Relationship(back_populates="type")


class DeviceBase(SQLModel):
    """Basic device scheme"""

    name: str = Field(
        index=True, description="User name for device (e.g. 'Living room light')"
    )
    is_active: bool = Field(default=False, description="Current state of activity")


class Device(DeviceBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    type_id: int | None = Field(default=None, foreign_key="devicetype.id")
    type: DeviceType | None = Relationship(back_populates="devices")

    user_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    user: Optional["User"] = Relationship(back_populates="devices")
