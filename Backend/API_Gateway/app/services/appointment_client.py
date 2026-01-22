import httpx
from app.config import settings

async def create(token: str, data: dict):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{settings.APPOINTMENT_SERVICE_URL}/appointments",
            headers={"Authorization": token},
            json=data
        )
        return res.json()
