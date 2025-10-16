from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.device import (
    ErrDeviceNotFound,
    ErrDeviceTypeExists,
    ErrNotDeviceOwner,
)
from app.crud import devices as device_crud
from app.models import (
    DeviceCreate,
    DevicePublic,
    DevicesPublic,
    DeviceTypeCreate,
    DeviceTypePublic,
    DeviceTypesPublic,
    DeviceUpdate,
    User,
)


class DeviceService:
    """
    Service layer for Device and DeviceType operations.
    Handles business logic, existence checks, and ownership validation.
    """

    def __init__(self, session: AsyncSession):
        """Injects the database session into the service instance."""
        self.session = session

    async def list_device_types_service(
        self, skip: int = 0, limit: int = 100
    ) -> DeviceTypesPublic:
        count = await device_crud.count_device_types(session=self.session)
        if not count:
            return DeviceTypesPublic(data=[], count=0)

        devices = await device_crud.list_device_types(
            session=self.session, skip=skip, limit=limit
        )
        return DeviceTypesPublic(data=devices, count=count)

    async def create_device_type_service(
        self, device_type_in: DeviceTypeCreate
    ) -> DeviceTypePublic:
        device_type = await device_crud.get_device_type_by_name(
            session=self.session, name=device_type_in.name
        )
        if device_type:
            raise ErrDeviceTypeExists(name=device_type_in.name)

        device_type = await device_crud.create_device_type(
            session=self.session, device_type_create=device_type_in
        )
        return DeviceTypePublic.model_validate(device_type)

    async def list_user_devices_service(self, user: User) -> DevicesPublic:
        count = await device_crud.count_user_devices(session=self.session, user=user)
        if not count:
            return DevicesPublic(data=[], count=0)

        devices = await device_crud.list_user_devices(session=self.session, user=user)
        return DevicesPublic(data=devices, count=count)

    async def create_user_device_service(
        self, user: User, device_in: DeviceCreate
    ) -> DevicePublic:
        device = await device_crud.create_device(
            session=self.session, user=user, device_create=device_in
        )
        return DevicePublic.model_validate(device)

    async def get_device_info_service(self, user: User, device_id: str) -> DevicePublic:
        device = await device_crud.get_device_by_id(
            session=self.session, device_id=device_id
        )
        if not device:
            raise ErrDeviceNotFound
        if device.user_id != user.id:
            raise ErrNotDeviceOwner

        return DevicePublic.model_validate(device)

    async def update_user_device_service(
        self, user: User, device_id: str, device_in: DeviceUpdate
    ) -> DevicePublic:
        device = await device_crud.get_device_by_id(session=self.session, device_id=device_id)
        if not device:
            raise ErrDeviceNotFound
        if device.user_id != user.id:
            raise ErrNotDeviceOwner

        device = await device_crud.update_device(
            session=self.session, db_device=device, device_update=device_in
        )
        return DevicePublic.model_validate(device)

    async def delete_user_device_service(
        self, user: User, device_id: str
    ) -> None:
        device = await device_crud.get_device_by_id(session=self.session, device_id=device_id)
        if not device:
            raise ErrDeviceNotFound
        if device.user_id != user.id:
            raise ErrNotDeviceOwner

        await device_crud.delete_device(session=self.session, db_device=device)
