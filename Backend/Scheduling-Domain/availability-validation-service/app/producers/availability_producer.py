import logging

logger = logging.getLogger(__name__)

def publish_validation_result(service_id: str, available: bool):
    logger.info(
        f"📤 Publishing validation result → service={service_id}, available={available}"
    )
