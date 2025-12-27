from __future__ import annotations

from datetime import datetime
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, auth_guard
from app.models.models import (
    Project,
    Client,
    Resource,
    RiskItem,
    Decision,
    Outcome,
    ProcessTemplate,
    GapInput,
    RuleFeedback,
)
from app.schemas.schemas import (
    ProjectCreate,
    ProjectRead,
    ClientCreate,
    ClientRead,
    ResourceCreate,
    ResourceRead,
    RiskCreate,
    RiskRead,
    DecisionCreate,
    DecisionRead,
    OutcomeCreate,
    OutcomeRead,
    ProcessTemplateCreate,
    ProcessTemplateRead,
    GapInputCreate,
    GapInputRead,
    PortfolioKPIResponse,
    ScenarioResult,
    RecommendationRead,
    ExecutiveBrief,
)
from app.engine.analytics import calculate_kpi, portfolio_totals, portfolio_ranking, monte_carlo
from app.engine.recommendations import generate_recommendations, update_rule_feedback
from app.adapters.importers import import_projects_from_csv, import_projects_from_json

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/auth/login")
def login(user=Depends(auth_guard)) -> dict:
    return {"user": user}


@router.post("/clients", response_model=ClientRead)
def create_client(payload: ClientCreate, db: Session = Depends(get_db), user=Depends(auth_guard)):
    client = Client(**payload.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.get("/clients", response_model=list[ClientRead])
def list_clients(db: Session = Depends(get_db), user=Depends(auth_guard)):
    return db.query(Client).all()


@router.get("/clients/{client_id}", response_model=ClientRead)
def get_client(client_id: int, db: Session = Depends(get_db), user=Depends(auth_guard)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/clients/{client_id}", response_model=ClientRead)
def update_client(client_id: int, payload: ClientCreate, db: Session = Depends(get_db), user=Depends(auth_guard)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in payload.model_dump().items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client


@router.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db), user=Depends(auth_guard)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return {"status": "deleted"}


@router.post("/projects", response_model=ProjectRead)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), user=Depends(auth_guard)):
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects", response_model=list[ProjectRead])
def list_projects(db: Session = Depends(get_db), user=Depends(auth_guard)):
    return db.query(Project).all()


@router.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db), user=Depends(auth_guard)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/projects/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int, payload: ProjectCreate, db: Session = Depends(get_db), user=Depends(auth_guard)
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in payload.model_dump().items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), user=Depends(auth_guard)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"status": "deleted"}


@router.post("/projects/import")
def import_projects(file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(auth_guard)):
    content = file.file.read().decode("utf-8")
    projects = import_projects_from_csv(content, db)
    return {"imported": len(projects)}


@router.post("/projects/import-json")
def import_projects_json(file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(auth_guard)):
    content = file.file.read().decode("utf-8")
    projects = import_projects_from_json(content, db)
    return {"imported": len(projects)}


@router.post("/resources", response_model=ResourceRead)
def create_resource(payload: ResourceCreate, db: Session = Depends(get_db), user=Depends(auth_guard)):
    resource = Resource(**payload.model_dump())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


@router.get("/resources", response_model=list[ResourceRead])
def list_resources(db: Session = Depends(get_db), user=Depends(auth_guard)):
    return db.query(Resource).all()


@router.get("/resources/{resource_id}", response_model=ResourceRead)
def get_resource(resource_id: int, db: Session = Depends(get_db), user=Depends(auth_guard)):
    resource = db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


@router.put("/resources/{resource_id}", response_model=ResourceRead)
def update_resource(
    resource_id: int, payload: ResourceCreate, db: Session = Depends(get_db), user=Depends(auth_guard)
):
    resource = db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    for key, value in payload.model_dump().items():
        setattr(resource, key, value)
    db.commit()
    db.refresh(resource)
    return resource


@router.delete("/resources/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db), user=Depends(auth_guard)):
    resource = db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(resource)
    db.commit()
    return {"status": "deleted"}


@router.post("/risks", response_model=RiskRead)
def create_risk(payload: RiskCreate, db: Session = Depends(get_db), user=Depends(auth_guard)):
    risk = RiskItem(**payload.model_dump())
    db.add(risk)
    db.commit()
    db.refresh(risk)
    return risk


@router.get("/risks", response_model=list[RiskRead])
def list_risks(db: Session = Depends(get_db), user=Depends(auth_guard)):
    return db.query(RiskItem).all()


@router.get("/risks/{risk_id}", response_model=RiskRead)
def get_risk(risk_id: int, db: Session = Depends(get_db), user=Depends(auth_guard)):
    risk = db.get(RiskItem, risk_id)
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    return risk


@router.put("/risks/{risk_id}", response_model=RiskRead)
def update_risk(risk_id: int, payload: RiskCreate, db: Session = Depends(get_db), user=Depends(auth_guard)):
    risk = db.get(RiskItem, risk_id)
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    for key, value in payload.model_dump().items():
        setattr(risk, key, value)
    db.commit()
    db.refresh(risk)
    return risk


@router.delete("/risks/{risk_id}")
def delete_risk(risk_id: int, db: Session = Depends(get_db), user=Depends(auth_guard)):
    risk = db.get(RiskItem, risk_id)
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    db.delete(risk)
    db.commit()
    return {"status": "deleted"}


@router.get("/analytics/kpis", response_model=PortfolioKPIResponse)
def analytics_kpis(db: Session = Depends(get_db), user=Depends(auth_guard)):
    projects = db.query(Project).all()
    kpis = [calculate_kpi(project) for project in projects]
    totals = portfolio_totals(kpis)
    return PortfolioKPIResponse(
        kpis=[
            {
                "project_id": kpi.project_id,
                "ev": kpi.ev,
                "ac": kpi.ac,
                "pv": kpi.pv,
                "cv": kpi.cv,
                "sv": kpi.sv,
                "cpi": kpi.cpi,
                "spi": kpi.spi,
            }
            for kpi in kpis
        ],
        totals=totals,
    )


@router.get("/analytics/portfolio-ranking")
def analytics_portfolio_ranking(db: Session = Depends(get_db), user=Depends(auth_guard)):
    projects = db.query(Project).all()
    risks = db.query(RiskItem).all()
    return {"ranking": portfolio_ranking(projects, risks)}


@router.get("/analytics/scenario", response_model=list[ScenarioResult])
def analytics_scenario(
    project_id: int | None = None,
    iterations: int = 1000,
    inflation_factor: float = 1.0,
    staffing_capacity_factor: float = 1.0,
    risk_mitigation_effectiveness: float = 1.0,
    seed: int | None = None,
    db: Session = Depends(get_db),
    user=Depends(auth_guard),
):
    results = []
    projects = db.query(Project).all() if project_id is None else [db.get(Project, project_id)]
    for project in projects:
        if not project:
            continue
        risks = db.query(RiskItem).filter(RiskItem.project_id == project.id).all()
        output = monte_carlo(
            project,
            risks,
            iterations=iterations,
            inflation_factor=inflation_factor,
            staffing_capacity_factor=staffing_capacity_factor,
            risk_mitigation_effectiveness=risk_mitigation_effectiveness,
            seed=seed,
        )
        results.append(
            ScenarioResult(
                project_id=project.id,
                p50_cost=output["p50_cost"],
                p80_cost=output["p80_cost"],
                p50_days=output["p50_days"],
                p80_days=output["p80_days"],
                iterations=iterations,
            )
        )
    return results


@router.get("/recommendations", response_model=list[RecommendationRead])
def list_recommendations(db: Session = Depends(get_db), user=Depends(auth_guard)):
    projects = db.query(Project).all()
    risks = db.query(RiskItem).all()
    templates = db.query(ProcessTemplate).all()
    feedback = db.query(RuleFeedback).all()
    recommendations = generate_recommendations(projects, risks, templates, feedback)
    return [
        RecommendationRead(
            decision_type=rec.decision_type,
            affected_project_ids=rec.affected_project_ids,
            expected_impact=rec.expected_impact,
            explanation=rec.explanation,
            confidence=rec.confidence,
        )
        for rec in recommendations
    ]


@router.post("/decisions", response_model=DecisionRead)
def create_decision(payload: DecisionCreate, db: Session = Depends(get_db), user=Depends(auth_guard)):
    decision = Decision(**payload.model_dump())
    db.add(decision)
    db.commit()
    db.refresh(decision)
    return decision


@router.get("/decisions", response_model=list[DecisionRead])
def list_decisions(db: Session = Depends(get_db), user=Depends(auth_guard)):
    return db.query(Decision).all()


@router.get("/decisions/{decision_id}", response_model=DecisionRead)
def get_decision(decision_id: int, db: Session = Depends(get_db), user=Depends(auth_guard)):
    decision = db.get(Decision, decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision


@router.put("/decisions/{decision_id}", response_model=DecisionRead)
def update_decision(
    decision_id: int, payload: DecisionCreate, db: Session = Depends(get_db), user=Depends(auth_guard)
):
    decision = db.get(Decision, decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    for key, value in payload.model_dump().items():
        setattr(decision, key, value)
    db.commit()
    db.refresh(decision)
    return decision


@router.delete("/decisions/{decision_id}")
def delete_decision(decision_id: int, db: Session = Depends(get_db), user=Depends(auth_guard)):
    decision = db.get(Decision, decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    db.delete(decision)
    db.commit()
    return {"status": "deleted"}


@router.post("/decisions/{decision_id}/execute", response_model=DecisionRead)
def execute_decision(decision_id: int, db: Session = Depends(get_db), user=Depends(auth_guard)):
    decision = db.get(Decision, decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    decision.status = "executed"
    db.commit()
    db.refresh(decision)
    return decision


@router.post("/decisions/{decision_id}/outcomes", response_model=OutcomeRead)
def create_outcome(decision_id: int, payload: OutcomeCreate, db: Session = Depends(get_db), user=Depends(auth_guard)):
    outcome = Outcome(decision_id=decision_id, **payload.model_dump(exclude={"decision_id"}))
    db.add(outcome)
    db.commit()
    db.refresh(outcome)
    return outcome


@router.post("/process-templates", response_model=ProcessTemplateRead)
def create_template(payload: ProcessTemplateCreate, db: Session = Depends(get_db), user=Depends(auth_guard)):
    template = ProcessTemplate(**payload.model_dump())
    db.add(template)
    db.commit()
    db.refresh(template)
    return template


@router.get("/process-templates", response_model=list[ProcessTemplateRead])
def list_templates(db: Session = Depends(get_db), user=Depends(auth_guard)):
    return db.query(ProcessTemplate).all()


@router.get("/process-templates/{template_id}", response_model=ProcessTemplateRead)
def get_template(template_id: int, db: Session = Depends(get_db), user=Depends(auth_guard)):
    template = db.get(ProcessTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.put("/process-templates/{template_id}", response_model=ProcessTemplateRead)
def update_template(
    template_id: int, payload: ProcessTemplateCreate, db: Session = Depends(get_db), user=Depends(auth_guard)
):
    template = db.get(ProcessTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    for key, value in payload.model_dump().items():
        setattr(template, key, value)
    db.commit()
    db.refresh(template)
    return template


@router.delete("/process-templates/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db), user=Depends(auth_guard)):
    template = db.get(ProcessTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    db.delete(template)
    db.commit()
    return {"status": "deleted"}


@router.post("/gaps", response_model=GapInputRead)
def create_gap(payload: GapInputCreate, db: Session = Depends(get_db), user=Depends(auth_guard)):
    gap = GapInput(**payload.model_dump())
    db.add(gap)
    db.commit()
    db.refresh(gap)
    return gap


@router.get("/gaps", response_model=list[GapInputRead])
def list_gaps(db: Session = Depends(get_db), user=Depends(auth_guard)):
    return db.query(GapInput).all()


@router.get("/gaps/{gap_id}", response_model=GapInputRead)
def get_gap(gap_id: int, db: Session = Depends(get_db), user=Depends(auth_guard)):
    gap = db.get(GapInput, gap_id)
    if not gap:
        raise HTTPException(status_code=404, detail="Gap not found")
    return gap


@router.put("/gaps/{gap_id}", response_model=GapInputRead)
def update_gap(gap_id: int, payload: GapInputCreate, db: Session = Depends(get_db), user=Depends(auth_guard)):
    gap = db.get(GapInput, gap_id)
    if not gap:
        raise HTTPException(status_code=404, detail="Gap not found")
    for key, value in payload.model_dump().items():
        setattr(gap, key, value)
    db.commit()
    db.refresh(gap)
    return gap


@router.delete("/gaps/{gap_id}")
def delete_gap(gap_id: int, db: Session = Depends(get_db), user=Depends(auth_guard)):
    gap = db.get(GapInput, gap_id)
    if not gap:
        raise HTTPException(status_code=404, detail="Gap not found")
    db.delete(gap)
    db.commit()
    return {"status": "deleted"}


@router.get("/reports/executive-brief", response_model=ExecutiveBrief)
def executive_brief(db: Session = Depends(get_db), user=Depends(auth_guard)):
    projects = db.query(Project).all()
    risks = db.query(RiskItem).all()
    templates = db.query(ProcessTemplate).all()
    feedback = db.query(RuleFeedback).all()
    recommendations = generate_recommendations(projects, risks, templates, feedback)
    total_projects = len(projects)
    high_risk = len([r for r in risks if r.probability > 0.6])
    summary = f"Portfolio tracking {total_projects} projects with {high_risk} high-risk items."
    markdown = f"# Executive Brief\n\n{summary}\n\n## Recommendations\n" + "\n".join(
        [f"- {rec.decision_type}: {rec.explanation}" for rec in recommendations]
    )
    return ExecutiveBrief(
        summary=summary,
        markdown=markdown,
        metrics={"total_projects": total_projects, "high_risk": high_risk},
        recommendations=[
            RecommendationRead(
                decision_type=rec.decision_type,
                affected_project_ids=rec.affected_project_ids,
                expected_impact=rec.expected_impact,
                explanation=rec.explanation,
                confidence=rec.confidence,
            )
            for rec in recommendations
        ],
    )


@router.post("/decisions/{decision_id}/feedback")
def decision_feedback(decision_id: int, was_successful: bool, db: Session = Depends(get_db), user=Depends(auth_guard)):
    decision = db.get(Decision, decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    rule_key = decision.decision_type
    feedback = db.query(RuleFeedback).filter(RuleFeedback.rule_key == rule_key).first()
    if not feedback:
        feedback = RuleFeedback(rule_key=rule_key)
        db.add(feedback)
    feedback = update_rule_feedback(rule_key, was_successful, feedback)
    feedback.updated_at = datetime.utcnow()
    db.commit()
    return {"rule_key": feedback.rule_key, "success_rate": feedback.success_rate}
