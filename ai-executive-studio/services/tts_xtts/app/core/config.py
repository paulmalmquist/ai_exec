from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    service_name: str = "tts_xtts"
    postgres_dsn: str = os.getenv("POSTGRES_DSN", "postgresql://ai_executive:ai_executive@postgres:5432/ai_executive")
    minio_endpoint: str = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
    minio_bucket: str = os.getenv("MINIO_BUCKET_MEDIA", "media")
    jwt_public_key: str = os.getenv("JWT_PUBLIC_KEY", "")
    speaker_config_dir: Path = Path(os.getenv("SPEAKER_CONFIG_DIR", "/data/speakers"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
