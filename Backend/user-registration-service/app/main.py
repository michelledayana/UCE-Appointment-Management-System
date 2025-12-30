from fastapi import FastAPI
from app.controllers.user_controller import router

app = FastAPI(title="User Registration Service")

app.include_router(router)
