from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.connection_manager import ConnectionManager
import logging

logger = logging.getLogger(__name__)

websocket_router = APIRouter()
manager = ConnectionManager()

@websocket_router.websocket("/ws/availability")
async def availability_socket(websocket: WebSocket):
    await manager.connect(websocket)
    logger.info("Availability service connected")

    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Availability event received: {data}")

            # simulate validation
            response = {
                "event": "availability_response",
                "service_id": data["service_id"],
                "available": True
            }

            await websocket.send_json(response)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.warning("Availability service disconnected")
