import uuid
from typing import List
from pydantic import BaseModel, Field

class SensorTypeBase(BaseModel):
    name: str = Field(max_length=255)
    unit: str

class SensorTypeCreate(SensorTypeBase):
    pass

class SensorTypePublic(SensorTypeBase):
    id: int

class SensorTypesPublic(BaseModel):
    data: List[SensorTypePublic]
    count: int

class SensorBase(BaseModel):
    name: str = Field(max_length=255)
    is_active: bool = False

class SensorCreate(SensorBase):
    type_id: int
    device_id: uuid.UUID

class SensorUpdate(BaseModel):
    name: str | None = Field(default=None)
    is_active: bool | None = Field(default=None)
    type_id: int | None = Field(default=None)

class SensorPublic(SensorBase):
    id: uuid.UUID

class SensorsPublic(BaseModel):
    data: List[SensorPublic]
    count: int
