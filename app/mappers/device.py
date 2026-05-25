import uuid
from app.models.persistence.device import DeviceTable, DeviceTypeTable
from app.models.domain.device import Device, DeviceType
from app.schemas.device import DevicePublic, DeviceCreate, DeviceTypePublic, DeviceTypeCreate


def to_domain(table: DeviceTable) -> Device:
    return Device(
        id=table.id,
        name=table.name,
        is_active=table.is_active,
        type_id=table.type_id,
        user_id=table.user_id,
    )


def to_persistence(domain: Device, table: DeviceTable | None = None) -> DeviceTable:
    if table is None:
        return DeviceTable(
            id=domain.id,
            name=domain.name,
            is_active=domain.is_active,
            type_id=domain.type_id,
            user_id=domain.user_id,
        )
    table.name = domain.name
    table.is_active = domain.is_active
    table.type_id = domain.type_id
    table.user_id = domain.user_id
    return table


def to_public(domain: Device) -> DevicePublic:
    return DevicePublic(
        id=domain.id,
        name=domain.name,
        is_active=domain.is_active,
    )


def to_domain_from_create(schema: DeviceCreate) -> Device:
    return Device(
        id=uuid.uuid4(),
        name=schema.name,
        is_active=schema.is_active,
        type_id=schema.type_id,
        user_id=uuid.uuid4(), # Set by service
    )


def to_domain_type(table: DeviceTypeTable) -> DeviceType:
    return DeviceType(
        id=table.id,
        name=table.name,
    )


def to_public_type(domain: DeviceType) -> DeviceTypePublic:
    return DeviceTypePublic(
        id=domain.id,
        name=domain.name,
    )


def to_persistence_type(domain: DeviceType, table: DeviceTypeTable | None = None) -> DeviceTypeTable:
    if table is None:
        return DeviceTypeTable(
            id=domain.id,
            name=domain.name,
        )
    table.name = domain.name
    return table
