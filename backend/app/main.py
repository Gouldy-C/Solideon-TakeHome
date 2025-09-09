import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import init_db
from app.utils.config_loader import init_load
from pathlib import Path
from app.routers import (
    groups,
    layers,
    ingest
)


def create_app() -> FastAPI:
    app = FastAPI(title="AM Spatial Sensing Analytics API")
    init_db()
    init_load(Path(__file__).parent / "config/v0.1")

    frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(groups.router)
    app.include_router(layers.router)
    app.include_router(ingest.router)
    return app


app = create_app()