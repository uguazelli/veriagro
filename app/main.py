from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from app.db import init_db_pool, close_db_pool
from app.routes import users, sensors, sensor_data
from app.mqtt_subscriber import mqtt_listener

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Iniciando FastAPI com listener MQTT embutido...")

    await init_db_pool()
    task = asyncio.create_task(mqtt_listener())

    yield  # rotas são carregadas aqui

    task.cancel()
    await close_db_pool()
    print("🛑 Listener MQTT encerrado e pool fechado.")

app = FastAPI(
    title="VeriAgro API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(sensors.router, prefix="/sensors", tags=["Sensors"])
app.include_router(sensor_data.router, prefix="/sensor_data", tags=["Sensor Data"])
