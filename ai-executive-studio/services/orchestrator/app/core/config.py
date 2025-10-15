from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import BaseModel


class Settings(BaseModel):
    service_name: str = os.getenv("SERVICE_NAME", "orchestrator")
    postgres_dsn: str = os.getenv("POSTGRES_DSN", "postgresql://ai_executive:ai_executive@postgres:5432/ai_executive")
    minio_endpoint: str = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
    minio_bucket: str = os.getenv("MINIO_BUCKET_MEDIA", "media")
    kafka_brokers: str = os.getenv("KAFKA_BROKERS", "redpanda:9092")
    policy_path: Path = Path(os.getenv("POLICY_CONFIG_PATH", "/app/config/policies.yaml"))
    jwt_public_key: str = os.getenv("JWT_PUBLIC_KEY", "")
    synthetic_caption_opt_in: bool = os.getenv("SYNTHETIC_CAPTION_OPT_IN", "true").lower() == "true"

    class Config:
        arbitrary_types_allowed = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    import yaml

    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}
