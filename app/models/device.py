from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class DeviceCreate(BaseModel):
    name: str
    model: Optional[str]
    serial_number: Optional[str]
    location: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

class DeviceOut(BaseModel):
    id: UUID
    company_id: UUID
    name: str
    model: Optional[str]
    serial_number: Optional[str]
    location: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    last_seen: Optional[datetime]
    registered_at: Optional[datetime]