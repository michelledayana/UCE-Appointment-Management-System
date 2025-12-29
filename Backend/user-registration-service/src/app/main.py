from fastapi import FastAPI
from app.controllers.user_controller import router

app = FastAPI(
    title="User Registration Service",
    version="1.0.0"
)

app.include_router(router)
