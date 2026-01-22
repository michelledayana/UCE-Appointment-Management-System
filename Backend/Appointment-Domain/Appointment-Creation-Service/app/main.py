from fastapi import FastAPI
from app.api.appointments import router as appointments_router

app = FastAPI(title="Appointment Creation Service")

# Incluimos router
app.include_router(appointments_router, prefix="/appointments")
