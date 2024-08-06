from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import os

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.getenv("API_KEY"):
            raise HTTPException(status_code=403, detail="Could not validate API Key")
        response = await call_next(request)
        return response
