import threading
from fastapi import FastAPI

from app.database.db import init_db
from app.controllers.auth_controller import router as auth_router
from app.services.kafka_consumer import iniciar_consumidor

app = FastAPI(title="User Authentication Service")

@app.on_event("startup")
def startup_event():
    print("📦 Initializing Auth DB...")
    init_db()

    print("🚀 Starting Kafka Consumer (Auth Service)...")
    thread = threading.Thread(
        target=iniciar_consumidor,
        daemon=True
    )
    thread.start()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "user-authentication-service"
    }
