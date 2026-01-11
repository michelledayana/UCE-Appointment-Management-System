from fastapi import FastAPI
from app.controllers.auth_controller import router as auth_router
from app.services.kafka_consumer import iniciar_consumidor
from app.database.db import init_db
import threading

app = FastAPI()

app.include_router(auth_router)

@app.on_event("startup")
def startup_event():
    # 🔥 CREA TABLAS
    init_db()

    # 🔥 INICIA KAFKA
    thread = threading.Thread(
        target=iniciar_consumidor,
        daemon=True
    )
    thread.start()
