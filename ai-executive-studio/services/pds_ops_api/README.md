# AI Executive (PDS Ops) API

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Running
```bash
uvicorn app.main:app --reload --port 8000
```

## Seeding sample data
```bash
python -m app.scripts.seed
```

## Import projects
```bash
curl -u admin:admin -F "file=@data/projects.csv" http://localhost:8000/projects/import
```

JSON import:
```bash
curl -u admin:admin -F "file=@data/projects.json" http://localhost:8000/projects/import-json
```

## Extending connectors
Adapters live in `app/adapters`. Replace the CSV importer with a connector to internal systems; keep mock data out of repo.

## Security note
Never commit proprietary data. Use the `/gaps` endpoint to capture internal data source requirements.
