from fastapi import FastAPI
from app.config import settings

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

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(profile_router, prefix="/profiles", tags=["Profiles"])
app.include_router(catalog_router, prefix="/catalog", tags=["Catalog"])
app.include_router(scheduling_router, prefix="/scheduling", tags=["Scheduling"])
app.include_router(appointment_router, prefix="/appointments", tags=["Appointments"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
