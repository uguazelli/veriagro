from app.models.sensor_data import SensorDataIn, SensorDataOut
import asyncpg
import uuid
from uuid import UUID

async def create_sensor_data(conn: asyncpg.Connection, data: SensorDataIn, company_id: UUID):
    # Security: Validate that sensor belongs to company via device
    row = await conn.fetchrow("""
        SELECT s.id
        FROM sensors s
        JOIN devices d ON s.device_id = d.id
        WHERE s.id = $1 AND d.company_id = $2
    """, data.sensor_id, company_id)

    if not row:
        raise Exception("Sensor does not belong to your company")

    row = await conn.fetchrow(
        """
        INSERT INTO sensor_data (id, sensor_id, unit, value, status)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, sensor_id, unit, value, status, timestamp
        """,
        uuid.uuid4(), data.sensor_id, data.unit, data.value, data.status
    )
    return SensorDataOut(**dict(row))


async def get_sensor_data_by_device(conn: asyncpg.Connection, device_id: UUID, limit: int, company_id: UUID):
    # Security check: device must belong to current user's company
    authorized = await conn.fetchval("""
        SELECT 1 FROM devices
        WHERE id = $1 AND company_id = $2
    """, device_id, company_id)

    if not authorized:
        raise Exception("Device does not belong to your company")

    # Fetch sensor data for the device
    rows = await conn.fetch("""
        SELECT sd.id, sd.sensor_id, sd.unit, sd.value, sd.status, sd.timestamp
        FROM sensor_data sd
        JOIN sensors s ON sd.sensor_id = s.id
        WHERE s.device_id = $1
        ORDER BY sd.timestamp DESC
        LIMIT $2
    """, device_id, limit)

    return [SensorDataOut(**dict(row)) for row in rows]



async def get_sensor_data_by_sensor(conn: asyncpg.Connection, sensor_id: UUID, limit: int, company_id: UUID):
    rows = await conn.fetch(
        """
        SELECT sd.id, sd.sensor_id, sd.unit, sd.value, sd.status, sd.timestamp
        FROM sensor_data sd
        JOIN sensors s ON sd.sensor_id = s.id
        JOIN devices d ON s.device_id = d.id
        WHERE s.id = $1 AND d.company_id = $2
        ORDER BY sd.timestamp DESC
        LIMIT $3
        """,
        sensor_id, company_id, limit
    )
    return [SensorDataOut(**dict(row)) for row in rows]


async def delete_sensor_data(conn: asyncpg.Connection, sensor_data_id: UUID, company_id: UUID):
    # Validate ownership before deletion
    row = await conn.fetchrow(
        """
        SELECT sd.id
        FROM sensor_data sd
        JOIN sensors s ON sd.sensor_id = s.id
        JOIN devices d ON s.device_id = d.id
        WHERE sd.id = $1 AND d.company_id = $2
        """,
        sensor_data_id, company_id
    )

    if not row:
        return 0

    await conn.execute(
        """
        DELETE FROM sensor_data
        WHERE id = $1
        """,
        sensor_data_id
    )
    return 1
