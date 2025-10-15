from __future__ import annotations

from pathlib import Path

import structlog
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from prometheus_fastapi_instrumentator import Instrumentator

from .core.logging import configure_logging
from .core.telemetry import configure_tracing
from .services.composer import composer

configure_logging()
configure_tracing("compositor")
logger = structlog.get_logger()

app = FastAPI(title="Compositor Service", version="0.1.0")


@app.on_event("startup")
async def startup_event() -> None:
    Instrumentator().instrument(app).expose(app)
    logger.info("service.startup", service="compositor")


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/compose")
async def compose(
    foreground: UploadFile = File(...),
    background: UploadFile | None = None,
    captions: UploadFile | None = None,
    theme: str | None = None,
) -> FileResponse:
    fg_path = Path(f"/tmp/{foreground.filename}")
    fg_path.write_bytes(await foreground.read())
    bg_path = None
    if background is not None:
        bg_path = Path(f"/tmp/{background.filename}")
        bg_path.write_bytes(await background.read())
    captions_path = None
    if captions is not None:
        captions_path = Path(f"/tmp/{captions.filename}")
        captions_path.write_bytes(await captions.read())
    output = composer.compose(fg_path, bg_path, captions_path, theme)
    return FileResponse(output)
