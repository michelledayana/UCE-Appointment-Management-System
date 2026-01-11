from fastapi import APIRouter, Request
from app.utils.proxy import proxy_request
from app.config import SERVICES

router = APIRouter()

@router.post("/schedules")
async def create_schedule(request: Request):
    return proxy_request(
        request,
        f"{SERVICES['scheduling']}/schedules/schedules/"
    )

@router.get("/health")
async def availability_health(request: Request):
    return proxy_request(
        request,
        f"{SERVICES['availability']}/health"
    )
