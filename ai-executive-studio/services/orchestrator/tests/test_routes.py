from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_persona() -> None:
    payload = {
        "name": "Avery",
        "style_guidelines": "Confident",
        "argumentation_level": "high",
        "risk_posture": "medium",
    }
    response = client.post("/persona", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Avery"
    assert "summary" in body


def test_render_pipeline() -> None:
    persona = client.post(
        "/persona",
        json={"name": "Persona", "style_guidelines": "", "argumentation_level": "medium", "risk_posture": "low"},
    ).json()
    voice = client.post("/voice", json={"name": "Voice"}).json()
    script = client.post(
        "/script",
        json={"persona_id": persona["id"], "text": "Hello", "tone": "confident"},
    ).json()
    render_resp = client.post(
        "/render",
        json={
            "persona_id": persona["id"],
            "voice_id": voice["id"],
            "script_id": script["id"],
            "avatar_id": "avatar",
            "layout": {"background": "studio"},
            "channel": "internal",
        },
    )
    assert render_resp.status_code == 200
    render = render_resp.json()
    assert render["status"] in {"queued", "running", "awaiting_approval"}
    fetch = client.get(f"/render/{render['id']}")
    assert fetch.status_code == 200
