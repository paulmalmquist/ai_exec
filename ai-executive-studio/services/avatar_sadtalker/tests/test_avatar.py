from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/healthz").status_code == 200


def test_animate(tmp_path) -> None:
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"FAKE")
    image = tmp_path / "image.png"
    image.write_bytes(b"PNG")
    with audio.open("rb") as audio_fh, image.open("rb") as image_fh:
        response = client.post(
            "/animate",
            files={
                "audio_wav": ("audio.wav", audio_fh, "audio/wav"),
                "still_image": ("image.png", image_fh, "image/png"),
            },
        )
    assert response.status_code == 200
