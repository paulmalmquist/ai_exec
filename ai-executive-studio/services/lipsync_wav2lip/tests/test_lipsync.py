from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/healthz").status_code == 200


def test_lipsync(tmp_path) -> None:
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"FAKE")
    with audio.open("rb") as fh:
        response = client.post("/lipsync", files={"audio_wav": ("audio.wav", fh, "audio/wav")})
    assert response.status_code == 200
