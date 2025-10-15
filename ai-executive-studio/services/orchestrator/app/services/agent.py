from __future__ import annotations

from typing import Any

import structlog

try:  # pragma: no cover - optional dependency wiring
    from langfuse import Langfuse

    langfuse_client = Langfuse()
except Exception:  # pragma: no cover - keep service running without Langfuse
    langfuse_client = None

logger = structlog.get_logger()


class OrchestratorAgent:
    def __init__(self) -> None:
        self.prompt_templates = {
            "confident_analytical": "You are a confident, analytical executive willing to argue for the best path forward."
        }

    async def rag_search(self, query: str) -> dict[str, Any]:
        logger.info("agent.rag_search", query=query)
        if langfuse_client:
            langfuse_client.trace(name="rag_search", input=query)
        return {"results": [f"Insight for {query}"]}

    async def make_script(self, context: str, tone: str, audience: str) -> str:
        logger.info("agent.make_script", tone=tone, audience=audience)
        prompt = self.prompt_templates["confident_analytical"]
        result = f"{prompt} Context: {context}. Tone: {tone}. Audience: {audience}."
        if langfuse_client:
            langfuse_client.trace(name="make_script", input=context, output=result)
        return result

    async def route_pipeline(self, render_job_id: str) -> dict[str, Any]:
        logger.info("agent.route_pipeline", job_id=render_job_id)
        if langfuse_client:
            langfuse_client.trace(name="route_pipeline", output=render_job_id)
        return {"job_id": render_job_id, "enqueued": ["tts", "align", "lipsync", "avatar", "compose"]}


def get_agent() -> OrchestratorAgent:
    return OrchestratorAgent()
