from app.models.sensor import SensorCreate
import asyncpg

async def create_sensor(conn: asyncpg.Connection, sensor: SensorCreate):
    row = await conn.fetchrow(
        """
        INSERT INTO sensors (sensor_id, user_id, nome, tipo, modelo, fabricante, unidade)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id, sensor_id, user_id, nome, tipo, modelo, fabricante, unidade, criado_em
        """,
        sensor.sensor_id, sensor.user_id, sensor.nome, sensor.tipo,
        sensor.modelo, sensor.fabricante, sensor.unidade
    )
    return dict(row)

async def get_sensor_by_id(conn: asyncpg.Connection, sensor_id: str):
    row = await conn.fetchrow(
        "SELECT * FROM sensors WHERE sensor_id = $1", sensor_id
    )
    return dict(row) if row else None

async def update_sensor(conn: asyncpg.Connection, sensor_id: str, update_data: dict):
    await conn.execute(
        """
        UPDATE sensors
        SET nome = $1, tipo = $2, modelo = $3, fabricante = $4, unidade = $5
        WHERE sensor_id = $6
        """,
        update_data.get("nome"), update_data.get("tipo"),
        update_data.get("modelo"), update_data.get("fabricante"),
        update_data.get("unidade"), sensor_id
    )

async def delete_sensor(conn: asyncpg.Connection, sensor_id: str):
    await conn.execute(
        "DELETE FROM sensors WHERE sensor_id = $1",
        sensor_id
    )
