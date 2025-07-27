from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db
from app.models.sensor import SensorCreate, SensorOut
from app.crud import sensor as crud
from app.utils.security import get_current_user
import asyncpg
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=SensorOut)
async def create_sensor(
    sensor: SensorCreate,
    conn: asyncpg.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await crud.create_sensor(conn, sensor, current_user["company_id"])


@router.get("/{sensor_id}", response_model=SensorOut)
async def get_sensor(
    sensor_id: UUID,
    conn: asyncpg.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    sensor = await crud.get_sensor_by_id(conn, sensor_id, current_user["company_id"])
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found or access denied")
    return sensor


@router.delete("/{sensor_id}")
async def delete_sensor(
    sensor_id: UUID,
    conn: asyncpg.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    deleted_sensor = await crud.delete_sensor(conn, sensor_id, current_user["company_id"])
    if not deleted_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found or access denied")
    return {"detail": "Sensor deleted successfully", "sensor": deleted_sensor}


@router.get("/device/{device_id}", response_model=list[SensorOut])
async def get_sensor_by_device(
    device_id: UUID,
    conn: asyncpg.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await crud.get_sensor_by_device_id(conn, device_id, current_user["company_id"])
