import uuid
import asyncpg

from app.models.mqtt_topic import MqttTopicCreate


async def create_mqtt_topic(conn: asyncpg.Connection, mqtt_topic: MqttTopicCreate):
    topic_id = str(uuid.uuid4())

    row = await conn.fetchrow("""
        INSERT INTO mqtt_topics (id, device_id, topic, direction, created_at)
        VALUES ($1, $2, $3, $4, now())
        RETURNING *
    """, topic_id, mqtt_topic.device_id, mqtt_topic.topic, mqtt_topic.direction)

    return dict(row)

async def list_mqtt_topics_by_device(conn: asyncpg.Connection, device_id: str):
    rows = await conn.fetch("""
        SELECT * FROM mqtt_topics WHERE device_id = $1
    """, device_id)

    return [dict(row) for row in rows]

async def get_mqtt_topic(conn: asyncpg.Connection, topic_id: str):
    row = await conn.fetchrow("""
        SELECT * FROM mqtt_topics WHERE id = $1
    """, topic_id)

    if row is None:
        raise ValueError("MQTT topic not found")

    return dict(row)

async def delete_mqtt_topic(conn: asyncpg.Connection, topic_id: str):
    result = await conn.execute("""
        DELETE FROM mqtt_topics WHERE id = $1
    """, topic_id)

    if result == "DELETE 0":
        raise ValueError("MQTT topic not found")

    return {"message": "MQTT topic deleted successfully"}