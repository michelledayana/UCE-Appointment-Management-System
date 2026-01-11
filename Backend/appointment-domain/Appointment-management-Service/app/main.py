from fastapi import FastAPI
from app.api.appointments import router

app = FastAPI(title="Appointment Management Service")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}