# app/routes/devices.py
from fastapi import APIRouter, Depends
from app.models.device import DeviceCreate, DeviceOut
from app.crud import device as crud
from app.db import get_db
from app.utils.security import get_current_user

import asyncpg
from typing import List

router = APIRouter()

@router.post("/", response_model=DeviceOut, status_code=201)
async def register_device(
    device: DeviceCreate,
    conn: asyncpg.Connection = Depends(get_db),
    user = Depends(get_current_user)
):
    return await crud.create_device(conn, user["id"], device)

@router.get("/", response_model=List[DeviceOut])
async def list_devices(
    conn: asyncpg.Connection = Depends(get_db),
    user = Depends(get_current_user)
):
    return await crud.get_devices_by_user(conn, user["id"])

@router.get("/{device_id}", response_model=DeviceOut)
async def get_device(
    device_id: str,
    conn: asyncpg.Connection = Depends(get_db),
    user = Depends(get_current_user)
):
    return await crud.get_device_by_id(conn, user["id"], device_id)


@router.delete("/{device_id}", status_code=204)
async def delete_device(
    device_id: str,
    conn: asyncpg.Connection = Depends(get_db),
    user = Depends(get_current_user)
):
    await crud.delete_device(conn, user["id"], device_id)
    return {"message": "Device deleted successfully"}