import uuid
from sqlmodel import Field, Relationship, SQLModel


class DeviceTypeBase(SQLModel):
    """Scheme for device type"""

    name: str = Field(
        index=True,
        description="A type of device (e.g. 'Light', 'Humidity', 'Thermostat')",
    )

    devices: list["Device"] = Relationship(back_populates="type")


class DeviceType(DeviceTypeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class DeviceBase(SQLModel):
    """Basic device scheme"""

    name: str = Field(
        index=True, description="User name for device (e.g. 'Living room light')"
    )
    is_active: bool = Field(default=False, description="Current state of activity")


class Device(DeviceBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    type_id: int | None = Field(default=None, foreign_key="type.id")
    type: DeviceType | None = Relationship(back_populates="devices")
