from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.middlewares.auth_middleware import auth_middleware
from app.middlewares.logging import logging_middleware

from app.routes import (
    auth_router,
    users_router,
    profile_router,
    catalog_router,
    scheduling_router,
    appointment_router,
    admin_router,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
)

# ✅ CONFIGURAR CORS (CRÍTICO)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ AGREGAR MIDDLEWARES
@app.middleware("http")
async def add_logging_middleware(request, call_next):
    return await logging_middleware(request, call_next)

@app.middleware("http")
async def add_auth_middleware(request, call_next):
    return await auth_middleware(request, call_next)

# ✅ INCLUIR ROUTERS (SIN /api)
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(profile_router, prefix="/profiles", tags=["Profiles"])
app.include_router(catalog_router, prefix="/catalog", tags=["Catalog"])
app.include_router(scheduling_router, prefix="/scheduling", tags=["Scheduling"])
app.include_router(appointment_router, prefix="/appointments", tags=["Appointments"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])

# Health check
@app.get("/health")
def health():
    return {"status": "healthy"}