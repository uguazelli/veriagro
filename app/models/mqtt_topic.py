#app/models/mqtt_topic.py
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class MqttTopicCreate(BaseModel):
    topic: str
    device_id: UUID
    direction: Optional[str] = 'publish'

class MqttTopicOut(BaseModel):
    id: UUID
    device_id: UUID
    topic: str
    direction: Optional[str] = 'publish'
    created_at: Optional[datetime]

