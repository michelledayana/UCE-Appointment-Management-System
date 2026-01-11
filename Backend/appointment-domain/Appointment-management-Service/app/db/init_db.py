from app.db.database import engine, Base
from app.models.appointment import Appointment

def init_db():
    Base.metadata.create_all(bind=engine)
