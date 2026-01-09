from fastapi import APIRouter

router = APIRouter(
    prefix="/catalog",
    tags=["Catalog"]
)

@router.get("/services")
def get_services():
    return [
        {
            "id": "1",
            "name": "Medical Appointment",
            "prices": {
                "STUDENT": 5,
                "GENERAL": 10
            }
        }
    ]
