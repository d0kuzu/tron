import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import register_routes
from app.middleware import register_middlewares
from app.db.main import init_db, close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("---START---")

    await init_db()
    yield
    await close_db()

    print("---END---")


def create_app() -> FastAPI:
    server = FastAPI(debug=settings.DEBUG_STATUS, lifespan=lifespan)

    register_routes(server)

    register_middlewares(server)

    return server


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s"
)

app = create_app()
