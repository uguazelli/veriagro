from app.models.sensor_data import SensorDataCreate
import asyncpg

async def insert_sensor_data(conn: asyncpg.Connection, data: SensorDataCreate):
    row = await conn.fetchrow(
        """
        INSERT INTO sensor_data (sensor_id, valor, unidade)
        VALUES ($1, $2, $3)
        RETURNING id, sensor_id, valor, unidade, timestamp
        """,
        data.sensor_id, data.valor, data.unidade
    )
    return dict(row)

async def get_sensor_data(conn: asyncpg.Connection, sensor_id: str, limit: int = 100):
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

async def delete_sensor_data(conn: asyncpg.Connection, data_id: int):
    await conn.execute(
        "DELETE FROM sensor_data WHERE id = $1", data_id
    )
