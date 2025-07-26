from app.models.device import DeviceCreate, DeviceOut
import asyncpg
import uuid
from uuid import UUID

async def create_device(conn: asyncpg.Connection, device: DeviceCreate, current_user: dict):
    device_id = str(uuid.uuid4())
    query = """
        INSERT INTO devices (
            id, company_id, name, model, serial_number,
            location, latitude, longitude, registered_at
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, now())
        RETURNING id, company_id, name, model, serial_number,
                  location, latitude, longitude, registered_at, last_seen
    """

    values = (
        device_id,
        current_user["company_id"],
        device.name,
        device.model,
        device.serial_number,
        device.location,
        device.latitude,
        device.longitude,
    )

    row = await conn.fetchrow(query, *values)
    return DeviceOut(**dict(row))


async def get_devices_by_company(conn: asyncpg.Connection, company_id: UUID):
    rows = await conn.fetch("""
        SELECT * FROM devices WHERE company_id = $1 ORDER BY registered_at DESC
    """, company_id)

    return [DeviceOut(**dict(row)) for row in rows]


async def get_device_by_id(conn: asyncpg.Connection, company_id: UUID, device_id: str):
    row = await conn.fetchrow("""
        SELECT * FROM devices WHERE id = $1 AND company_id = $2
    """, device_id, company_id)

    if not row:
        raise ValueError("Device not found or does not belong to your company")

    return DeviceOut(**dict(row))


async def delete_device(conn: asyncpg.Connection, company_id: UUID, device_id: str):
    result = await conn.execute("""
        DELETE FROM devices WHERE id = $1 AND company_id = $2
    """, device_id, company_id)

    if result != "DELETE 1":
        raise ValueError("Device not found or does not belong to your company")

    return {"message": "Device deleted successfully"}
