from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from sqlalchemy.orm import Session
from app.db.session import AsyncSessionLocal

class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        async with AsyncSessionLocal() as session:
            request.state.db = session
            try:
                response = await call_next(request)
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            return response
