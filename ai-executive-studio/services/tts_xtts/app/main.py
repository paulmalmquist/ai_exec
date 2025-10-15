from __future__ import annotations

import structlog
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from prometheus_fastapi_instrumentator import Instrumentator

from .api.schemas import SynthesizeRequest, SynthesizeResponse, VoiceCreateResponse
from .core.config import get_settings
from .core.logging import configure_logging
from .core.telemetry import configure_tracing
from .services.tts import registry

configure_logging()
settings = get_settings()
configure_tracing(settings.service_name)
logger = structlog.get_logger()

app = FastAPI(title="XTTS Service", version="0.1.0")


@app.on_event("startup")
async def startup_event() -> None:
    Instrumentator().instrument(app).expose(app)
    logger.info("service.startup", service=settings.service_name)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/voices", response_model=VoiceCreateResponse)
async def create_voice(name: str) -> VoiceCreateResponse:
    speaker_id = registry.register(name)
    return VoiceCreateResponse(id=speaker_id, message="Voice created")


@app.post("/synthesize", response_model=SynthesizeResponse)
async def synthesize(request: SynthesizeRequest) -> SynthesizeResponse:
    audio_path, phonemes = registry.synthesize(request.speaker_id, request.text)
    return SynthesizeResponse(speaker_id=request.speaker_id, audio_url=str(audio_path), phonemes=phonemes)


@app.post("/preview")
async def preview(text: str, speaker_id: str) -> FileResponse:
    audio_path, _ = registry.synthesize(speaker_id, text)
    return FileResponse(audio_path)


@app.post("/voices/upload", response_model=VoiceCreateResponse)
async def upload_voice(file: UploadFile = File(...)) -> VoiceCreateResponse:
    contents = await file.read()
    speaker_id = registry.register(file.filename)
    (registry.speakers_dir / f"{speaker_id}-sample.wav").write_bytes(contents)
    return VoiceCreateResponse(id=speaker_id, message="Voice uploaded")
