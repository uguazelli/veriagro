from app.models.sensor_data import SensorDataIn, SensorDataOut
import asyncpg
import uuid

async def insert_sensor_data(conn: asyncpg.Connection, data: SensorDataIn):
    print(f"Inserting sensor data: {data}")
    row = await conn.fetchrow(
        """
        INSERT INTO sensor_data (id, sensor_id, unit, value, status)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, sensor_id, unit, value, status, timestamp
        """,
        uuid.uuid4(), data.sensor_id, data.unit, data.value, data.status
    )
    return SensorDataOut(**dict(row))


async def get_sensor_data_by_sensor(conn: asyncpg.Connection, sensor_id: str, limit: int = 100):
    print(f"Fetching sensor data for sensor_id: {sensor_id} with limit: {limit}")
    rows = await conn.fetch(
        """
        SELECT id, sensor_id, unit, value, status, timestamp
        FROM sensor_data
        WHERE sensor_id = $1
        ORDER BY timestamp DESC
        LIMIT $2
        """,
        sensor_id, limit
    )
    return [SensorDataOut(**dict(row)) for row in rows]


async def get_sensor_data_by_device(conn: asyncpg.Connection, device_id: str, limit: int = 1000):
    print(f"Fetching sensor data for device_id: {device_id} with limit: {limit}")
    rows = await conn.fetch(
        """
        SELECT sd.id, sd.sensor_id, sd.unit, sd.value, sd.status, sd.timestamp
        FROM sensor_data sd
        JOIN sensors s ON sd.sensor_id = s.id
        WHERE s.device_id = $1
        ORDER BY sd.timestamp DESC
        LIMIT $2
        """,
        device_id, limit
    )
    return [SensorDataOut(**dict(row)) for row in rows]


async def delete_sensor_data(conn: asyncpg.Connection, sensor_data_id: str):
    print(f"Deleting sensor data with id: {sensor_data_id}")
    result = await conn.execute(
        """
        DELETE FROM sensor_data
        WHERE id = $1
        """,
        sensor_data_id
    )
    if "DELETE 0" in result:
        return 0  # No rows deleted
    return 1  # Row deleted successfully