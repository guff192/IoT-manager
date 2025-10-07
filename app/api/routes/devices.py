from typing import Any
from fastapi import APIRouter, Depends, status

from app.api.deps import AsyncSessionDep, CurrentUser, get_current_active_superuser
from app.api.exceptions.device import (
    ErrDeviceNotFound,
    ErrDeviceTypeExists,
    ErrNotDeviceOwner,
)
from app.models.device import (
    DeviceCreate,
    DevicePublic,
    DeviceTypeCreate,
    DeviceTypePublic,
    DeviceTypesPublic,
    DeviceUpdate,
    DevicesPublic,
)
from app.crud import devices as device_crud


router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/types", response_model=DeviceTypesPublic)
async def list_device_types(
    session: AsyncSessionDep, skip: int = 0, limit: int = 100
) -> Any:
    count = await device_crud.count_device_types(session=session)
    if not count:
        return DeviceTypesPublic(data=[], count=0)

    devices = await device_crud.list_device_types(
        session=session, skip=skip, limit=limit
    )
    return DeviceTypesPublic(data=devices, count=count)


@router.post(
    "/types",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=DeviceTypePublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_device_type(
    session: AsyncSessionDep, device_type_in: DeviceTypeCreate
) -> Any:
    device_type = await device_crud.get_device_type_by_name(
        session=session, name=device_type_in.name
    )
    if device_type:
        raise ErrDeviceTypeExists(name=device_type_in.name)

    device_type = await device_crud.create_device_type(
        session=session, device_type_create=device_type_in
    )
    return device_type


@router.get("/", response_model=DevicesPublic)
async def list_user_devices(session: AsyncSessionDep, user: CurrentUser) -> Any:
    count = await device_crud.count_user_devices(session=session, user=user)
    if not count:
        return DeviceTypesPublic(data=[], count=0)

    devices = await device_crud.list_user_devices(session=session, user=user)
    return DevicesPublic(data=devices, count=count)


@router.post("/", response_model=DevicePublic, status_code=status.HTTP_201_CREATED)
async def create_user_device(
    session: AsyncSessionDep, user: CurrentUser, device_in: DeviceCreate
) -> Any:
    device = await device_crud.create_device(
        session=session, user=user, device_create=device_in
    )
    return device


@router.get("/{device_id}", response_model=DevicePublic)
async def get_device_info(
    session: AsyncSessionDep,
    user: CurrentUser,
    device_id: str,
) -> Any:
    device = await device_crud.get_device_by_id(session=session, device_id=device_id)
    if not device:
        raise ErrDeviceNotFound
    if device.user_id != user.id:
        raise ErrNotDeviceOwner

    return device


@router.patch("/{device_id}", response_model=DevicePublic)
async def update_user_device(
    session: AsyncSessionDep,
    user: CurrentUser,
    device_id: str,
    device_in: DeviceUpdate,
) -> Any:
    device = await device_crud.get_device_by_id(session=session, device_id=device_id)
    if not device:
        raise ErrDeviceNotFound
    if device.user_id != user.id:
        raise ErrNotDeviceOwner

    device = await device_crud.update_device(
        session=session, db_device=device, device_update=device_in
    )
    return device


@router.delete("/{device_id}")
async def delete_user_device(
    session: AsyncSessionDep,
    user: CurrentUser,
    device_id: str,
) -> dict:
    device = await device_crud.get_device_by_id(session=session, device_id=device_id)
    if not device:
        raise ErrDeviceNotFound
    if device.user_id != user.id:
        raise ErrNotDeviceOwner

    await device_crud.delete_device(session=session, db_device=device)
    return {"ok": True}
