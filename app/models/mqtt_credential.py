#app/models/mqtt_credential.py
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class MqttCredentialCreate(BaseModel):
    device_id: UUID
    mqtt_username: str
    mqtt_password_hash: str


class MqttCredentialOut(BaseModel):
    id: UUID
    device_id: UUID
    mqtt_username: str
    mqtt_password_hash: str
    created_at: Optional[datetime] = None