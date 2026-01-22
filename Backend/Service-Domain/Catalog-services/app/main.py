from fastapi import FastAPI

from app.api.rest.catalog import router as catalog_router
from app.api.rest.admin import router as admin_router

app = FastAPI(
    title="Service Catalog Service",
    version="0.1.0"
)

app.include_router(catalog_router)
app.include_router(admin_router)

