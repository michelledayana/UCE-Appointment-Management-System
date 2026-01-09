from app.schemas.schedule_schema import ScheduleCreate, ScheduleResponse
import uuid
import logging

logger = logging.getLogger(__name__)

class ScheduleService:

    def create_schedule(self, data: ScheduleCreate) -> ScheduleResponse:
        logger.info("Creating schedule slot")

        return ScheduleResponse(
            id=str(uuid.uuid4()),
            service_id=data.service_id,
            date=data.date,
            time_slot=data.time_slot,
            available=True
        )
