import uuid
import asyncpg

from app.models.mqtt_topic import MqttTopicCreate, MqttTopicOut


async def create_mqtt_topic(
    conn: asyncpg.Connection, topic: MqttTopicCreate
) -> MqttTopicOut:
    """
    Create a new MQTT topic in the database.
    """
    query = """
        INSERT INTO mqtt_topics (id, name, device_id)
        VALUES ($1, $2, $3)
        RETURNING id, name, device_id;
    """
    topic_id = str(uuid.uuid4())
    row = await conn.fetchrow(query, topic_id, topic.name, topic.device_id)
    return MqttTopicOut(**row)


async def get_mqtt_topic(
    conn: asyncpg.Connection, topic_id: str
) -> MqttTopicOut:
    """
    Retrieve a specific MQTT topic by its ID.
    """
    query = "SELECT id, name, device_id FROM mqtt_topics WHERE id = $1;"
    row = await conn.fetchrow(query, topic_id)
    if row:
        return MqttTopicOut(**row)
    raise ValueError(f"MQTT topic with ID {topic_id} not found.")


async def get_topics_by_device(
    conn: asyncpg.Connection, device_id: str
) -> list[MqttTopicOut]:
    """
    Retrieve all MQTT topics associated with a specific device.
    """
    query = "SELECT id, name, device_id FROM mqtt_topics WHERE device_id = $1;"
    rows = await conn.fetch(query, device_id)
    return [MqttTopicOut(**row) for row in rows]


async def delete_mqtt_topic(
    conn: asyncpg.Connection, topic_id: str
) -> None:
    """
    Delete a specific MQTT topic by its ID.
    """
    query = "DELETE FROM mqtt_topics WHERE id = $1;"
    result = await conn.execute(query, topic_id)
    if result == "DELETE 0":
        raise ValueError(f"MQTT topic with ID {topic_id} not found.")


