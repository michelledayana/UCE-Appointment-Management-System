from fastapi import FastAPI
from app.config.settings import settings
from app.routes.appointments import router as appointment_router

app = FastAPI(title=settings.SERVICE_NAME)

app.include_router(appointment_router)


@app.get("/appointments/health")
def health():
    return {"service": settings.SERVICE_NAME, "status": "ok"}
