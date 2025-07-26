# app/routes/topics.py
import asyncpg
from fastapi import APIRouter, Depends
from app.crud import mqtt_topic as crud
from app.db import get_db
from app.models.mqtt_topic import MqttTopicCreate, MqttTopicOut


router = APIRouter()

@router.post("/", response_model=MqttTopicOut, status_code=201)
async def create_topic(topic: MqttTopicCreate, db: asyncpg.Connection = Depends(get_db)):
    """
    Create a new MQTT topic.
    """
    return await crud.create_topic(db, topic)



@router.get("/device/{device_id}", response_model=list[MqttTopicOut])
async def get_topics_by_device(device_id: str, conn: asyncpg.Connection = Depends(get_db)):
    """Get all MQTT topics for a specific device.
    """
    return await crud.get_topics_by_device(conn, device_id)



@router.get("/{topic_id}", response_model=MqttTopicOut)
async def get_mqtt_topic(topic_id: str, conn: asyncpg.Connection = Depends(get_db)):
    """Get a specific MQTT topic by its ID.
    """
    return await crud.get_mqtt_topic(conn, topic_id)



@router.delete("/{topic_id}", status_code=204)
async def delete_mqtt_topic(topic_id: str, conn: asyncpg.Connection = Depends(get_db)):
    """Delete a specific MQTT topic by its ID.
    """
    await crud.delete_mqtt_topic(conn, topic_id)
    return {"message": "Topic deleted successfully."}
