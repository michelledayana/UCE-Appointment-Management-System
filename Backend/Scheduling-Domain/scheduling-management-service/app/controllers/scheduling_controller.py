from fastapi import APIRouter, Depends
from app.schemas.schedule_schema import ScheduleCreate, ScheduleResponse
from app.services.schedule_service import ScheduleService

router = APIRouter()

@router.post("/", response_model=ScheduleResponse)
def create_schedule(data: ScheduleCreate):
    service = ScheduleService()
    return service.create_schedule(data)
