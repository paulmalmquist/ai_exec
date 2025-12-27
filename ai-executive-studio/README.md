# AI Executive (PDS Ops)

This repo provides a full MVP for an executive decision intelligence loop inspired by operational leadership patterns (portfolio optimization, risk/scenario planning, standardization, real-time visibility, client-centric adaptation, and talent/knowledge management). It uses mock/sample data only and is designed to connect to internal systems later.

## Architecture
- **Backend**: FastAPI + SQLAlchemy + Pydantic v2 (SQLite by default, optional MS SQL Server via pyodbc)
- **Frontend**: React + TypeScript + Vite
- **Engine**: transparent analytics + recommendation rules in `services/pds_ops_api/app/engine`

## Local setup
```bash
cp .env.example .env
docker compose up --build
```

Optional MS SQL Server profile:
```bash
docker compose --profile mssql up --build
```

Then open:
- API: http://localhost:8000/docs
- UI: http://localhost:5173

## Sample data
Seed the database with mock data:
```bash
docker compose exec api python -m app.scripts.seed
curl -u admin:admin -F "file=@services/pds_ops_api/data/projects.csv" http://localhost:8000/projects/import
```

## Import data
- CSV: `POST /projects/import`
- JSON: `POST /projects/import-json`

Sample data files live in `services/pds_ops_api/data` and contain **only mock data**.

## Database configuration
SQLite is the default. To use MS SQL Server, set:
```
DATABASE_URL=mssql+pyodbc://sa:${MSSQL_SA_PASSWORD}@mssql:1433/master?driver=ODBC+Driver+18+for+SQL+Server
```

## Executive loop capabilities
- **KPI calculation**: EVM metrics (EV, AC, PV, CV, SV, CPI, SPI)
- **Portfolio ranking**: attention scoring based on risks, variance, client priority, safety
- **Scenario planning**: Monte Carlo with what-if toggles
- **Recommendations**: rule-based decisions with explainable triggers
- **Feedback loop**: record outcomes and adjust rule confidence
- **Gap capture**: front-end wizard stores missing data/access details without embedding proprietary data

## Extending connectors
Adapters are in `services/pds_ops_api/app/adapters`. Replace the CSV/JSON mock importers with connectors to internal project management and finance systems.

## Security note
Keep proprietary data out of the repo. Use the Gap Capture page to capture internal data source requirements.
