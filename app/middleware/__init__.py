from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.db_session import DBSessionMiddleware

def register_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(DBSessionMiddleware)
