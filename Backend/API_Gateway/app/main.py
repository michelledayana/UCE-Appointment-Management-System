from fastapi import FastAPI
from app.routes import users

app = FastAPI(
    title="API Gateway",
    description="Central API Gateway for Microservices",
    version="1.0.0"
)

app.include_router(users.router, prefix="/users", tags=["Users"])
