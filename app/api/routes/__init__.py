from fastapi import FastAPI
from app.api.routes import tron

def register_routes(app: FastAPI):
    app.include_router(tron.router, prefix="/tron", tags=["tron"])