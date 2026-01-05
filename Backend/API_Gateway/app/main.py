from fastapi import FastAPI
from app.middlewares.auth_middleware import auth_middleware
from app.middlewares.logging import logging_middleware
from app.routes import auth, users, appointments

app = FastAPI(title="API Gateway")

app.middleware("http")(logging_middleware)
app.middleware("http")(auth_middleware)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(appointments.router)
