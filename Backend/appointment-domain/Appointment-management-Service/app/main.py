from fastapi import FastAPI
from app.api.appointments import router
from app.db.database import Base
from app.db.session import engine
from threading import Thread
from app.core.kafka import start_consumer

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Appointment Management Service")
app.include_router(router)

Thread(target=start_consumer, daemon=True).start()
