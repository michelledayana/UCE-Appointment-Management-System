
from fastapi import APIRouter
from fastapi import APIRouter
from app.schemas.schedule_schema import ScheduleCreate, ScheduleResponse
from app.services.schedule_service import create_schedule

router = APIRouter(
    prefix="/schedules",
    tags=["Schedules"]
)


@router.post("/", response_model=ScheduleResponse)
def create(schedule: ScheduleCreate):
    return create_schedule(schedule)
