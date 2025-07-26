from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class MqttCredentialCreate(BaseModel):
    device_id: UUID
    mqtt_username: str
    mqtt_password_hash: str

class MqttCredentialOut(BaseModel):
    id: UUID
    device_id: UUID
    mqtt_username: str
    created_at: Optional[datetime] = None