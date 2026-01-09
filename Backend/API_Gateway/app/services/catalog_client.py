import httpx
from app.config import settings

async def get_services(user_role: str = "GENERAL"):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{settings.CATALOG_SERVICE_URL}/services",
            headers={"x-user-role": user_role}
        )
        return res.json()

async def create_service(data: dict, user_role: str):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{settings.CATALOG_SERVICE_URL}/admin/services",
            json=data,
            headers={"x-user-role": user_role}
        )
        return res.json()

async def get_all_services(user_role: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{settings.CATALOG_SERVICE_URL}/admin/services",
            headers={"x-user-role": user_role}
        )
        return res.json()

async def get_service_by_id(service_id: str, user_role: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{settings.CATALOG_SERVICE_URL}/admin/services/{service_id}",
            headers={"x-user-role": user_role}
        )
        return res.json()

async def update_service(service_id: str, data: dict, user_role: str):
    async with httpx.AsyncClient() as client:
        res = await client.put(
            f"{settings.CATALOG_SERVICE_URL}/admin/services/{service_id}",
            json=data,
            headers={"x-user-role": user_role}
        )
        return res.json()

async def disable_service(service_id: str, user_role: str):
    async with httpx.AsyncClient() as client:
        res = await client.patch(
            f"{settings.CATALOG_SERVICE_URL}/admin/services/{service_id}/disable",
            headers={"x-user-role": user_role}
        )
        return res.json()

async def delete_service(service_id: str, user_role: str):
    async with httpx.AsyncClient() as client:
        res = await client.delete(
            f"{settings.CATALOG_SERVICE_URL}/admin/services/{service_id}",
            headers={"x-user-role": user_role}
        )
        return res.json()

