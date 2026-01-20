# app/api/appointments.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db  # <- Import correcto
from app.models.appointment import Appointment

router = APIRouter(prefix="/appointments")

# Ejemplo endpoint
@router.get("/")
def read_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()
