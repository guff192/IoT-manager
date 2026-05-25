import uuid
from typing import List
from pydantic import BaseModel, Field

class DeviceTypeBase(BaseModel):
    name: str = Field(max_length=255)

class DeviceTypeCreate(DeviceTypeBase):
    pass

class DeviceTypePublic(DeviceTypeBase):
    id: int

class DeviceTypesPublic(BaseModel):
    data: List[DeviceTypePublic]
    count: int

class DeviceBase(BaseModel):
    name: str = Field(max_length=255)
    is_active: bool = False

class DeviceCreate(DeviceBase):
    type_id: int

class DeviceUpdate(BaseModel):
    name: str | None = Field(default=None)
    is_active: bool | None = Field(default=None)
    type_id: int | None = Field(default=None)

class DevicePublic(DeviceBase):
    id: uuid.UUID

class DevicesPublic(BaseModel):
    data: List[DevicePublic]
    count: int
