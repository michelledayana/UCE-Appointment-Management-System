# app/main.py
import os
from fastapi import FastAPI
from app.api.appointments import router
from app.core.kafka import run_kafka_consumer

app = FastAPI(title="Appointment Management Service")

# Solo iniciar Kafka si RUN_KAFKA != "false"
if os.getenv("RUN_KAFKA", "true") == "true":
    @app.on_event("startup")
    def startup_event():
        run_kafka_consumer()

app.include_router(router)
