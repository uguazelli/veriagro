from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class SensorModelCreate(BaseModel):
    type: str
    model: str
    manufacturer: Optional[str]
    unit: Optional[str]

class SensorModelOut(BaseModel):
    id: UUID
    type: str
    model: str
    manufacturer: Optional[str]
    unit: Optional[str]