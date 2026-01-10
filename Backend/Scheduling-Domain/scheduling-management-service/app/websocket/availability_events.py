from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.connection_manager import ConnectionManager
import logging
import asyncio

logger = logging.getLogger(__name__)

websocket_router = APIRouter()
manager = ConnectionManager()

@websocket_router.websocket("/ws/availability")
async def availability_socket(websocket: WebSocket):
    await manager.connect(websocket)
    logger.info("🟢 WebSocket client connected")

    try:
        while True:
            # Keep connection alive (no request-response)
            await asyncio.sleep(10)

            event = {
                "event": "availability_update",
                "service_id": "dentistry",
                "available": True
            }

            await manager.broadcast(event)
            logger.info(" Availability event sent")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.warning(" WebSocket client disconnected")
