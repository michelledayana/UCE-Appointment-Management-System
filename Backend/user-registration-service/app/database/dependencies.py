from app.database.db import SessionLocal
from fastapi import HTTPException, status

def get_db():
    if SessionLocal is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
