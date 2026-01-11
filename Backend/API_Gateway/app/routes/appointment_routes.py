from fastapi import APIRouter, Request
from app.utils.proxy import proxy_request
from app.config import SERVICES

router = APIRouter()

@router.post("/appointments")
async def create_appointment(request: Request):
    return proxy_request(
        request,
        f"{SERVICES['appointment_create']}/appointments"
    )

@router.get("/appointments")
@router.get("/appointments/{appointment_id}")
@router.patch("/appointments/{appointment_id}")
async def appointment_ops(request: Request, appointment_id: str = None):
    path = request.url.path
    return proxy_request(
        request,
        f"{SERVICES['appointment_view']}{path}"
    )
