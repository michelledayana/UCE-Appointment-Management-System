from fastapi import FastAPI
import time
import logging

from app.config import settings
from app.controllers.user_controller import router as user_router
from app.database.db import engine, Base
from app.models.user_model import User  # registra tablas

logging.basicConfig(level=logging.INFO)

app = FastAPI(title=settings.app_name)

app.include_router(user_router)


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

    logging.error("❌ Database could not be initialized")
    raise Exception("Database connection failed")


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": settings.app_name
    }
