from fastapi import FastAPI
from app.routes.profile import router as profile_router

app = FastAPI(title="User Profile Service")

app.include_router(profile_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "user-profile-service"}
