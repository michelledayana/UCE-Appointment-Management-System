from fastapi import FastAPI
from app.api.appointments import router


app = FastAPI(title="Appointment Query Service")


app.include_router(router)


@app.get("/health")
def health():
 return {"status": "ok"}