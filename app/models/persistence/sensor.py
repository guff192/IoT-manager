import uuid
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.persistence.device import DeviceTable
    from app.models.persistence.sensor_data import SensorDataTable


class SensorTypeTable(SQLModel, table=True):
    __tablename__ = "sensortype"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    unit: str = Field()

    sensors: list["SensorTable"] = Relationship(back_populates="type")


class SensorTable(SQLModel, table=True):
    __tablename__ = "sensor"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    is_active: bool = Field(default=False)
    type_id: int = Field(foreign_key="sensortype.id", nullable=False)
    device_id: uuid.UUID = Field(foreign_key="device.id", nullable=False, ondelete="CASCADE")

    type: "SensorTypeTable" = Relationship(back_populates="sensors")
    device: "DeviceTable" = Relationship(back_populates="sensors")
    data: list["SensorDataTable"] = Relationship(back_populates="sensor")
