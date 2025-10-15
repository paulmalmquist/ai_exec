# AI Executive Studio

AI Executive Studio is an on-prem focused "video + voice" synthesis monorepo designed to power an executive-grade synthetic media pipeline. It prioritizes open-source tooling, GPU acceleration, observability, and governance controls for enterprise deployments.

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Services](#services)
- [Infra Components](#infra-components)
- [Workflows](#workflows)
- [Local Development](#local-development)
- [GPU & Driver Requirements](#gpu--driver-requirements)
- [Environment Variables](#environment-variables)
- [Security, Governance, and Ethics](#security-governance-and-ethics)
- [Demo Pipeline](#demo-pipeline)
- [Testing](#testing)

## Architecture Overview
The platform is composed of FastAPI microservices, an Angular 20 admin UI, and workflow orchestration via Airflow and n8n. Data persistence spans Postgres (jobs, personas, audit logs), MinIO (media artifacts), Qdrant (RAG embeddings), and Redpanda/Kafka (render pipeline queues). Grafana/Prometheus provide observability, with Langfuse monitoring LLM-driven flows.

```
Persona/Voice/Script Management → Render Orchestrator → (Kafka Queue)
    ↳ TTS (Coqui XTTS v2) → Alignment (MFA) → LipSync (Wav2Lip) → Avatar Motion (SadTalker) → Compositor
                                  ↘ Assets in MinIO ↗                ↗ Background Plates / Branding ↗
```

## Services
Each Python service uses Poetry-managed environments targeting Python 3.12, structlog-based logging, OpenTelemetry exporters, and Prometheus metrics via `prometheus-fastapi-instrumentator`.

| Service | Description |
|---------|-------------|
| `services/orchestrator` | Render job lifecycle, policy gating, LangChain agent routing, JWT auth, Kafka producer integration. |
| `services/tts_xtts` | Coqui XTTS v2 serving, voice registration, speaker embedding persistence, adaptation tooling. |
| `services/alignment` | Montreal Forced Aligner wrapper with phoneme JSON output and graceful degradation. |
| `services/lipsync_wav2lip` | GPU-accelerated Wav2Lip inference for single-image or video lip-syncing. |
| `services/avatar_sadtalker` | SadTalker-based head pose, blink, and expression synthesis. |
| `services/compositor` | FFmpeg/MoviePy-based compositor with watermarking and loudness normalization. |
| `ui-admin` | Angular 20 admin portal for personas, voices, scripts, render queue, and branding. |

## Infra Components
Located under `infra/` for containerized dependencies:

- `postgres/`: initialization SQL for jobs, renders, voices, personas, scripts, assets, audit_logs.
- `minio/`: bucket bootstrap script.
- `qdrant/`: vector store configuration for LangChain/LlamaIndex.
- `grafana/` & `prometheus/`: dashboards and scrapes for GPU metrics, queue lag, and render latency.

## Workflows
- `workflows/airflow`: DAGs for nightly document ingestion, weekly voice integrity checks, and monthly model backups.
- `workflows/n8n`: example flows for Slack and email distribution when renders complete.

## Local Development
1. Ensure [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) is installed for GPU pass-through.
2. Copy `.env.example` to `.env` and update secrets.
3. Build and start the stack:
   ```bash
   make up
   ```
4. Seed databases and sample assets:
   ```bash
   make seed
   ```
5. Run the demo pipeline (requires CUDA-capable GPU):
   ```bash
   ./demo.sh
   ```
6. Access the Angular admin UI at http://localhost:4200.

## GPU & Driver Requirements
- CUDA 12.1+ drivers on host.
- GPU-enabled Docker images for TTS, Wav2Lip, and SadTalker (`nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04`).
- Ensure `--gpus all` is honored in `docker-compose.yml` (requires Docker 20.10+).

## Environment Variables
Environment variables are centralized in `.env.example`. Key values:

- `POSTGRES_*`: connection details.
- `MINIO_*`: credentials and bucket names.
- `QDRANT_URL`, `KAFKA_BROKERS`, `LANGFUSE_*`.
- `JWT_PUBLIC_KEY`, `JWT_PRIVATE_KEY` (PEM).
- `SYNTHETIC_CAPTION_OPT_IN`: toggles on-screen "synthetic media" captions.
- `POLICY_CONFIG_PATH`: path to YAML policy rules.

## Security, Governance, and Ethics
- **Human-in-the-loop**: policy YAML can require approval before external release channels.
- **Audit trails**: all renders log persona, voice, script hashes, and request metadata.
- **Watermarking**: invisible watermark via `imwatermark` plus optional audio watermark stub.
- **Ethical use**: this project is for consensual, disclosed synthetic media. Consult legal counsel before deployment.

## Demo Pipeline
`demo.sh` showcases persona creation, voice registration from sample WAVs, script generation via the orchestrator agent, and render pipeline progression through Kafka topics. The final artifact is stored in MinIO and a signed URL is printed.

## Testing
Each Python service includes pytest suites for health and primary endpoints:

```bash
poetry install
poetry run pytest
```

CI/CD integration can run these tests via the provided Makefile targets or your preferred pipeline.
