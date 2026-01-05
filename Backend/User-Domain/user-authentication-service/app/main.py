from fastapi import FastAPI
from app.controllers.auth_controller import router as auth_router

app = FastAPI(title="User Authentication Service")

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

@app.get("/health")
def health():
    return {"status": "UP"}
