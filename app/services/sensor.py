from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.api.exceptions.device import ErrDeviceNotFound, ErrNotDeviceOwner
from app.api.exceptions.sensor import (
    ErrNotSensorOwner,
    ErrSensorNotFound,
    ErrSensorTypeExists,
)
from app.crud import devices as device_crud
from app.crud import sensors as sensor_crud
from app.models.domain.user import User
from app.models.device import Device
from app.schemas.sensor import (
    SensorCreate,
    SensorPublic,
    SensorTypeCreate,
    SensorTypePublic,
    SensorUpdate,
    SensorsPublic,
    SensorTypesPublic,
)
from app.mappers.sensor import (
    to_domain, 
    to_public, 
    to_domain_from_create,
    to_domain_type,
    to_public_type,
    to_persistence_type
)


class SensorService:
    def __init__(self, session: AsyncSession):
        """Injects the database session into the service instance."""
        self.session = session

    def _check_device_existence_and_owner(
        self, user: User, device: Device | None
    ) -> None:
        if not device:
            raise ErrDeviceNotFound
        if device.user_id != user.id:
            raise ErrNotDeviceOwner

    async def list_sensor_types_service(
        self, skip: int = 0, limit: int = 100
    ) -> SensorTypesPublic:
        count = await sensor_crud.count_sensor_types(session=self.session)
        if not count:
            return SensorTypesPublic(data=[], count=0)

        type_tables = await sensor_crud.list_sensor_types(
            session=self.session, skip=skip, limit=limit
        )
        
        # Map Persistence -> Domain -> Schema
        types_public = [to_public_type(to_domain_type(tt)) for tt in type_tables]
        return SensorTypesPublic(data=types_public, count=count)

    async def create_sensor_type_service(
        self, sensor_type_in: SensorTypeCreate
    ) -> SensorTypePublic:
        sensor_type_table = await sensor_crud.get_sensor_type_by_name(
            session=self.session, name=sensor_type_in.name
        )
        if sensor_type_table:
            raise ErrSensorTypeExists(name=sensor_type_in.name)

        sensor_type_table = await sensor_crud.create_sensor_type(
            session=self.session, 
            name=sensor_type_in.name, 
            unit=sensor_type_in.unit
        )
        return to_public_type(to_domain_type(sensor_type_table))

    async def list_user_sensors_service(self, user: User) -> SensorsPublic:
        count = await sensor_crud.count_user_sensors(session=self.session, user_id=user.id)
        if not count:
            return SensorsPublic(data=[], count=0)

        sensor_tables = await sensor_crud.list_user_sensors(session=self.session, user_id=user.id)
        
        # Map Persistence -> Domain -> Schema
        sensors_public = [to_public(to_domain(st)) for st in sensor_tables]
        return SensorsPublic(data=sensors_public, count=count)

    async def create_user_sensor_service(
        self, user: User, sensor_in: SensorCreate
    ) -> SensorPublic:
        device = await device_crud.get_device_by_id(
            session=self.session, device_id=sensor_in.device_id
        )
        self._check_device_existence_and_owner(user, device)

        sensor_table = await sensor_crud.create_sensor(
            session=self.session, 
            name=sensor_in.name,
            is_active=sensor_in.is_active,
            type_id=sensor_in.type_id,
            device_id=sensor_in.device_id
        )
        return to_public(to_domain(sensor_table))

    async def get_sensor_info_service(
        self,
        user: User,
        sensor_id: str,
    ) -> SensorPublic:
        device = await device_crud.get_device_by_sensor_id(
            session=self.session, sensor_id=sensor_id
        )
        self._check_device_existence_and_owner(user, device)

        sensor_table = await sensor_crud.get_sensor_by_id(
            session=self.session, sensor_id=sensor_id
        )
        if not sensor_table:
            raise ErrSensorNotFound

        return to_public(to_domain(sensor_table))

    async def update_user_sensor_service(
        self,
        user: User,
        sensor_id: str,
        sensor_in: SensorUpdate,
    ) -> SensorPublic:
        device = await device_crud.get_device_by_sensor_id(
            session=self.session, sensor_id=sensor_id
        )
        self._check_device_existence_and_owner(user, device)

        sensor_table = await sensor_crud.get_sensor_by_id(
            session=self.session, sensor_id=sensor_id
        )
        if not sensor_table:
            raise ErrSensorNotFound

        updated_table = await sensor_crud.update_sensor(
            session=self.session, db_sensor=sensor_table, update_data=sensor_in.model_dump(exclude_unset=True)
        )
        return to_public(to_domain(updated_table))

    async def delete_user_sensor_service(
        self,
        user: User,
        sensor_id: str,
    ) -> None:
        device = await device_crud.get_device_by_sensor_id(
            session=self.session, sensor_id=sensor_id
        )
        self._check_device_existence_and_owner(user, device)

        sensor_table = await sensor_crud.get_sensor_by_id(
            session=self.session, sensor_id=sensor_id
        )
        if not sensor_table:
            raise ErrSensorNotFound

        await sensor_crud.delete_sensor(session=self.session, db_sensor=sensor_table)
