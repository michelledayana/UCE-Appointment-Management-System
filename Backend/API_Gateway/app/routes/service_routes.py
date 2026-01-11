from fastapi import APIRouter, Request, HTTPException
from app.utils.proxy import proxy_request
from app.config import SERVICES

router = APIRouter()

# PUBLIC
@router.get("/catalog/services")
async def list_services(request: Request):
    return proxy_request(
        request,
        f"{SERVICES['service_catalog']}/catalog/services"
    )

# ADMIN
@router.post("/admin/catalog/services")
@router.put("/admin/catalog/services/{service_id}")
@router.delete("/admin/catalog/services/{service_id}")
async def admin_services(request: Request, service_id: str = None):
    user = request.state.user
    if user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin only")

    path = request.url.path.replace("/admin", "")
    return proxy_request(
        request,
        f"{SERVICES['service_catalog']}{path}"
    )