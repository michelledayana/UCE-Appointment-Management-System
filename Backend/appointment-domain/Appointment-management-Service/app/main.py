from fastapi import FastAPI
from app.api.appointments import router as appointment_router
from app.db.database import init_db

app = FastAPI(title="Appointment Management Service")

@app.on_event("startup")
def startup():
    init_db()

app.include_router(appointment_router, prefix="/appointments", tags=["Appointments"])

