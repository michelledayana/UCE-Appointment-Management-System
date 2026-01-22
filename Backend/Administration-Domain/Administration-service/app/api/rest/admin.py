from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["Administration"])


@router.get("/health")
def health():
    return {
        "service": "administration-service",
        "status": "ok"
    }
