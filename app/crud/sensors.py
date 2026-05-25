from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from app.models.persistence.sensor import SensorTable, SensorTypeTable
from app.models.device import Device


async def count_sensor_types(*, session: AsyncSession) -> int | None:
    statement = select(func.count()).select_from(SensorTypeTable)
    result = await session.execute(statement)
    return result.scalar()


async def list_sensor_types(
    *, session: AsyncSession, skip: int = 0, limit: int = 100
) -> list[SensorTypeTable]:
    statement = select(SensorTypeTable).offset(skip).limit(limit)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_sensor_type_by_name(
    *, session: AsyncSession, name: str
) -> SensorTypeTable | None:
    statement = select(SensorTypeTable).where(SensorTypeTable.name == name)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def create_sensor_type(
    *, session: AsyncSession, name: str, unit: str
) -> SensorTypeTable:
    db_obj = SensorTypeTable(name=name, unit=unit)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def get_sensor_by_id(*, session: AsyncSession, sensor_id: str) -> SensorTable | None:
    return await session.get(SensorTable, sensor_id)


async def count_user_sensors(*, session: AsyncSession, user_id: str) -> int | None:
    statement = select(func.count()).select_from(SensorTable).join(Device).where(Device.user_id == user_id)
    result = await session.execute(statement)
    return result.scalar()


async def list_user_sensors(
    *, session: AsyncSession, user_id: str, skip: int = 0, limit: int = 100
) -> list[SensorTable]:
    statement = (
        select(SensorTable).join(Device).where(Device.user_id == user_id).offset(skip).limit(limit)
    )
    result = await session.execute(statement)
    return list(result.scalars().all())


async def create_sensor(
    *, session: AsyncSession, name: str, is_active: bool, type_id: int, device_id: str
) -> SensorTable:
    db_obj = SensorTable(
        name=name, 
        is_active=is_active, 
        type_id=type_id, 
        device_id=device_id
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def update_sensor(
    *, session: AsyncSession, db_sensor: SensorTable, update_data: dict
) -> SensorTable:
    for key, value in update_data.items():
        setattr(db_sensor, key, value)

    session.add(db_sensor)
    await session.commit()
    await session.refresh(db_sensor)
    return db_sensor


async def delete_sensor(*, session: AsyncSession, db_sensor: SensorTable) -> None:
    await session.delete(db_sensor)
    await session.commit()
    return
