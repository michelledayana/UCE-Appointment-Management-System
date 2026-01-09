from fastapi import FastAPI
from threading import Thread

from app.db.database import Base, engine
from app.routes.profile import router as profile_router
from app.services.kafka_consumer import consume_user_registered

app = FastAPI(title="User Profile Service")

Base.metadata.create_all(bind=engine)

app.include_router(profile_router)


@app.on_event("startup")
def start_kafka_consumer():
    Thread(target=consume_user_registered, daemon=True).start()
