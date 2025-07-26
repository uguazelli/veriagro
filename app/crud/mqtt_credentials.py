import uuid
import asyncpg
from app.utils.security import hash_password
from app.models.mqtt_credential import MqttCredentialCreate, MqttCredentialOut


async def create_mqtt_credential(conn: asyncpg.Connection, mqtt_credential: MqttCredentialCreate):
    credential_id = str(uuid.uuid4())
    hashed_password = hash_password(mqtt_credential.mqtt_password_hash)

    row = await conn.fetchrow("""
        INSERT INTO mqtt_credentials (id, device_id, mqtt_username, mqtt_password_hash, created_at)
        VALUES ($1, $2, $3, $4, now())
        RETURNING id, device_id, mqtt_username, mqtt_password_hash, created_at
    """, credential_id, mqtt_credential.device_id, mqtt_credential.mqtt_username, hashed_password)
    return MqttCredentialOut(**dict(row))



async def get_mqtt_credential(conn: asyncpg.Connection, credential_id: str):
    row = await conn.fetchrow("""
        SELECT id, device_id, mqtt_username, mqtt_password_hash, created_at
        FROM mqtt_credentials
        WHERE id = $1
    """, credential_id)

    if row is None:
        return None

    return MqttCredentialOut(**dict(row))



async def get_mqtt_credentials_by_device(conn: asyncpg.Connection, device_id: str):
    rows = await conn.fetch("""
        SELECT id, device_id, mqtt_username, mqtt_password_hash, created_at
        FROM mqtt_credentials
        WHERE device_id = $1
    """, device_id)

    return [MqttCredentialOut(**dict(row)) for row in rows]



async def delete_mqtt_credential(conn: asyncpg.Connection, credential_id: str):
    result = await conn.execute("""
        DELETE FROM mqtt_credentials
        WHERE id = $1
    """, credential_id)

    if result == "DELETE 0":
        raise ValueError("MQTT credential not found")

    return {"message": "MQTT credential deleted successfully"}