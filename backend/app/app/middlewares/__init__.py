from fastapi import FastAPI

from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware


def register_middlewares(app: FastAPI):

    # CORS middleware
    origins = [settings.BACKEND_CORS_ORIGINS]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )