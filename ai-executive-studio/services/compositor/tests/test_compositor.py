from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/healthz").status_code == 200


def test_compose(tmp_path) -> None:
    foreground = tmp_path / "fg.mp4"
    foreground.write_bytes(b"FAKE")
    with foreground.open("rb") as fh:
        response = client.post("/compose", files={"foreground": ("fg.mp4", fh, "video/mp4")})
    assert response.status_code == 200
