from app.models.sensor_data import SensorDataCreate
import asyncpg
import uuid

async def insert_sensor_data(conn: asyncpg.Connection, data: SensorDataCreate):
    sensor_data_id = str(uuid.uuid4())

    row = await conn.fetchrow(
        """
        INSERT INTO sensor_data (id, sensor_id, value, unit)
        VALUES ($1, $2, $3, $4)
        RETURNING id, sensor_id, value, unit, timestamp
        """,
        sensor_data_id, data.sensor_id, data.value, data.unit
    )
    return dict(row)


async def get_sensor_data_by_sensor(conn: asyncpg.Connection, sensor_id: str, limit: int = 100):
    print(f"Fetching sensor data for sensor_id: {sensor_id} with limit: {limit}")
    rows = await conn.fetch(
        """
        SELECT * FROM sensor_data
        WHERE sensor_id = $1
        ORDER BY timestamp DESC
        LIMIT $2
        """,
        sensor_id, limit
    )
    return [dict(row) for row in rows]

async def get_sensor_data_by_device(conn: asyncpg.Connection, device_id: str, limit: int = 100):
    print(f"Fetching sensor data for device_id: {device_id} with limit: {limit}")
    rows = await conn.fetch(
        """
        SELECT sd.id, d.name AS device_name, s.name AS sensor_name, sd.unit, sd.value, sd.timestamp
        FROM sensor_data sd
        JOIN sensors s ON sd.sensor_id = s.id
        JOIN devices d ON s.device_id = d.id
        WHERE d.id = $1
        LIMIT $2
        """,
        device_id, limit
    )
    return [dict(row) for row in rows]

async def delete_sensor_data(conn: asyncpg.Connection, sensor_data_id: str):
    row = await conn.fetchrow(
        "DELETE FROM sensor_data WHERE id = $1 RETURNING id, sensor_id, value, unit, timestamp",
        sensor_data_id
    )
    if row:
        return dict(row)
    return None