from __future__ import annotations

from pathlib import Path

import structlog
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from prometheus_fastapi_instrumentator import Instrumentator

from .core.logging import configure_logging
from .core.telemetry import configure_tracing
from .services.sadtalker import service

configure_logging()
configure_tracing("avatar")
logger = structlog.get_logger()

app = FastAPI(title="SadTalker Service", version="0.1.0")


@app.on_event("startup")
async def startup_event() -> None:
    Instrumentator().instrument(app).expose(app)
    logger.info("service.startup", service="avatar")


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/animate")
async def animate(still_image: UploadFile = File(...), audio_wav: UploadFile = File(...)) -> FileResponse:
    image_path = Path(f"/tmp/{still_image.filename}")
    image_path.write_bytes(await still_image.read())
    audio_path = Path(f"/tmp/{audio_wav.filename}")
    audio_path.write_bytes(await audio_wav.read())
    output = service.animate(image_path, audio_path)
    return FileResponse(output)
