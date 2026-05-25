from dataclasses import dataclass
from datetime import datetime

@dataclass
class SensorData:
    id: int
    data: float
    sensor_id: str
    created_at: datetime
