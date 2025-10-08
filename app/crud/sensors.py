from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from app.models import (
    Sensor,
    SensorCreate,
    SensorPublic,
    SensorType,
    SensorTypePublic,
    SensorUpdate,
    User,
)


async def count_sensor_types(*, session: AsyncSession) -> int | None:
    statement = select(func.count()).select_from(SensorType)
    result = await session.execute(statement)
    return result.scalar()


async def list_sensor_types(*, session: AsyncSession, skip: int = 0, limit: int = 100) -> list[SensorTypePublic]:
    statement = select(SensorType).offset(skip).limit(limit)
    result = await session.execute(statement)
    db_objects = result.scalars().all()
    return [SensorTypePublic.model_validate(obj) for obj in db_objects]


async def get_sensor_by_id(*, session: AsyncSession, id: str) -> Sensor | None:
    return await session.get(Sensor, id)


async def count_user_sensors(*, session: AsyncSession, user: User) -> int | None:
    statement = select(func.count()).where(Sensor.device.user_id == user.id)
    result = await session.execute(statement)
    return result.scalar()


async def list_user_sensors(*, session: AsyncSession, user: User, skip: int = 0, limit: int = 100) -> list[SensorPublic]:
    statement = select(Sensor).where(Sensor.device.user_id == user.id).offset(skip).limit(limit)
    result = await session.execute(statement)
    db_objects = result.scalars().all()
    return [SensorPublic.model_validate(obj) for obj in db_objects]


async def create_sensor(
    *, session: AsyncSession, sensor_create: SensorCreate
) -> Sensor:
    db_obj = Sensor.model_validate(sensor_create)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def update_sensor(
    *, session: AsyncSession, db_sensor: Sensor, sensor_update: SensorUpdate
) -> Sensor:
    sensor_data = sensor_update.model_dump(exclude_unset=True)

    db_sensor.sqlmodel_update(sensor_data)
    session.add(db_sensor)
    await session.commit()
    await session.refresh(db_sensor)
    return db_sensor


async def delete_sensor(*, session: AsyncSession, db_sensor: Sensor) -> None:
    await session.delete(db_sensor)
    await session.commit()
    return
