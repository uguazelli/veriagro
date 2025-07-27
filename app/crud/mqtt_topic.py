from uuid import UUID, uuid4
import asyncpg
from app.models.mqtt_topic import MqttTopicCreate, MqttTopicOut
from fastapi import HTTPException
import json



async def create_topic(conn: asyncpg.Connection, topic: MqttTopicCreate, company_id: UUID) -> MqttTopicOut:
    # Verify device belongs to company
    check = await conn.fetchval(
        "SELECT 1 FROM devices WHERE id = $1 AND company_id = $2",
        topic.device_id, company_id
    )
    if not check:
        raise HTTPException(status_code=404, detail="Device not found or access denied")

    topic_id = str(uuid4())
    row = await conn.fetchrow("""
        INSERT INTO public.mqtt_topics (id, device_id, topic, direction)
        VALUES ($1, $2, $3, $4)
        RETURNING id, device_id, topic, direction, created_at
    """, topic_id, topic.device_id, topic.topic, topic.direction)

    return MqttTopicOut(**dict(row))


async def get_topics_by_device(conn: asyncpg.Connection, device_id: str) -> list[MqttTopicOut]:
    rows = await conn.fetch("""
        SELECT id, device_id, topic, direction, created_at
        FROM public.mqtt_topics
        WHERE device_id = $1
    """, device_id)

    return [MqttTopicOut(**dict(r)) for r in rows]
