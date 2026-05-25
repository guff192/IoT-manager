from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.persistence.sensor import SensorTable


class SensorDataTable(SQLModel, table=True):
    __tablename__ = "sensordata"

    id: Optional[int] = Field(default=None, primary_key=True)
    data: float = Field(description="The measured sensor value.")
    sensor_id: str = Field(foreign_key="sensor.id", index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    sensor: "SensorTable" = Relationship(back_populates="data")
