from __future__ import annotations

from io import StringIO
import json
import pandas as pd
from sqlalchemy.orm import Session

from app.models.models import Project


def _project_from_dict(payload: dict) -> Project:
    return Project(
        client_id=int(payload["client_id"]),
        region=payload["region"],
        sector=payload["sector"],
        start_date=pd.to_datetime(payload["start_date"]).date(),
        end_date=pd.to_datetime(payload["end_date"]).date(),
        baseline_budget=float(payload["baseline_budget"]),
        current_forecast=float(payload["current_forecast"]),
        actual_spend=float(payload["actual_spend"]),
        baseline_schedule_days=int(payload["baseline_schedule_days"]),
        forecast_schedule_days=int(payload["forecast_schedule_days"]),
        percent_complete=float(payload["percent_complete"]),
        safety_incidents=int(payload["safety_incidents"]),
        status=payload.get("status", "active"),
    )


def import_projects_from_csv(content: str, db: Session) -> list[Project]:
    df = pd.read_csv(StringIO(content))
    projects = []
    for _, row in df.iterrows():
        project = _project_from_dict(row.to_dict())
        projects.append(project)
        db.add(project)
    db.commit()
    return projects


def import_projects_from_json(content: str, db: Session) -> list[Project]:
    data = json.loads(content)
    projects = []
    for payload in data:
        project = _project_from_dict(payload)
        projects.append(project)
        db.add(project)
    db.commit()
    return projects
