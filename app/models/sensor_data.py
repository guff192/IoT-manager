from datetime import datetime
from typing import TYPE_CHECKING, Optional, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models import Sensor


class SensorDataBase(SQLModel):
    """Base model for sensor data fields."""

    data: float = Field(description="The measured sensor value.")

    sensor_id: str = Field(foreign_key="sensor.id", index=True, nullable=False)


class SensorDataCreate(SensorDataBase):
    """Schema for creating a new sensor data record."""

    pass


class SensorData(SensorDataBase, table=True):
    """DB model for sensor readings (timeseries data)."""

    id: Optional[int] = Field(default=None, primary_key=True)

    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    # Relationship back to the Sensor model
    sensor: "Sensor" = Relationship(back_populates="data")


class SensorDataPublic(SensorDataBase):
    """Schema for public response (reading sensor data)."""

    id: int
    created_at: datetime


class SensorDatasPublic(SQLModel):
    """Schema for a list of sensor data records."""

    data: List[SensorDataPublic]
    count: int
