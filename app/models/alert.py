from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class AlertCreate(BaseModel):
    sensor_id: UUID
    value: float
    level: str
    message: str

class AlertOut(BaseModel):
    id: UUID
    sensor_id: UUID
    value: float
    level: str
    message: str
    timestamp: Optional[datetime]