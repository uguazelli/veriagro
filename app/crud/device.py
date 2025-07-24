# app/crud/device.py
from app.models.device import DeviceCreate
from app.utils.security import hash_password
import asyncpg
import uuid
from uuid import UUID

async def create_device(conn: asyncpg.Connection, user_id: UUID, device: DeviceCreate):
    device_id = str(uuid.uuid4())

    row = await conn.fetchrow("""
        INSERT INTO devices (id, user_id, name, model, serial_number, registered_at)
        VALUES ($1, $2, $3, $4, $5, now())
        RETURNING *
    """, device_id, user_id, device.name, device.model, device.serial_number)

    return dict(row)

async def get_devices_by_user(conn: asyncpg.Connection, user_id: int):
    rows = await conn.fetch("SELECT * FROM devices WHERE user_id = $1", user_id)
    return [dict(r) for r in rows]


async def delete_device(conn: asyncpg.Connection, user_id: UUID, device_id: str):
    result = await conn.execute("""
        DELETE FROM devices WHERE id = $1 AND user_id = $2
    """, device_id, user_id)

    if result == "DELETE 0":
        raise ValueError("Device not found or does not belong to the user")

    return {"message": "Device deleted successfully"}


async def get_device_by_id(conn: asyncpg.Connection, user_id: UUID, device_id: str):
    row = await conn.fetchrow("""
        SELECT * FROM devices WHERE id = $1 AND user_id = $2
    """, device_id, user_id)

    if not row:
        raise ValueError("Device not found or does not belong to the user")

    return dict(row)