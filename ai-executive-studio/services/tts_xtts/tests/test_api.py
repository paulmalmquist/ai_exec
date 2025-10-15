from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200


def test_voice_and_synthesis(tmp_path) -> None:
    response = client.post("/voices", params={"name": "Demo"})
    assert response.status_code == 200
    speaker_id = response.json()["id"]

    synth = client.post("/synthesize", json={"text": "Hello", "speaker_id": speaker_id})
    assert synth.status_code == 200
    data = synth.json()
    assert data["speaker_id"] == speaker_id
