import asyncpg
from fastapi import APIRouter, Depends
from app.crud import mqtt_credentials as crud
from app.db import get_db
from app.models.mqtt_credential import MqttCredentialCreate, MqttCredentialOut


router = APIRouter()

@router.post("/", status_code=201)
async def create_mqtt_credential(mqtt_credential: MqttCredentialCreate, conn: asyncpg.Connection = Depends(get_db)):
    return await crud.create_mqtt_credential(conn, mqtt_credential)


@router.get("/{credential_id}", response_model=MqttCredentialOut)
async def get_mqtt_credential(credential_id: str, conn: asyncpg.Connection = Depends(get_db)):
    return await crud.get_mqtt_credential(conn, credential_id)


@router.get("/device/{device_id}", response_model=list[MqttCredentialOut])
async def get_mqtt_credentials_by_device(device_id: str, conn: asyncpg.Connection = Depends(get_db)):
    return await crud.get_mqtt_credentials_by_device(conn, device_id)


@router.delete("/{credential_id}", status_code=204)
async def delete_mqtt_credential(credential_id: str, conn: asyncpg.Connection = Depends(get_db)):
    await crud.delete_mqtt_credential(conn, credential_id)
    return {"message": "MQTT credential deleted successfully"}