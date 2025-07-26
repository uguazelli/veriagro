from app.models.sensor import SensorCreate, SensorOut
import asyncpg
import uuid

async def create_sensor(conn: asyncpg.Connection, sensor: SensorCreate) -> SensorOut:
    query = """
    INSERT INTO sensors (device_id, name, type, model, manufacturer, model_id, config)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    RETURNING id, device_id, name, type, model, manufacturer, model_id, config, created_at;
    """
    values = (
        sensor.device_id,
        sensor.name,
        sensor.type,
        sensor.model,
        sensor.manufacturer,
        sensor.model_id,
        sensor.config
    )
    row = await conn.fetchrow(query, *values)
    if row:
        return SensorOut(
            id=row['id'],
            device_id=row['device_id'],
            name=row['name'],
            type=row['type'],
            model=row['model'],
            manufacturer=row['manufacturer'],
            model_id=row['model_id'],
            config=row['config'],
            created_at=row['created_at']
        )
    return None

async def get_sensor_by_id(conn: asyncpg.Connection, sensor_id: str) -> SensorOut:
    query = "SELECT id, device_id, name, type, model, manufacturer, model_id, config, created_at FROM sensors WHERE id = $1;"
    row = await conn.fetchrow(query, uuid.UUID(sensor_id))
    if row:
        return SensorOut(
            id=row['id'],
            device_id=row['device_id'],
            name=row['name'],
            type=row['type'],
            model=row['model'],
            manufacturer=row['manufacturer'],
            model_id=row['model_id'],
            config=row['config'],
            created_at=row['created_at']
        )
    return None

async def delete_sensor(conn: asyncpg.Connection, sensor_id: str) -> SensorOut:
    query = "DELETE FROM sensors WHERE id = $1 RETURNING id, device_id, name, type, model, manufacturer, model_id, config, created_at;"
    row = await conn.fetchrow(query, uuid.UUID(sensor_id))
    if row:
        return SensorOut(
            id=row['id'],
            device_id=row['device_id'],
            name=row['name'],
            type=row['type'],
            model=row['model'],
            manufacturer=row['manufacturer'],
            model_id=row['model_id'],
            config=row['config'],
            created_at=row['created_at']
        )
    return None


async def get_sensor_by_device_id(conn: asyncpg.Connection, device_id: str) -> list[SensorOut]:
    query = "SELECT id, device_id, name, type, model, manufacturer, model_id, config, created_at FROM sensors WHERE device_id = $1;"
    rows = await conn.fetch(query, uuid.UUID(device_id))
    sensors = []
    for row in rows:
        sensors.append(SensorOut(
            id=row['id'],
            device_id=row['device_id'],
            name=row['name'],
            type=row['type'],
            model=row['model'],
            manufacturer=row['manufacturer'],
            model_id=row['model_id'],
            config=row['config'],
            created_at=row['created_at']
        ))
    return sensors
