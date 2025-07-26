from fastapi import APIRouter, Depends
from app.models.device import DeviceCreate, DeviceOut
from app.crud import device as crud
from app.db import get_db
from app.utils.security import get_current_user

import asyncpg
from typing import List

router = APIRouter()

@router.post("/", response_model=DeviceOut)
async def create_device(
    device: DeviceCreate,
    db: asyncpg.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await crud.create_device(db, device, current_user)


@router.get("/", response_model=List[DeviceOut])
async def list_devices(
    conn: asyncpg.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    List all devices for the current user's company.
    """
    return await crud.get_devices_by_company(conn, current_user["company_id"])


@router.get("/{device_id}", response_model=DeviceOut)
async def get_device(
    device_id: str,
    conn: asyncpg.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific device by ID for the current user's company.
    """
    return await crud.get_device_by_id(conn, current_user["company_id"], device_id)


@router.delete("/{device_id}", response_model=dict)
async def delete_device(
    device_id: str,
    conn: asyncpg.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a specific device by ID for the current user's company.
    """
    return await crud.delete_device(conn, current_user["company_id"], device_id)
