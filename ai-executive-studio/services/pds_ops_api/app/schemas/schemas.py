from __future__ import annotations

from datetime import date, datetime
from typing import Any, List, Optional
from pydantic import BaseModel, Field


class ClientBase(BaseModel):
    name: str
    satisfaction_score: float = 0.0
    pipeline_value: float = 0.0
    strategic_priority: int = 1


class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: int

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    client_id: int
    region: str
    sector: str
    start_date: date
    end_date: date
    baseline_budget: float = 0.0
    current_forecast: float = 0.0
    actual_spend: float = 0.0
    baseline_schedule_days: int = 0
    forecast_schedule_days: int = 0
    percent_complete: float = 0.0
    safety_incidents: int = 0
    status: str = "active"
    last_updated: Optional[datetime] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int

    class Config:
        from_attributes = True


class ResourceBase(BaseModel):
    name: str
    role: str
    region: str
    skill_tags: str = ""
    utilization_pct: float = 0.0


class ResourceCreate(ResourceBase):
    pass


class ResourceRead(ResourceBase):
    id: int

    class Config:
        from_attributes = True


class RiskBase(BaseModel):
    project_id: int
    category: str
    probability: float = 0.0
    impact_cost: float = 0.0
    impact_days: float = 0.0
    mitigation_status: str = "open"


class RiskCreate(RiskBase):
    pass


class RiskRead(RiskBase):
    id: int

    class Config:
        from_attributes = True


class DecisionBase(BaseModel):
    decision_type: str
    rationale: str
    expected_impact_json: dict[str, Any] = Field(default_factory=dict)
    status: str = "proposed"
    owner: str = "system"
    related_project_ids: List[int] = Field(default_factory=list)
    related_risk_ids: List[int] = Field(default_factory=list)


class DecisionCreate(DecisionBase):
    pass


class DecisionRead(DecisionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class OutcomeBase(BaseModel):
    decision_id: int
    kpi_before_json: dict[str, Any] = Field(default_factory=dict)
    kpi_after_json: dict[str, Any] = Field(default_factory=dict)
    notes: str = ""


class OutcomeCreate(OutcomeBase):
    pass


class OutcomeRead(OutcomeBase):
    id: int
    measured_at: datetime

    class Config:
        from_attributes = True


class ProcessTemplateBase(BaseModel):
    name: str
    description: str = ""
    checklist_json: list[Any] = Field(default_factory=list)
    adoption_rate_pct: float = 0.0


class ProcessTemplateCreate(ProcessTemplateBase):
    pass


class ProcessTemplateRead(ProcessTemplateBase):
    id: int

    class Config:
        from_attributes = True


class GapInputBase(BaseModel):
    category: str
    question: str
    answer: str = ""
    confidence: float = 0.0
    attachments_meta_json: dict[str, Any] = Field(default_factory=dict)


class GapInputCreate(GapInputBase):
    pass


class GapInputRead(GapInputBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RuleFeedbackBase(BaseModel):
    rule_key: str
    success_rate: float = 0.5


class RuleFeedbackRead(RuleFeedbackBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True


class KPIResult(BaseModel):
    project_id: int
    ev: float
    ac: float
    pv: float
    cv: float
    sv: float
    cpi: float
    spi: float


class PortfolioKPIResponse(BaseModel):
    kpis: list[KPIResult]
    totals: dict[str, float]


class ScenarioResult(BaseModel):
    project_id: int
    p50_cost: float
    p80_cost: float
    p50_days: float
    p80_days: float
    iterations: int


class RecommendationRead(BaseModel):
    decision_type: str
    affected_project_ids: list[int]
    expected_impact: dict[str, Any]
    explanation: str
    confidence: float


class ExecutiveBrief(BaseModel):
    summary: str
    markdown: str
    metrics: dict[str, Any]
    recommendations: list[RecommendationRead]
