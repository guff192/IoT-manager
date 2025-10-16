from app.models.device import Device
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.device import ErrDeviceNotFound, ErrNotDeviceOwner
from app.api.exceptions.sensor import (
    ErrNotSensorOwner,
    ErrSensorNotFound,
    ErrSensorTypeExists,
)
from app.crud import devices as device_crud
from app.crud import sensors as sensor_crud
from app.models import SensorsPublic, SensorTypesPublic, User
from app.models.sensor import (
    SensorCreate,
    SensorPublic,
    SensorTypeCreate,
    SensorTypePublic,
    SensorUpdate,
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

        sensors = await sensor_crud.list_sensor_types(
            session=self.session, skip=skip, limit=limit
        )
        return SensorTypesPublic(data=sensors, count=count)

    async def create_sensor_type_service(
        self, sensor_type_in: SensorTypeCreate
    ) -> SensorTypePublic:
        sensor_type = await sensor_crud.get_sensor_type_by_name(
            session=self.session, name=sensor_type_in.name
        )
        if sensor_type:
            raise ErrSensorTypeExists(name=sensor_type_in.name)

        sensor_type = await sensor_crud.create_sensor_type(
            session=self.session, sensor_type_create=sensor_type_in
        )
        return SensorTypePublic.model_validate(sensor_type)

    async def list_user_sensors_service(self, user: User) -> SensorsPublic:
        count = await sensor_crud.count_user_sensors(session=self.session, user=user)
        if not count:
            return SensorsPublic(data=[], count=0)

        sensors = await sensor_crud.list_user_sensors(session=self.session, user=user)
        return SensorsPublic(data=sensors, count=count)

    async def create_user_sensor_service(
        self, user: User, sensor_in: SensorCreate
    ) -> SensorPublic:
        device = await device_crud.get_device_by_id(
            session=self.session, device_id=sensor_in.device_id
        )
        self._check_device_existence_and_owner(user, device)

        sensor = await sensor_crud.create_sensor(
            session=self.session, sensor_create=sensor_in
        )
        return SensorPublic.model_validate(sensor)

    async def get_sensor_info_service(
        self,
        user: User,
        sensor_id: str,
    ) -> SensorPublic:
        device = await device_crud.get_device_by_sensor_id(
            session=self.session, sensor_id=sensor_id
        )
        self._check_device_existence_and_owner(user, device)

        sensor = await sensor_crud.get_sensor_by_id(
            session=self.session, sensor_id=sensor_id
        )
        if not sensor:
            raise ErrSensorNotFound

        return SensorPublic.model_validate(sensor)

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

        sensor = await sensor_crud.get_sensor_by_id(
            session=self.session, sensor_id=sensor_id
        )
        if not sensor:
            raise ErrSensorNotFound

        sensor = await sensor_crud.update_sensor(
            session=self.session, db_sensor=sensor, sensor_update=sensor_in
        )
        return SensorPublic.model_validate(sensor)

    async def delete_user_sensor_service(
        self,
        user: User,
        sensor_id: str,
    ) -> None:
        device = await device_crud.get_device_by_sensor_id(
            session=self.session, sensor_id=sensor_id
        )
        self._check_device_existence_and_owner(user, device)

        sensor = await sensor_crud.get_sensor_by_id(
            session=self.session, sensor_id=sensor_id
        )
        if not sensor:
            raise ErrSensorNotFound

        await sensor_crud.delete_sensor(session=self.session, db_sensor=sensor)
