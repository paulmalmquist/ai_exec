#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
ROOT_DIR=$(cd "$SCRIPT_DIR/.." && pwd)

source "$ROOT_DIR/.env" 2>/dev/null || echo "Using environment defaults."

psql "postgresql://${POSTGRES_USER:-ai_executive}:${POSTGRES_PASSWORD:-ai_executive}@${POSTGRES_HOST:-localhost}:${POSTGRES_PORT:-5432}/${POSTGRES_DB:-ai_executive}" -f "$ROOT_DIR/infra/postgres/init.sql" || echo "Postgres seed skipped."

python "$ROOT_DIR/services/orchestrator/tools/seed_policy.py" || echo "Policy seed skipped."

mc alias set local ${MINIO_ENDPOINT:-http://localhost:9000} ${MINIO_ACCESS_KEY:-ai-executive} ${MINIO_SECRET_KEY:-ai-executive-secret} >/dev/null 2>&1 || echo "MinIO client configuration skipped."
mc mb --ignore-existing local/${MINIO_BUCKET_MEDIA:-media} >/dev/null 2>&1 || echo "MinIO bucket ensured."
