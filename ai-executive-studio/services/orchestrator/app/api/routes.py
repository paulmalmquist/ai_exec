from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from ..core.auth import JWTDependency
from ..models.schemas import (
    HealthResponse,
    PersonaRequest,
    PersonaResponse,
    RenderRequest,
    RenderResponse,
    RenderStatus,
    ScriptRequest,
    ScriptResponse,
    VoiceRequest,
    VoiceResponse,
)
from ..services.agent import get_agent
from ..services.policy import load_policy_rules, requires_approval
from ..services.store import MemoryStore, get_store

router = APIRouter()


@router.get("/healthz", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/readyz", response_model=HealthResponse)
async def ready() -> HealthResponse:
    return HealthResponse(status="ready")


@router.post("/persona", response_model=PersonaResponse)
async def create_persona(payload: PersonaRequest, store: MemoryStore = Depends(get_store), user: JWTDependency | None = None) -> PersonaResponse:  # noqa: B008
    return store.create_persona(payload)


@router.post("/voice", response_model=VoiceResponse)
async def register_voice(payload: VoiceRequest, store: MemoryStore = Depends(get_store), user: JWTDependency | None = None) -> VoiceResponse:  # noqa: B008
    return store.create_voice(payload)


@router.post("/script", response_model=ScriptResponse)
async def save_script(payload: ScriptRequest, store: MemoryStore = Depends(get_store), user: JWTDependency | None = None) -> ScriptResponse:  # noqa: B008
    return store.create_script(payload)


@router.post("/render", response_model=RenderResponse)
async def create_render(
    payload: RenderRequest,
    store: MemoryStore = Depends(get_store),
    user: JWTDependency | None = None,
):  # noqa: B008
    rules = load_policy_rules()
    approval = requires_approval(payload.channel, rules)
    render = store.create_render(payload, approval)
    if not approval:
        agent = get_agent()
        await agent.route_pipeline(render.id)
        store.update_render(render.id, status=RenderStatus.running, artifacts={"final_video": "s3://demo"})
    return store.renders[render.id]


@router.get("/render/{render_id}", response_model=RenderResponse)
async def get_render(render_id: str, store: MemoryStore = Depends(get_store), user: JWTDependency | None = None) -> RenderResponse:  # noqa: B008
    if render_id not in store.renders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Render not found")
    return store.renders[render_id]
