from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from app.database.db import engine, Base
from app.models.user_model import User
import time

from app.config import settings
from app.controllers.user_controller import router as user_router

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Init DB
    retries = 10
    delay = 3
    for attempt in range(retries):
        try:
            logging.info("📦 Initializing database...")
            Base.metadata.create_all(bind=engine)
            logging.info("✅ Database initialized successfully")
            break
        except Exception as e:
            logging.warning(
                f"⏳ Database not ready (attempt {attempt + 1}/{retries}): {e}"
            )
            time.sleep(delay)
    else:
        logging.error("❌ Database could not be initialized")
        raise Exception("Database connection failed")

    yield  # Aquí empieza la vida del app

app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(user_router)

@app.get("/health")
def health():
    return {"status": "UP", "service": settings.app_name}
