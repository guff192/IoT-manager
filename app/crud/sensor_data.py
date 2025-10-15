from datetime import datetime
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import asc, func, select, desc

from app.models import SensorData, SensorDataCreate, SensorDataPublic


async def create_sensor_data(
    *, session: AsyncSession, sensor_data_create: SensorDataCreate
) -> SensorData:
    """Creates a new sensor data record in the database."""
    db_obj = SensorData.model_validate(sensor_data_create)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def list_sensor_data_by_sensor_id(
    *,
    session: AsyncSession,
    sensor_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    reverse: bool = True,  # Newest first
    skip: int = 0,
    limit: int = 100,
) -> List[SensorDataPublic]:
    """
    Retrieves data points for a given sensor, with optional time-based filtering.
    Orders results by 'created_at' descending (newest first) by default.
    """
    statement = select(SensorData).where(SensorData.sensor_id == sensor_id)

    if start_time:
        statement = statement.where(SensorData.created_at >= start_time)
    if end_time:
        statement = statement.where(SensorData.created_at <= end_time)

    order_expr = desc(SensorData.created_at) if reverse else asc(SensorData.created_at)
    statement = (
        statement.order_by(order_expr).offset(skip).limit(limit)
    )

    result = await session.execute(statement)
    db_objects = result.scalars().all()
    return [SensorDataPublic.model_validate(obj) for obj in db_objects]


async def count_sensor_data_by_sensor_id(
    *,
    session: AsyncSession,
    sensor_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> int | None:
    """Counts the number of records for a given sensor within a specified time range."""
    statement = (
        select(func.count())
        .select_from(SensorData)
        .where(SensorData.sensor_id == sensor_id)
    )

    if start_time:
        statement = statement.where(SensorData.created_at >= start_time)
    if end_time:
        statement = statement.where(SensorData.created_at <= end_time)

    result = await session.execute(statement)
    return result.scalar_one_or_none()
