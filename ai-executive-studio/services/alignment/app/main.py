from __future__ import annotations

from pathlib import Path

import structlog
from fastapi import FastAPI, UploadFile
from prometheus_fastapi_instrumentator import Instrumentator

from .core.logging import configure_logging
from .core.telemetry import configure_tracing
from .services.aligner import aligner

configure_logging()
configure_tracing("alignment")
logger = structlog.get_logger()

app = FastAPI(title="Alignment Service", version="0.1.0")


@app.on_event("startup")
async def startup_event() -> None:
    Instrumentator().instrument(app).expose(app)
    logger.info("service.startup", service="alignment")


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/align")
async def align(transcript: str, wav: UploadFile) -> dict[str, object]:
    temp_path = Path(f"/tmp/{wav.filename}")
    temp_path.write_bytes(await wav.read())
    result = aligner.align(transcript, temp_path)
    return {"alignment": result}
