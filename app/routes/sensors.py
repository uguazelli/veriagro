from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db
from app.models.sensor import SensorCreate, SensorOut
from app.crud import sensor as crud
import asyncpg

router = APIRouter()

@router.post("/", response_model=SensorOut)
async def create_sensor(sensor: SensorCreate, conn: asyncpg.Connection = Depends(get_db)):
    created_sensor = await crud.create_sensor(conn, sensor)
    if not created_sensor:
        raise HTTPException(status_code=400, detail="Failed to create sensor")
    return created_sensor

@router.get("/{sensor_id}")
async def get_sensor(sensor_id: str, conn: asyncpg.Connection = Depends(get_db)):
    sensor = await crud.get_sensor_by_id(conn, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor

@router.delete("/{sensor_id}")
async def delete_sensor(sensor_id: str, conn: asyncpg.Connection = Depends(get_db)):
    deleted_sensor = await crud.delete_sensor(conn, sensor_id)
    if not deleted_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return {"detail": "Sensor deleted successfully", "sensor": deleted_sensor}


@router.get("/device/{device_id}")
async def get_sensor(device_id: str, conn: asyncpg.Connection = Depends(get_db)):
    sensors = await crud.get_sensor_by_device_id(conn, device_id)
    if not sensors:
        raise HTTPException(status_code=404, detail="No sensors found for this device")
    return sensors
