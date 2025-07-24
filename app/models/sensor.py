from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class SensorCreate(BaseModel):
    device_id: UUID
    name: Optional[str]
    type: Optional[str]
    model: Optional[str]
    manufacturer: Optional[str]

class SensorOut(BaseModel):
    id: UUID
    device_id: UUID
    name: Optional[str]
    type: Optional[str]
    model: Optional[str]
    manufacturer: Optional[str]
    created_at: datetime
