from fastapi import APIRouter, Depends, HTTPException
from app.models.sensor_data import SensorDataIn, SensorDataOut
from app.db import get_db
from app.crud import sensor_data as crud
from app.utils.security import get_current_user
import asyncpg
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=SensorDataOut)
async def create_sensor_data(
    sensor_data: SensorDataIn,
    conn: asyncpg.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await crud.create_sensor_data(conn, sensor_data, current_user["company_id"])


@router.get("/sensor/{sensor_id}", response_model=list[SensorDataOut])
async def get_sensor_data_by_sensor(
    sensor_id: UUID,
    limit: int = 1000,
    conn: asyncpg.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await crud.get_sensor_data_by_sensor(conn, sensor_id, limit, current_user["company_id"])


@router.get("/device/{device_id}", response_model=list[SensorDataOut])
async def get_sensor_data_by_device(
    device_id: UUID,
    limit: int = 1000,
    conn: asyncpg.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await crud.get_sensor_data_by_device(conn, device_id, limit, current_user["company_id"])


@router.delete("/{sensor_data_id}")
async def delete_sensor_data(
    sensor_data_id: UUID,
    conn: asyncpg.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    deleted_count = await crud.delete_sensor_data(conn, sensor_data_id, current_user["company_id"])
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sensor data not found or not owned by your company")
    return {"detail": "Sensor data deleted successfully"}
