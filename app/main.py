import asyncio
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.db import init_db_pool, close_db_pool
from app.routes import mqtt_topics, users, sensors, sensor_data, devices, admin, mqtt_credentials, companies
from app.mqtt_subscriber import mqtt_listener
from app.routes import frontend
from fastapi.staticfiles import StaticFiles
from app.utils.security import get_current_user

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Iniciando FastAPI com listener MQTT embutido...")

    await init_db_pool()
    task = asyncio.create_task(mqtt_listener())

    yield  # rotas são carregadas aqui

    task.cancel()
    await close_db_pool()
    print("🛑 Listener MQTT encerrado e pool fechado.")

app = FastAPI( title="VeriAgro API", version="1.0.0", lifespan=lifespan )

# Allow frontend (e.g., React running at localhost:8000) to access your backend
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],              # Allow all HTTP methods
    allow_headers=["*"],              # Allow all headers
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(frontend.router, tags=["Frontend"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

app.include_router(companies.router, prefix="/companies", tags=["Companies"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(devices.router, prefix="/devices", dependencies=[Depends(get_current_user)], tags=["Devices"])
app.include_router(sensors.router, prefix="/sensors", dependencies=[Depends(get_current_user)], tags=["Sensors"])
app.include_router(sensor_data.router, prefix="/sensor_data", dependencies=[Depends(get_current_user)], tags=["Sensor Data"])
app.include_router(mqtt_topics.router, prefix="/topics", dependencies=[Depends(get_current_user)], tags=["Topics"])
app.include_router(mqtt_credentials.router, prefix="/mqtt_credential", dependencies=[Depends(get_current_user)], tags=["MQTT Credential"])
