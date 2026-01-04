from fastapi import FastAPI
from app.controllers.auth_controller import router

app = FastAPI(
    title="User Authentication Service",
    version="1.0.0"
)

app.include_router(router, prefix="/auth", tags=["Authentication"])
