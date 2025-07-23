from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorCreate(BaseModel):
    sensor_id: str
    user_id: int
    nome: Optional[str]
    tipo: Optional[str]
    modelo: Optional[str]
    fabricante: Optional[str]
    unidade: Optional[str] = "%"

class SensorOut(BaseModel):
    id: int
    sensor_id: str
    user_id: int
    nome: Optional[str]
    tipo: Optional[str]
    modelo: Optional[str]
    fabricante: Optional[str]
    unidade: Optional[str]
    criado_em: datetime
