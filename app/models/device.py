# app/models/device.py
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class DeviceCreate(BaseModel):
    name: str
    model: Optional[str]
    serial_number: Optional[str]

class DeviceOut(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    model: Optional[str]
    serial_number: Optional[str]
    last_seen: Optional[datetime]
    registered_at: datetime
