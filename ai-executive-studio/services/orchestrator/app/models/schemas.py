from __future__ import annotations

from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class PersonaRequest(BaseModel):
    name: str
    style_guidelines: str | None = None
    argumentation_level: Literal['low', 'medium', 'high'] | str | None = None
    risk_posture: Literal['low', 'medium', 'high'] | str | None = None


class PersonaResponse(PersonaRequest):
    id: str
    summary: str


class VoiceRequest(BaseModel):
    name: str
    description: str | None = None
    cloning_method: str | None = None


class VoiceResponse(VoiceRequest):
    id: str
    message: str = "Voice registered"


class ScriptRequest(BaseModel):
    persona_id: str
    text: str
    tone: str | None = None
    metadata: dict[str, Any] | None = None


class ScriptResponse(BaseModel):
    id: str
    persona_id: str
    text: str
    tone: str | None = None


class LayoutOptions(BaseModel):
    background: str | None = None
    lower_third: str | None = None
    caption: bool | None = None


class RenderRequest(BaseModel):
    persona_id: str
    voice_id: str
    script_id: str
    avatar_id: str
    layout: LayoutOptions = Field(default_factory=LayoutOptions)
    channel: str | None = None


class RenderStatus(str, Enum):
    pending = "pending"
    queued = "queued"
    running = "running"
    awaiting_approval = "awaiting_approval"
    complete = "complete"


class RenderResponse(BaseModel):
    id: str
    status: RenderStatus
    artifacts: dict[str, Any]
    approval_required: bool = False


class HealthResponse(BaseModel):
    status: str


class PolicyRule(BaseModel):
    channel: str
    requires_approval: bool = False
