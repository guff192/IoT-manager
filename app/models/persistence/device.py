from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.persistence.user import UserTable
    from app.models.persistence.sensor import SensorTable


class DeviceTypeTable(SQLModel, table=True):
    __tablename__ = "devicetype"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    
    devices: list["DeviceTable"] = Relationship(back_populates="type")


class DeviceTable(SQLModel, table=True):
    __tablename__ = "device"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    is_active: bool = Field(default=False)
    type_id: int = Field(foreign_key="devicetype.id", nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")

    type: "DeviceTypeTable" = Relationship(back_populates="devices")
    user: "UserTable" = Relationship(back_populates="devices")
    sensors: list["SensorTable"] = Relationship(back_populates="device", cascade_delete=True)
