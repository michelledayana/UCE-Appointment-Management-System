import time
from fastapi import Request

async def logging_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url.path} - {duration:.3f}s")
    return response
