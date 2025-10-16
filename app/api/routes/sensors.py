from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.deps import AsyncSessionDep, CurrentUser, get_current_active_superuser
from app.models import (
    SensorCreate,
    SensorPublic,
    SensorsPublic,
    SensorTypeCreate,
    SensorTypePublic,
    SensorTypesPublic,
    SensorUpdate,
)
from app.services.sensor import SensorService

router = APIRouter(prefix="/sensors", tags=["sensors"])


async def sensor_service_dependency(
    session: AsyncSessionDep,
) -> SensorService:
    """Dependency that creates and provides a SensorService instance, injecting the DB session."""
    return SensorService(session=session)


SensorServiceDep = Annotated[SensorService, Depends(sensor_service_dependency)]


@router.get("/types", response_model=SensorTypesPublic)
async def list_sensor_types(
    sensor_service: SensorServiceDep, skip: int = 0, limit: int = 100
) -> Any:
    sensors = await sensor_service.list_sensor_types_service(skip=skip, limit=limit)
    return sensors


@router.post(
    "/types",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=SensorTypePublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_sensor_type(
    sensor_service: SensorServiceDep, sensor_type_in: SensorTypeCreate
) -> Any:
    sensor_type = await sensor_service.create_sensor_type_service(sensor_type_in)
    return sensor_type


@router.get("/", response_model=SensorsPublic)
async def list_user_sensors(sensor_service: SensorServiceDep, user: CurrentUser) -> Any:
    sensors = await sensor_service.list_user_sensors_service(user=user)
    return sensors


@router.post("/", response_model=SensorPublic, status_code=status.HTTP_201_CREATED)
async def create_user_sensor(
    sensor_service: SensorServiceDep, user: CurrentUser, sensor_in: SensorCreate
) -> Any:
    sensor = await sensor_service.create_user_sensor_service(user=user, sensor_in=sensor_in)
    return sensor


@router.get("/{sensor_id}", response_model=SensorPublic)
async def get_sensor_info(
    sensor_service: SensorServiceDep,
    user: CurrentUser,
    sensor_id: str,
) -> Any:
    sensor = await sensor_service.get_sensor_info_service(user=user, sensor_id=sensor_id)
    return sensor


@router.patch("/{sensor_id}", response_model=SensorPublic)
async def update_user_sensor(
    sensor_service: SensorServiceDep,
    user: CurrentUser,
    sensor_id: str,
    sensor_in: SensorUpdate,
) -> Any:
    sensor = await sensor_service.update_user_sensor_service(
        user=user, sensor_id=sensor_id, sensor_in=sensor_in
    )
    return sensor


@router.delete("/{sensor_id}")
async def delete_user_sensor(
    sensor_service: SensorServiceDep,
    user: CurrentUser,
    sensor_id: str,
) -> dict:
    await sensor_service.delete_user_sensor_service(user=user, sensor_id=sensor_id)
    return {"ok": True}
