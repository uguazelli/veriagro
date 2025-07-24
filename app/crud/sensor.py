from app.models.sensor import SensorCreate
import asyncpg
import uuid

async def create_sensor(conn: asyncpg.Connection, sensor: SensorCreate):
    sensor_id = str(uuid.uuid4())

    row = await conn.fetchrow("""
        INSERT INTO sensors (id, device_id, name, type, model, manufacturer,  created_at)
        VALUES ($1, $2, $3, $4, $5, $6, now())
        RETURNING *
    """, sensor_id, sensor.device_id, sensor.name, sensor.type, sensor.model, sensor.manufacturer)

    return dict(row)

async def get_sensor_by_id(conn: asyncpg.Connection, id: uuid.UUID):
    rows = await conn.fetch("SELECT * FROM sensors WHERE id = $1", id)
    return [dict(row) for row in rows]


async def get_sensor_by_device_id(conn: asyncpg.Connection, device_id: uuid.UUID):
    rows = await conn.fetch("SELECT * FROM sensors WHERE device_id = $1", device_id)
    return [dict(row) for row in rows]

async def delete_sensor(conn: asyncpg.Connection, sensor_id: uuid.UUID):
    row = await conn.fetchrow("DELETE FROM sensors WHERE id = $1 RETURNING *", sensor_id)
    if row:
        return dict(row)
    return None