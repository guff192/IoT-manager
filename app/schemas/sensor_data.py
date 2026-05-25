from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class SensorDataBase(BaseModel):
    data: float = Field(description="The measured sensor value.")
    sensor_id: str

class SensorDataCreate(SensorDataBase):
    pass

class SensorDataPublic(SensorDataBase):
    id: int
    created_at: datetime

class SensorDatasPublic(BaseModel):
    data: List[SensorDataPublic]
    count: int
