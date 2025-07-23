import json
import os
from aiomqtt import Client
from app.models.sensor_data import SensorDataCreate
from app.crud.sensor_data import insert_sensor_data
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = os.getenv("MQTT_PORT", 1883)
TOPIC = os.getenv("TOPIC", "sensor/+/data")

async def mqtt_listener():
    try:
        print("📡 Iniciando listener MQTT com aiomqtt...")

        async with Client(MQTT_BROKER, port=MQTT_PORT) as client:
            await client.subscribe(TOPIC)
            async for message in client.messages:
                try:
                    payload = message.payload.decode()
                    print(f"📨 MQTT recebido: {payload}")
                    data = json.loads(payload)

                    sensor_data = SensorDataCreate(**data)
                    await insert_sensor_data(sensor_data)

                except Exception as e:
                    print(f"❌ Erro ao processar mensagem MQTT: {e}")

    except Exception as conn_err:
        print(f"🚨 Falha ao conectar ao broker MQTT: {conn_err}")
