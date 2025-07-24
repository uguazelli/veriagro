from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db
from app.models.sensor import SensorCreate
from app.crud import sensor as crud
import asyncpg

router = APIRouter()

@router.post("/", status_code=201)
async def create_sensor(sensor: SensorCreate, conn: asyncpg.Connection = Depends(get_db)):
    return await crud.create_sensor(conn, sensor)

@router.get("/{sensor_id}")
async def get_sensor(sensor_id: str, conn: asyncpg.Connection = Depends(get_db)):
    sensor = await crud.get_sensor_by_id(conn, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor

@router.delete("/{sensor_id}")
async def delete_sensor(sensor_id: str, conn: asyncpg.Connection = Depends(get_db)):
    sensor = await crud.delete_sensor(conn, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return {"detail": "Sensor deleted successfully"}


@router.get("/device/{device_id}")
async def get_sensor(device_id: str, conn: asyncpg.Connection = Depends(get_db)):
    sensor = await crud.get_sensor_by_device_id(conn, device_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="No sensor not found")
    return sensor
