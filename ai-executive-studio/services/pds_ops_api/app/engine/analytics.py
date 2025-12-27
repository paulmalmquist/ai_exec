from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable
import random

from app.models.models import Project, RiskItem


@dataclass
class KPI:
    project_id: int
    ev: float
    ac: float
    pv: float
    cv: float
    sv: float
    cpi: float
    spi: float


def _safe_div(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def calculate_kpi(project: Project, as_of: date | None = None) -> KPI:
    percent_complete = project.percent_complete / 100 if project.percent_complete > 1 else project.percent_complete
    ev = percent_complete * project.baseline_budget
    ac = project.actual_spend
    if not as_of:
        as_of = date.today()
    time_elapsed = (as_of - project.start_date).days
    baseline_duration = project.baseline_schedule_days or max((project.end_date - project.start_date).days, 1)
    pv = _safe_div(time_elapsed, baseline_duration) * project.baseline_budget
    cv = ev - ac
    sv = ev - pv
    cpi = _safe_div(ev, ac)
    spi = _safe_div(ev, pv)
    return KPI(
        project_id=project.id,
        ev=ev,
        ac=ac,
        pv=pv,
        cv=cv,
        sv=sv,
        cpi=cpi,
        spi=spi,
    )


def portfolio_totals(kpis: Iterable[KPI]) -> dict[str, float]:
    totals = {
        "ev": 0.0,
        "ac": 0.0,
        "pv": 0.0,
        "cv": 0.0,
        "sv": 0.0,
    }
    for kpi in kpis:
        totals["ev"] += kpi.ev
        totals["ac"] += kpi.ac
        totals["pv"] += kpi.pv
        totals["cv"] += kpi.cv
        totals["sv"] += kpi.sv
    totals["cpi"] = _safe_div(totals["ev"], totals["ac"])
    totals["spi"] = _safe_div(totals["ev"], totals["pv"])
    return totals


def portfolio_ranking(projects: list[Project], risks: list[RiskItem]) -> list[dict[str, float]]:
    risk_map: dict[int, float] = {}
    for risk in risks:
        risk_map.setdefault(risk.project_id, 0.0)
        risk_map[risk.project_id] += risk.probability * (risk.impact_cost + risk.impact_days * 1000)

    ranking = []
    for project in projects:
        kpi = calculate_kpi(project)
        client_priority = project.client.strategic_priority if project.client else 1
        satisfaction = project.client.satisfaction_score if project.client else 0
        pipeline = project.client.pipeline_value if project.client else 0
        attention_score = (
            abs(kpi.cv) * 0.2
            + abs(kpi.sv) * 0.15
            + risk_map.get(project.id, 0.0) * 0.1
            + client_priority * 10
            + max(0.0, (5 - satisfaction)) * 5
            + pipeline * 0.0001
            + project.safety_incidents * 15
        )
        ranking.append(
            {
                "project_id": project.id,
                "attention_score": attention_score,
                "cv": kpi.cv,
                "sv": kpi.sv,
                "risk_exposure": risk_map.get(project.id, 0.0),
            }
        )
    return sorted(ranking, key=lambda item: item["attention_score"], reverse=True)


def monte_carlo(
    project: Project,
    risks: list[RiskItem],
    iterations: int = 1000,
    inflation_factor: float = 1.0,
    staffing_capacity_factor: float = 1.0,
    risk_mitigation_effectiveness: float = 1.0,
    seed: int | None = None,
) -> dict[str, float]:
    if seed is not None:
        random.seed(seed)

    total_costs = []
    total_days = []
    for _ in range(iterations):
        cost = project.current_forecast
        days = project.forecast_schedule_days
        for risk in risks:
            probability = min(max(risk.probability * risk_mitigation_effectiveness, 0.0), 1.0)
            if random.random() <= probability:
                cost += risk.impact_cost * inflation_factor
                days += risk.impact_days / max(staffing_capacity_factor, 0.1)
        total_costs.append(cost)
        total_days.append(days)

    total_costs.sort()
    total_days.sort()
    p50_index = int(0.5 * iterations) - 1
    p80_index = int(0.8 * iterations) - 1
    return {
        "p50_cost": total_costs[max(p50_index, 0)],
        "p80_cost": total_costs[max(p80_index, 0)],
        "p50_days": total_days[max(p50_index, 0)],
        "p80_days": total_days[max(p80_index, 0)],
    }
