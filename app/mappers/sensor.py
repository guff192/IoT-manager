import uuid
from app.models.persistence.sensor import SensorTable, SensorTypeTable
from app.models.domain.sensor import Sensor, SensorType
from app.schemas.sensor import SensorPublic, SensorCreate, SensorTypePublic, SensorTypeCreate


def to_domain(table: SensorTable) -> Sensor:
    return Sensor(
        id=table.id,
        name=table.name,
        is_active=table.is_active,
        type_id=table.type_id,
        device_id=table.device_id,
    )


def to_persistence(domain: Sensor, table: SensorTable | None = None) -> SensorTable:
    if table is None:
        return SensorTable(
            id=domain.id,
            name=domain.name,
            is_active=domain.is_active,
            type_id=domain.type_id,
            device_id=domain.device_id,
        )
    table.name = domain.name
    table.is_active = domain.is_active
    table.type_id = domain.type_id
    table.device_id = domain.device_id
    return table


def to_public(domain: Sensor) -> SensorPublic:
    return SensorPublic(
        id=domain.id,
        name=domain.name,
        is_active=domain.is_active,
    )


def to_domain_from_create(schema: SensorCreate) -> Sensor:
    return Sensor(
        id=uuid.uuid4(),
        name=schema.name,
        is_active=schema.is_active,
        type_id=schema.type_id,
        device_id=schema.device_id,
    )


def to_domain_type(table: SensorTypeTable) -> SensorType:
    return SensorType(
        id=table.id,
        name=table.name,
        unit=table.unit,
    )


def to_public_type(domain: SensorType) -> SensorTypePublic:
    return SensorTypePublic(
        id=domain.id,
        name=domain.name,
        unit=domain.unit,
    )


def to_persistence_type(domain: SensorType, table: SensorTypeTable | None = None) -> SensorTypeTable:
    if table is None:
        return SensorTypeTable(
            id=domain.id,
            name=domain.name,
            unit=domain.unit,
        )
    table.name = domain.name
    table.unit = domain.unit
    return table
