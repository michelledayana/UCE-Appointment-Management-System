from fastapi import FastAPI
from app.api.rest.admin import router as admin_router
from app.api.rest.catalog import router as catalog_router

app = FastAPI(title="Catalog Service")

# 👇 ESTO ES OBLIGATORIO
app.include_router(catalog_router)
app.include_router(admin_router)
