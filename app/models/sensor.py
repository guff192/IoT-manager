from typing import TYPE_CHECKING, Optional
import uuid

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.models import Device


class SensorTypeBase(SQLModel):
    """Base sensor type scheme"""

    name: str = Field(
        unique=True,
        index=True,
        description="A type of sensor (e.g. 'Temperature', 'Humidity', 'Pressure')",
    )
    unit: str = Field(description="Unit of measurement (e.g. '°C', '%', 'mbar')")


class SensorTypeCreate(SensorTypeBase):
    pass


class SensorType(SensorTypeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    sensors: list["Sensor"] = Relationship(back_populates="type")


class SensorTypePublic(SensorTypeBase):
    id: int


class SensorTypesPublic(SQLModel):
    data: list[SensorTypePublic]
    count: int


class SensorBase(SQLModel):
    name: str = Field(
        index=True, description="User name for sensor (e.g. 'Living room temperature')"
    )
    is_active: bool = Field(default=False, description="Current state of activity")


class SensorCreate(SensorBase):
    type_id: int


class SensorUpdate(SQLModel):
    name: str | None = Field(default=None)
    is_active: bool | None = Field(default=None)
    type_id: int | None = Field(default=None)


class Sensor(SensorBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    type_id: int = Field(foreign_key="sensortype.id", nullable=False)
    type: SensorType = Relationship(back_populates="sensors")

    device_id: uuid.UUID = Field(
        foreign_key="device.id", nullable=False, ondelete="CASCADE"
    )
    device: "Device" = Relationship(back_populates="sensors")


class SensorPublic(SensorBase):
    id: uuid.UUID


class SensorsPublic(SQLModel):
    data: list[SensorPublic]
    count: int
