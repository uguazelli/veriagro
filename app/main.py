import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import mqtt_credentials
from app.db import init_db_pool, close_db_pool
from app.routes import mqtt_topics, users, sensors, sensor_data, devices
from app.mqtt_subscriber import mqtt_listener
from app.routes import frontend
from fastapi.staticfiles import StaticFiles
from app.routes import admin

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

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(frontend.router, tags=["Frontend"])

app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(sensors.router, prefix="/sensors", tags=["Sensors"])
app.include_router(sensor_data.router, prefix="/sensor_data", tags=["Sensor Data"])
app.include_router(devices.router, prefix="/devices", tags=["Devices"])
app.include_router(mqtt_topics.router, prefix="/topics", tags=["Topics"])
app.include_router(mqtt_credentials.router, prefix="/mqtt_credential", tags=["MQTT Credential"])
