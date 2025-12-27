from __future__ import annotations

import json
from pathlib import Path
from sqlalchemy.orm import Session

from app.models.models import Client, RiskItem, Resource, ProcessTemplate

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def seed_clients(db: Session):
    clients = json.loads((DATA_DIR / "clients.json").read_text())
    for item in clients:
        db.merge(Client(**item))
    db.commit()


def seed_risks(db: Session):
    risks = json.loads((DATA_DIR / "risks.json").read_text())
    for item in risks:
        db.add(RiskItem(**item))
    db.commit()


def seed_resources(db: Session):
    resources = json.loads((DATA_DIR / "resources.json").read_text())
    for item in resources:
        db.add(Resource(**item))
    db.commit()


def seed_templates(db: Session):
    templates = [
        ProcessTemplate(
            name="Schedule Recovery Playbook",
            description="Checklist for schedule recovery and variance control.",
            checklist_json=[
                "Daily schedule variance review",
                "Critical path analysis",
                "Client escalation triggers",
            ],
            adoption_rate_pct=0.45,
        )
    ]
    for template in templates:
        db.add(template)
    db.commit()
