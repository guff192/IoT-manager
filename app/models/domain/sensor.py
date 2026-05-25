from dataclasses import dataclass
import uuid

@dataclass
class SensorType:
    id: int
    name: str
    unit: str

@dataclass
class Sensor:
    id: uuid.UUID
    name: str
    is_active: bool
    type_id: int
    device_id: uuid.UUID
