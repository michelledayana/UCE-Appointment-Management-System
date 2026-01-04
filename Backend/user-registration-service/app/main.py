import uvicorn
from fastapi import FastAPI
from app.controllers.user_controller import router as user_router

app = FastAPI(title="User Registration Service")

app.include_router(user_router, prefix="/users", tags=["Users"])

# 🔹 Health check para AWS / NLB
@app.get("/health")
def health():
    return {"status": "UP"}

# 🔹 Root simple
@app.get("/")
def root():
    return {"service": "User Registration Service"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8081
    )
