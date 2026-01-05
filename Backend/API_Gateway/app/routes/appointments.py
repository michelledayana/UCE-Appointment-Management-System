from fastapi import APIRouter, Request, Depends
from app.security.dependencies import require_role
from app.services.appointment_client import create

router = APIRouter(prefix="/appointments")

@router.post("/")
async def create_appointment(
    request: Request,
    data: dict,
    _: None = Depends(require_role("student"))
):
    token = request.headers.get("Authorization")
    return await create(token, data)
