from fastapi import FastAPI
import asyncio
import logging

from app.consumers.availability_consumer import consume_availability_events

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Availability Validation Service",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_availability_events())

@app.get("/health")
def health_check():
    return {"status": "ok"}
