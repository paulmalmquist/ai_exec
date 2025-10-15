from __future__ import annotations

from pathlib import Path

import structlog
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from prometheus_fastapi_instrumentator import Instrumentator

from .core.logging import configure_logging
from .core.telemetry import configure_tracing
from .services.wav2lip import service

configure_logging()
configure_tracing("lipsync")
logger = structlog.get_logger()

app = FastAPI(title="Wav2Lip Service", version="0.1.0")


@app.on_event("startup")
async def startup_event() -> None:
    Instrumentator().instrument(app).expose(app)
    logger.info("service.startup", service="lipsync")


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/lipsync")
async def lipsync(audio_wav: UploadFile = File(...), face_video: UploadFile | None = None, still_image: UploadFile | None = None):
    audio_path = Path(f"/tmp/{audio_wav.filename}")
    audio_path.write_bytes(await audio_wav.read())
    video_path = None
    if face_video is not None:
        video_path = Path(f"/tmp/{face_video.filename}")
        video_path.write_bytes(await face_video.read())
    image_path = None
    if still_image is not None:
        image_path = Path(f"/tmp/{still_image.filename}")
        image_path.write_bytes(await still_image.read())
    output = service.sync(audio_path, video_path, image_path)
    return FileResponse(output)
