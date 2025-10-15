from __future__ import annotations

import os

import structlog
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .api.routes import router
from .core.config import get_settings
from .core.logging import configure_logging
from .core.telemetry import configure_tracing

configure_logging()
settings = get_settings()
configure_tracing(settings.service_name)
logger = structlog.get_logger()

app = FastAPI(title="AI Executive Orchestrator", version="0.1.0")
app.include_router(router, prefix="")


@app.on_event("startup")
async def startup_event() -> None:
    Instrumentator().instrument(app).expose(app)
    logger.info("service.startup", service=settings.service_name)


@app.on_event("shutdown")
async def shutdown_event() -> None:  # pragma: no cover
    logger.info("service.shutdown", service=settings.service_name)
