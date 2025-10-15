from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Dict

from ..models.schemas import LayoutOptions, PersonaRequest, PersonaResponse, RenderRequest, RenderResponse, RenderStatus, ScriptRequest, ScriptResponse, VoiceRequest, VoiceResponse


@dataclass
class MemoryStore:
    personas: Dict[str, PersonaResponse] = field(default_factory=dict)
    voices: Dict[str, VoiceResponse] = field(default_factory=dict)
    scripts: Dict[str, ScriptResponse] = field(default_factory=dict)
    renders: Dict[str, RenderResponse] = field(default_factory=dict)

    def create_persona(self, payload: PersonaRequest) -> PersonaResponse:
        persona_id = str(uuid.uuid4())
        summary = (
            f"Persona {payload.name} configured with tone {payload.argumentation_level or 'balanced'}"
        )
        persona = PersonaResponse(id=persona_id, summary=summary, **payload.model_dump())
        self.personas[persona_id] = persona
        return persona

    def create_voice(self, payload: VoiceRequest) -> VoiceResponse:
        voice_id = str(uuid.uuid4())
        voice = VoiceResponse(id=voice_id, **payload.model_dump())
        self.voices[voice_id] = voice
        return voice

    def create_script(self, payload: ScriptRequest) -> ScriptResponse:
        script_id = str(uuid.uuid4())
        script = ScriptResponse(id=script_id, **payload.model_dump())
        self.scripts[script_id] = script
        return script

    def create_render(self, payload: RenderRequest, approval_required: bool) -> RenderResponse:
        render_id = str(uuid.uuid4())
        status = RenderStatus.awaiting_approval if approval_required else RenderStatus.queued
        artifacts: Dict[str, Any] = {"final_video": None}
        render = RenderResponse(id=render_id, status=status, artifacts=artifacts, approval_required=approval_required)
        self.renders[render_id] = render
        return render

    def update_render(self, render_id: str, *, status: RenderStatus, artifacts: Dict[str, Any]) -> RenderResponse:
        render = self.renders[render_id]
        updated = render.model_copy(update={"status": status, "artifacts": artifacts})
        self.renders[render_id] = updated
        return updated


def get_store() -> MemoryStore:
    return MemoryStore()
