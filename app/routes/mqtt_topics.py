# app/routes/topics.py
import asyncpg
from fastapi import APIRouter, Depends
from app.crud import mqtt_topic as crud
from app.db import get_db
from app.models.mqtt_topic import MqttTopicCreate, MqttTopicOut
from app.utils.security import get_current_user
from fastapi import HTTPException
from typing import List

router = APIRouter()


@router.post("/", response_model=MqttTopicOut)
async def create_topic(
    topic: MqttTopicCreate,
    conn: asyncpg.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    print("currrent_user: ${current_user}")
    return await crud.create_topic(conn, topic, current_user["company_id"])



@router.get("/device/{device_id}", response_model=List[MqttTopicOut])
async def get_topic_by_device(device_id: str, conn: asyncpg.Connection = Depends(get_db)):
    result = await crud.get_topics_by_device(conn, device_id)
    return result


