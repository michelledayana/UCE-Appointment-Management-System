from fastapi import FastAPI
from app.api.rest.admin import router as admin_router

app = FastAPI(title="Administration Service")

app.include_router(admin_router)
