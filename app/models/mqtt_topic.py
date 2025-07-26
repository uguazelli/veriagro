from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class MqttTopicCreate(BaseModel):
    device_id: UUID
    topic: str
    direction: str

class MqttTopicOut(BaseModel):
    id: UUID
    device_id: UUID
    topic: str
    direction: str
    created_at: Optional[datetime] = None