from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.deps import AsyncSessionDep, CurrentUser, get_current_active_superuser
from app.api.exceptions.device import ErrDeviceNotFound, ErrNotDeviceOwner
from app.api.exceptions.sensor import (
    ErrNotSensorOwner,
    ErrSensorNotFound,
    ErrSensorTypeExists,
)
from app.crud import devices as device_crud
from app.crud import sensors as sensor_crud
from app.models import (
    SensorPublic,
    SensorsPublic,
    SensorTypeCreate,
    SensorTypePublic,
    SensorTypesPublic,
)
from app.models.sensor import SensorCreate, SensorUpdate

router = APIRouter(prefix="/sensors", tags=["sensors"])


@router.get("/types", response_model=SensorTypesPublic)
async def list_sensor_types(
    session: AsyncSessionDep, skip: int = 0, limit: int = 100
) -> Any:
    count = await sensor_crud.count_sensor_types(session=session)
    if not count:
        return SensorTypesPublic(data=[], count=0)

    sensors = await sensor_crud.list_sensor_types(
        session=session, skip=skip, limit=limit
    )
    return SensorTypesPublic(data=sensors, count=count)


@router.post(
    "/types",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=SensorTypePublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_sensor_type(
    session: AsyncSessionDep, sensor_type_in: SensorTypeCreate
) -> Any:
    sensor_type = await sensor_crud.get_sensor_type_by_name(
        session=session, name=sensor_type_in.name
    )
    if sensor_type:
        raise ErrSensorTypeExists(name=sensor_type_in.name)

    sensor_type = await sensor_crud.create_sensor_type(
        session=session, sensor_type_create=sensor_type_in
    )
    return sensor_type


@router.get("/", response_model=SensorsPublic)
async def list_user_sensors(session: AsyncSessionDep, user: CurrentUser) -> Any:
    count = await sensor_crud.count_user_sensors(session=session, user=user)
    if not count:
        return SensorTypesPublic(data=[], count=0)

    sensors = await sensor_crud.list_user_sensors(session=session, user=user)
    return SensorsPublic(data=sensors, count=count)


@router.post("/", response_model=SensorPublic, status_code=status.HTTP_201_CREATED)
async def create_user_sensor(
    session: AsyncSessionDep, user: CurrentUser, sensor_in: SensorCreate
) -> Any:
    device = await device_crud.get_device_by_id(
        session=session, device_id=sensor_in.device_id
    )
    if not device:
        raise ErrDeviceNotFound
    if device.user_id != user.id:
        raise ErrNotDeviceOwner

    sensor = await sensor_crud.create_sensor(session=session, sensor_create=sensor_in)
    return sensor


@router.get("/{sensor_id}", response_model=SensorPublic)
async def get_sensor_info(
    session: AsyncSessionDep,
    user: CurrentUser,
    sensor_id: str,
) -> Any:
    device = await device_crud.get_device_by_sensor_id(session=session, sensor_id=sensor_id)
    if not device:
        raise ErrSensorNotFound
    if device.user_id != user.id:
        raise ErrNotSensorOwner

    sensor = await sensor_crud.get_sensor_by_id(session=session, sensor_id=sensor_id)
    if not sensor:
        raise ErrSensorNotFound

    return sensor


@router.patch("/{sensor_id}", response_model=SensorPublic)
async def update_user_sensor(
    session: AsyncSessionDep,
    user: CurrentUser,
    sensor_id: str,
    sensor_in: SensorUpdate,
) -> Any:
    device = await device_crud.get_device_by_sensor_id(session=session, sensor_id=sensor_id)
    if not device:
        raise ErrSensorNotFound
    if device.user_id != user.id:
        raise ErrNotSensorOwner

    sensor = await sensor_crud.get_sensor_by_id(session=session, sensor_id=sensor_id)
    if not sensor:
        raise ErrSensorNotFound

    sensor = await sensor_crud.update_sensor(
        session=session, db_sensor=sensor, sensor_update=sensor_in
    )
    return sensor


@router.delete("/{sensor_id}")
async def delete_user_sensor(
    session: AsyncSessionDep,
    user: CurrentUser,
    sensor_id: str,
) -> dict:
    device = await device_crud.get_device_by_sensor_id(session=session, sensor_id=sensor_id)
    if not device:
        raise ErrSensorNotFound
    if device.user_id != user.id:
        raise ErrNotSensorOwner

    sensor = await sensor_crud.get_sensor_by_id(session=session, sensor_id=sensor_id)
    if not sensor:
        raise ErrSensorNotFound

    await sensor_crud.delete_sensor(session=session, db_sensor=sensor)
    return {"ok": True}
