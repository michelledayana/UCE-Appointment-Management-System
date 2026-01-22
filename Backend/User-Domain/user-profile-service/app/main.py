from fastapi import FastAPI
from threading import Thread
import time
import logging

from app.db.database import Base, engine
from app.routes.profile import router as profile_router
from app.services.kafka_consumer import consume_user_registered

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="User Profile Service")

app.include_router(profile_router)


def init_db():
    retries = 10
    delay = 3

    for attempt in range(retries):
        try:
            logging.info("📦 Initializing database...")
            Base.metadata.create_all(bind=engine)
            logging.info("✅ Database initialized successfully")
            return
        except Exception as e:
            logging.warning(
                f"⏳ Database not ready (attempt {attempt + 1}/{retries}): {e}"
            )
            time.sleep(delay)

    raise Exception("Database connection failed")


@app.on_event("startup")
def startup_event():
    init_db()
    Thread(target=consume_user_registered, daemon=True).start()
    logging.info("🚀 Kafka consumer started")
