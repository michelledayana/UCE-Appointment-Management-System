from app.database.mongo import audit_collection
from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["Administration"])

@router.get("/health")
def health():
    return {"status": "Administration Service OK"}