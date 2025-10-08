from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.models import User


class DeviceTypeBase(SQLModel):
    """Scheme for device type"""

    name: str = Field(
        unique=True,
        index=True,
        description="A type of device (e.g. 'Light', 'Humidity', 'Thermostat')",
    )


class DeviceTypeCreate(DeviceTypeBase):
    pass


class DeviceType(DeviceTypeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    devices: list["Device"] = Relationship(back_populates="type")


class DeviceTypePublic(DeviceTypeBase):
    id: int


class DeviceTypesPublic(SQLModel):
    data: list[DeviceTypePublic]
    count: int


class DeviceBase(SQLModel):
    """Basic device scheme"""

    name: str = Field(
        index=True, description="User name for device (e.g. 'Living room light')"
    )
    is_active: bool = Field(default=False, description="Current state of activity")


class DeviceCreate(DeviceBase):
    type_id: int


class DeviceUpdate(DeviceBase):
    name: str | None = Field(default=None)  # type: ignore
    is_active: bool | None = Field(default=None)  # type: ignore
    type_id: int | None = Field(default=None)


class Device(DeviceBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    type_id: int = Field(foreign_key="devicetype.id", nullable=False)
    type: DeviceType = Relationship(back_populates="devices")

    user_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    user: "User" = Relationship(back_populates="devices")


class DevicePublic(DeviceBase):
    id: uuid.UUID


class DevicesPublic(SQLModel):
    data: list[DevicePublic]
    count: int
