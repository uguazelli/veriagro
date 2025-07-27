from app.models.sensor import SensorCreate, SensorOut
import asyncpg
from fastapi import HTTPException
from uuid import UUID, uuid4
import json


async def create_sensor(conn: asyncpg.Connection, sensor: SensorCreate, company_id: UUID) -> SensorOut:
    # Verify device belongs to company
    check = await conn.fetchval(
        "SELECT 1 FROM devices WHERE id = $1 AND company_id = $2",
        sensor.device_id, company_id
    )
    if not check:
        raise HTTPException(status_code=404, detail="Device not found or access denied")

    sensor_id = str(uuid4())
    row = await conn.fetchrow("""
        INSERT INTO sensors (id, device_id, name, type, model, manufacturer, model_id, config)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        RETURNING id, device_id, name, type, model, manufacturer, model_id, config, created_at
    """, sensor_id, sensor.device_id, sensor.name, sensor.type,
         sensor.model, sensor.manufacturer, sensor.model_id,
         json.dumps(sensor.config) if sensor.config else None)

    return SensorOut(**{
        **dict(row),
        "config": json.loads(row["config"]) if row["config"] else None
    })




async def get_sensor_by_id(conn: asyncpg.Connection, sensor_id: UUID, company_id: UUID) -> SensorOut:
    row = await conn.fetchrow("""
        SELECT s.*
        FROM sensors s
        JOIN devices d ON s.device_id = d.id
        WHERE s.id = $1 AND d.company_id = $2
    """, sensor_id, company_id)

    return SensorOut(**dict(row)) if row else None


async def delete_sensor(conn: asyncpg.Connection, sensor_id: UUID, company_id: UUID) -> SensorOut:
    row = await conn.fetchrow("""
        DELETE FROM sensors
        WHERE id = $1 AND device_id IN (
            SELECT id FROM devices WHERE company_id = $2
        )
        RETURNING id, device_id, name, type, model, manufacturer, model_id, config, created_at
    """, sensor_id, company_id)

    return SensorOut(**dict(row)) if row else None


async def get_sensor_by_device_id(conn: asyncpg.Connection, device_id: UUID, company_id: UUID) -> list[SensorOut]:
    # Verifica se o device pertence à empresa
    check = await conn.fetchval("SELECT 1 FROM devices WHERE id = $1 AND company_id = $2", device_id, company_id)
    if not check:
        return []

    rows = await conn.fetch("SELECT * FROM sensors WHERE device_id = $1", device_id)

    result = []
    for row in rows:
        row_dict = dict(row)
        if isinstance(row_dict.get("config"), str):
            try:
                row_dict["config"] = json.loads(row_dict["config"])
            except json.JSONDecodeError:
                row_dict["config"] = None  # ou lance um erro se preferir
        result.append(SensorOut(**row_dict))

    return result
