from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/healthz").status_code == 200


def test_align(monkeypatch, tmp_path) -> None:
    wav_path = tmp_path / "sample.wav"
    wav_path.write_bytes(b"FAKE")
    with wav_path.open("rb") as fh:
        response = client.post("/align", data={"transcript": "hello world"}, files={"wav": ("sample.wav", fh, "audio/wav")})
    assert response.status_code == 200
    assert "alignment" in response.json()
