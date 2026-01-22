import httpx
from app.config import settings

async def login(data: dict):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{settings.AUTH_SERVICE_URL}/auth/login",
            json=data
        )
        return res.json()
