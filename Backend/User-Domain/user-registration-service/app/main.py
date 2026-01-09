from fastapi import FastAPI
from app.config import settings
from app.controllers.user_controller import router as user_router

# 🔥 IMPORTS REALES SEGÚN TU PROYECTO
from app.database.db import engine, Base
from app.models.user_model import User  # 👈 ESTO REGISTRA LA TABLA

app = FastAPI(title=settings.app_name)

# 🔥 CREA LAS TABLAS
Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/register")

@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": settings.app_name
    }
