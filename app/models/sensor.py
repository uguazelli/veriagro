from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Dict

class SensorCreate(BaseModel):
    device_id: UUID
    name: Optional[str]
    type: Optional[str]
    model: Optional[str]
    manufacturer: Optional[str]
    model_id: Optional[UUID]
    config: Optional[Dict]

class SensorOut(BaseModel):
    id: UUID
    device_id: UUID
    name: Optional[str]
    type: Optional[str]
    model: Optional[str]
    manufacturer: Optional[str]
    model_id: Optional[UUID]
    config: Optional[Dict]
    created_at: Optional[datetime]