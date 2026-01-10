from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.controllers.scheduling_controller import router
from app.websocket.availability_events import websocket_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 SIN prefix aquí
app.include_router(router)
app.include_router(websocket_router)

@app.get("/health")
def health():
    return {"status": "UP"}
