from fastapi import APIRouter, Depends, HTTPException
from app.models.sensor_data import SensorDataIn, SensorDataOut
from app.db import get_db
from app.crud import sensor_data as crud
import asyncpg

router = APIRouter()

@router.post("/", status_code=201)
async def create_sensor_data(
    sensor_data: SensorDataIn, conn: asyncpg.Connection = Depends(get_db)
):
    try:
        return await crud.create_sensor_data(conn, sensor_data)
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=400, detail="Sensor data already exists")


@router.get("/sensor/{sensor_id}")
async def get_sensor_data_by_sensor(
    sensor_id: str, limit: int = 1000, conn: asyncpg.Connection = Depends(get_db)
):
    return await crud.get_sensor_data_by_sensor(conn, sensor_id, limit)


@router.get("/device/{device_id}")
async def get_sensor_data_by_device(
    device_id: str, limit: int = 1000, conn: asyncpg.Connection = Depends(get_db)
):
    return await crud.get_sensor_data_by_device(conn, device_id, limit)



@router.delete("/{sensor_data_id}")
async def delete_sensor_data(
    sensor_data_id: str, conn: asyncpg.Connection = Depends(get_db)
):
    deleted_count = await crud.delete_sensor_data(conn, sensor_data_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sensor data not found")
    return {"detail": "Sensor data deleted successfully"}
