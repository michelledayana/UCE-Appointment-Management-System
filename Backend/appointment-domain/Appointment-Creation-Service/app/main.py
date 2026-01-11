from fastapi import FastAPI
from app.api.appointments import router
from app.mqtt.mqtt_client import connect_mqtt

app = FastAPI(title="Appointment Creation Service")

@app.on_event("startup")
def startup_event():
    connect_mqtt()  # si falla → solo log

app.include_router(router)
