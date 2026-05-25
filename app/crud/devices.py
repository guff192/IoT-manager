import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from app.models.persistence.device import DeviceTable, DeviceTypeTable
from app.models.persistence.sensor import SensorTable


async def count_device_types(*, session: AsyncSession) -> int | None:
    statement = select(func.count()).select_from(DeviceTypeTable)
    result = await session.execute(statement)
    return result.scalar()


async def list_device_types(
    *, session: AsyncSession, skip: int = 0, limit: int = 100
) -> list[DeviceTypeTable]:
    statement = select(DeviceTypeTable).offset(skip).limit(limit)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def create_device_type(
    *, session: AsyncSession, name: str
) -> DeviceTypeTable:
    db_obj = DeviceTypeTable(name=name)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def get_device_type_by_id(*, session: AsyncSession, id: int) -> DeviceTypeTable | None:
    return await session.get(DeviceTypeTable, id)


async def get_device_type_by_name(
    *, session: AsyncSession, name: str
) -> DeviceTypeTable | None:
    statement = select(DeviceTypeTable).where(DeviceTypeTable.name == name)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def count_user_devices(*, session: AsyncSession, user_id: str) -> int | None:
    statement = select(func.count()).where(DeviceTable.user_id == user_id)
    result = await session.execute(statement)
    return result.scalar()


async def get_device_by_id(*, session: AsyncSession, device_id: str) -> DeviceTable | None:
    return await session.get(DeviceTable, uuid.UUID(device_id))


async def get_device_by_sensor_id(
    *, session: AsyncSession, sensor_id: str
) -> DeviceTable | None:
    statement = select(DeviceTable).join(SensorTable).where(SensorTable.id == sensor_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def list_user_devices(*, session: AsyncSession, user_id: str):
    statement = select(DeviceTable).where(DeviceTable.user_id == user_id)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def create_device(
    *, session: AsyncSession, user_id: str, name: str, is_active: bool, type_id: int
) -> DeviceTable:
    db_obj = DeviceTable(
        name=name,
        is_active=is_active,
        type_id=type_id,
        user_id=user_id,
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def update_device(
    *, session: AsyncSession, db_device: DeviceTable, update_data: dict
) -> DeviceTable:
    for key, value in update_data.items():
        setattr(db_device, key, value)

    session.add(db_device)
    await session.commit()
    await session.refresh(db_device)
    return db_device


async def delete_device(*, session: AsyncSession, db_device: DeviceTable) -> None:
    await session.delete(db_device)
    await session.commit()
    return
