from dataclasses import dataclass
import uuid

@dataclass
class DeviceType:
    id: int
    name: str

@dataclass
class Device:
    id: uuid.UUID
    name: str
    is_active: bool
    type_id: int
    user_id: uuid.UUID
