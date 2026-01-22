from app.schemas.appointment import AppointmentCreate, AppointmentResponse
import uuid

def create_appointment_service(appointment: AppointmentCreate) -> AppointmentResponse:
    # Mock simple: crea un id aleatorio y retorna el objeto
    return AppointmentResponse(
        id=str(uuid.uuid4()),
        user_id=appointment.user_id,
        service_id=appointment.service_id,
        scheduled_at=appointment.scheduled_at
    )
