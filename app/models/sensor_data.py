from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorDataCreate(BaseModel):
    sensor_id: str
    valor: float
    unidade: Optional[str] = "%"

class SensorDataOut(BaseModel):
    id: int
    sensor_id: str
    valor: float
    unidade: Optional[str]
    timestamp: datetime
