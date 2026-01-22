import httpx
from app.config import settings

async def register(data: dict):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{settings.USER_REGISTRATION_URL}/users/register",
            json=data
        )
        return res.json()
