from __future__ import annotations

from datetime import datetime, date
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    JSON,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    satisfaction_score = Column(Float, default=0.0)
    pipeline_value = Column(Float, default=0.0)
    strategic_priority = Column(Integer, default=1)

    projects = relationship("Project", back_populates="client")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    region = Column(String, nullable=False)
    sector = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    baseline_budget = Column(Float, default=0.0)
    current_forecast = Column(Float, default=0.0)
    actual_spend = Column(Float, default=0.0)
    baseline_schedule_days = Column(Integer, default=0)
    forecast_schedule_days = Column(Integer, default=0)
    percent_complete = Column(Float, default=0.0)
    safety_incidents = Column(Integer, default=0)
    status = Column(String, default="active")
    last_updated = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="projects")
    risks = relationship("RiskItem", back_populates="project")


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    region = Column(String, nullable=False)
    skill_tags = Column(String, default="")
    utilization_pct = Column(Float, default=0.0)


class RiskItem(Base):
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    category = Column(String, nullable=False)
    probability = Column(Float, default=0.0)
    impact_cost = Column(Float, default=0.0)
    impact_days = Column(Float, default=0.0)
    mitigation_status = Column(String, default="open")

    project = relationship("Project", back_populates="risks")


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    decision_type = Column(String, nullable=False)
    rationale = Column(Text, nullable=False)
    expected_impact_json = Column(JSON, default={})
    status = Column(String, default="proposed")
    owner = Column(String, default="system")
    related_project_ids = Column(JSON, default=[])
    related_risk_ids = Column(JSON, default=[])

    outcomes = relationship("Outcome", back_populates="decision")


class Outcome(Base):
    __tablename__ = "outcomes"

    id = Column(Integer, primary_key=True, index=True)
    decision_id = Column(Integer, ForeignKey("decisions.id"), nullable=False)
    measured_at = Column(DateTime, default=datetime.utcnow)
    kpi_before_json = Column(JSON, default={})
    kpi_after_json = Column(JSON, default={})
    notes = Column(Text, default="")

    decision = relationship("Decision", back_populates="outcomes")


class ProcessTemplate(Base):
    __tablename__ = "process_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    checklist_json = Column(JSON, default=[])
    adoption_rate_pct = Column(Float, default=0.0)


class GapInput(Base):
    __tablename__ = "gap_inputs"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    category = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, default="")
    confidence = Column(Float, default=0.0)
    attachments_meta_json = Column(JSON, default={})


class RuleFeedback(Base):
    __tablename__ = "rule_feedback"

    id = Column(Integer, primary_key=True, index=True)
    rule_key = Column(String, nullable=False, unique=True)
    success_rate = Column(Float, default=0.5)
    updated_at = Column(DateTime, default=datetime.utcnow)
