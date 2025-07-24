from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class SensorDataCreate(BaseModel):
    sensor_id: UUID
    value: float
    unit: Optional[str] = "%"

class SensorDataOut(BaseModel):
    id: UUID
    sensor_id: UUID
    unit: Optional[str]
    value: float
    timestamp: datetime
