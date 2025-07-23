from fastapi import APIRouter, Depends, HTTPException
from app.models.sensor_data import SensorDataCreate
from app.db import get_db
from app.crud import sensor_data as crud
import asyncpg

router = APIRouter()

@router.post("/", status_code=201)
async def create_data(data: SensorDataCreate, conn: asyncpg.Connection = Depends(get_db)):
    return await crud.insert_sensor_data(conn, data)

@router.get("/{sensor_id}")
async def read_data(sensor_id: str, limit: int = 100, conn: asyncpg.Connection = Depends(get_db)):
    return await crud.get_sensor_data(conn, sensor_id, limit)

@router.delete("/{data_id}")
async def delete_data(data_id: int, conn: asyncpg.Connection = Depends(get_db)):
    await crud.delete_sensor_data(conn, data_id)
    return {"message": "Registro de dado deletado com sucesso"}
