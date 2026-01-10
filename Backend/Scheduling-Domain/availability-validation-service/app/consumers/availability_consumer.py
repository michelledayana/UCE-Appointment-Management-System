import asyncio
import logging
from app.services.validation_service import validate_availability

logger = logging.getLogger(__name__)

async def consume_availability_events():
    """
    Simulated consumer loop
    """
    await asyncio.sleep(5)

    # 🔥 Evento simulado
    event = {
        "event": "availability_update",
        "service_id": "dentistry"
    }

    logger.info(f"📥 Event received: {event}")

    result = validate_availability(event["service_id"])

    logger.info(f"🧪 Validation result: {result}")
