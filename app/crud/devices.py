import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from app.models import (
    Device,
    DeviceCreate,
    DevicePublic,
    DeviceType,
    DeviceTypeCreate,
    DeviceTypePublic,
    DeviceUpdate,
    User,
)


async def count_device_types(*, session: AsyncSession) -> int | None:
    statement = select(func.count()).select_from(DeviceType)
    result = await session.execute(statement)
    return result.scalar()


async def list_device_types(
    *, session: AsyncSession, skip: int = 0, limit: int = 100
) -> list[DeviceTypePublic]:
    statement = select(DeviceType).offset(skip).limit(limit)
    result = await session.execute(statement)
    db_objects = result.scalars().all()
    return [DeviceTypePublic.model_validate(obj) for obj in db_objects]


async def create_device_type(
    *, session: AsyncSession, device_type_create: DeviceTypeCreate
) -> DeviceType:
    db_obj = DeviceType.model_validate(device_type_create)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def get_device_type_by_id(*, session: AsyncSession, id: int) -> DeviceType | None:
    return await session.get(DeviceType, id)


async def get_device_type_by_name(
    *, session: AsyncSession, name: str
) -> DeviceType | None:
    statement = select(DeviceType).where(DeviceType.name == name)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def count_user_devices(*, session: AsyncSession, user: User) -> int | None:
    statement = select(func.count()).where(Device.user_id == user.id)
    result = await session.execute(statement)
    return result.scalar()


async def get_device_by_id(*, session: AsyncSession, device_id: str) -> Device | None:
    return await session.get(Device, uuid.UUID(device_id))


async def list_user_devices(*, session: AsyncSession, user: User):
    statement = select(Device).where(Device.user_id == user.id)
    result = await session.execute(statement)
    db_objects = result.scalars().all()
    return [DevicePublic.model_validate(obj) for obj in db_objects]


async def create_device(
    *, session: AsyncSession, user: User, device_create: DeviceCreate
) -> Device:
    db_obj = Device.model_validate(device_create, update={"user_id": user.id})
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def update_device(
    *, session: AsyncSession, db_device: Device, device_update: DeviceUpdate
) -> Device:
    device_data = device_update.model_dump(exclude_unset=True)

    db_device.sqlmodel_update(device_data)
    session.add(db_device)
    await session.commit()
    await session.refresh(db_device)
    return db_device


async def delete_device(*, session: AsyncSession, db_device: Device) -> None:
    await session.delete(db_device)
    await session.commit()
    return
