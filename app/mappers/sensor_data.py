from app.models.persistence.sensor_data import SensorDataTable
from app.models.domain.sensor_data import SensorData
from app.schemas.sensor_data import SensorDataPublic, SensorDataCreate


def to_domain(table: SensorDataTable) -> SensorData:
    return SensorData(
        id=table.id,
        data=table.data,
        sensor_id=table.sensor_id,
        created_at=table.created_at,
    )


def to_persistence(domain: SensorData, table: SensorDataTable | None = None) -> SensorDataTable:
    if table is None:
        return SensorDataTable(
            id=domain.id,
            data=domain.data,
            sensor_id=domain.sensor_id,
            created_at=domain.created_at,
        )
    
    table.data = domain.data
    table.sensor_id = domain.sensor_id
    table.created_at = domain.created_at
    return table


def to_public(domain: SensorData) -> SensorDataPublic:
    return SensorDataPublic(
        id=domain.id,
        data=domain.data,
        sensor_id=domain.sensor_id,
        created_at=domain.created_at,
    )


def to_domain_from_create(schema: SensorDataCreate) -> SensorData:
    # ID and created_at are usually handled by DB
    from datetime import datetime
    import uuid # not needed for int id but for consistency
    return SensorData(
        id=0, # Placeholder
        data=schema.data,
        sensor_id=schema.sensor_id,
        created_at=datetime.now(),
    )
