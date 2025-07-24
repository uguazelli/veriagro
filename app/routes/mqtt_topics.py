# app/routes/topics.py
import asyncpg
from fastapi import APIRouter, Depends
from app.crud import mqtt_topic as crud
from app.db import get_db
from app.models.mqtt_topic import MqttTopicCreate, MqttTopicOut


router = APIRouter()

@router.post("/", status_code=201)
async def create_mqtt_topic(mqtt_topic: MqttTopicCreate, conn: asyncpg.Connection = Depends(get_db)):
    return await crud.create_mqtt_topic(conn, mqtt_topic)


@router.get("/device/{device_id}", response_model=list[MqttTopicOut])
async def list_mqtt_topics_by_device(device_id: str, conn: asyncpg.Connection = Depends(get_db)):
    return await crud.list_mqtt_topics_by_device(conn, device_id)


@router.get("/{topic_id}", response_model=MqttTopicOut)
async def get_mqtt_topic(topic_id: str, conn: asyncpg.Connection = Depends(get_db)):
    return await crud.get_mqtt_topic(conn, topic_id)


@router.delete("/{topic_id}", status_code=204)
async def delete_mqtt_topic(topic_id: str, conn: asyncpg.Connection = Depends(get_db)):
    await crud.delete_mqtt_topic(conn, topic_id)
    return {"message": "MQTT topic deleted successfully"}