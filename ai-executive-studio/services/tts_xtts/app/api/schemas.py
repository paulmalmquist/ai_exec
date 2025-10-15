from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class VoiceCreateResponse(BaseModel):
    id: str
    message: str


class SynthesizeRequest(BaseModel):
    text: str
    speaker_id: str
    prosody: dict[str, Any] | None = None


class SynthesizeResponse(BaseModel):
    speaker_id: str
    audio_url: str
    phonemes: dict[str, Any] | None = None
