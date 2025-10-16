from typing import Annotated, Any
from fastapi import APIRouter, Depends, status

from app.api.deps import AsyncSessionDep, CurrentUser, get_current_active_superuser
from app.api.exceptions.device import (
    ErrDeviceNotFound,
    ErrDeviceTypeExists,
    ErrNotDeviceOwner,
)
from app.models import (
    DeviceCreate,
    DevicePublic,
    DeviceTypeCreate,
    DeviceTypePublic,
    DeviceTypesPublic,
    DeviceUpdate,
    DevicesPublic,
)
from app.crud import devices as device_crud
from app.services.devices import DeviceService


router = APIRouter(prefix="/devices", tags=["devices"])


async def device_service_dependency(session: AsyncSessionDep) -> DeviceService:
    """Dependency that creates and provides a DeviceService instance, injecting the DB session."""
    return DeviceService(session=session)


DeviceServiceDep = Annotated[DeviceService, Depends(device_service_dependency)]


@router.get("/types", response_model=DeviceTypesPublic)
async def list_device_types(
    device_service: DeviceServiceDep, skip: int = 0, limit: int = 100
) -> Any:
    device_types = await device_service.list_device_types_service(skip, limit)
    return device_types


@router.post(
    "/types",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=DeviceTypePublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_device_type(
    device_service: DeviceServiceDep, device_type_in: DeviceTypeCreate
) -> Any:
    device_type = await device_service.create_device_type_service(device_type_in)
    return device_type


@router.get("/", response_model=DevicesPublic)
async def list_user_devices(device_service: DeviceServiceDep, user: CurrentUser) -> Any:
    devices = await device_service.list_user_devices_service(user)
    return devices


@router.post("/", response_model=DevicePublic, status_code=status.HTTP_201_CREATED)
async def create_user_device(
    device_service: DeviceServiceDep, user: CurrentUser, device_in: DeviceCreate
) -> Any:
    device = await device_service.create_user_device_service(user, device_in)
    return device


@router.get("/{device_id}", response_model=DevicePublic)
async def get_device_info(
    device_service: DeviceServiceDep,
    user: CurrentUser,
    device_id: str,
) -> Any:
    device = await device_service.get_device_info_service(user, device_id)
    return device


@router.patch("/{device_id}", response_model=DevicePublic)
async def update_user_device(
    device_service: DeviceServiceDep,
    user: CurrentUser,
    device_id: str,
    device_in: DeviceUpdate,
) -> Any:
    device = await device_service.update_user_device_service(user, device_id, device_in)
    return device


@router.delete("/{device_id}")
async def delete_user_device(
    device_service: DeviceServiceDep,
    user: CurrentUser,
    device_id: str,
) -> dict:
    await device_service.delete_user_device_service(user, device_id)
    return {"ok": True}
