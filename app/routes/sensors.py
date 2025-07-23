from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db
from app.models.sensor import SensorCreate
from app.crud import sensor as crud
import asyncpg

router = APIRouter()

@router.post("/", status_code=201)
async def create(sensor: SensorCreate, conn: asyncpg.Connection = Depends(get_db)):
    return await crud.create_sensor(conn, sensor)

@router.get("/{sensor_id}")
async def read(sensor_id: str, conn: asyncpg.Connection = Depends(get_db)):
    sensor = await crud.get_sensor_by_id(conn, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor não encontrado")
    return sensor

@router.put("/{sensor_id}")
async def update(sensor_id: str, update: dict, conn: asyncpg.Connection = Depends(get_db)):
    await crud.update_sensor(conn, sensor_id, update)
    return {"message": "Sensor atualizado com sucesso"}

@router.delete("/{sensor_id}")
async def delete(sensor_id: str, conn: asyncpg.Connection = Depends(get_db)):
    await crud.delete_sensor(conn, sensor_id)
    return {"message": "Sensor deletado com sucesso"}
