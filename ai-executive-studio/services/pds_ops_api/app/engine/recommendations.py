from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from app.engine.analytics import calculate_kpi
from app.models.models import Project, RiskItem, ProcessTemplate, RuleFeedback


@dataclass
class Recommendation:
    decision_type: str
    affected_project_ids: list[int]
    expected_impact: dict
    explanation: str
    confidence: float
    rule_key: str


def _rule_confidence(rule_key: str, feedback: Iterable[RuleFeedback]) -> float:
    for item in feedback:
        if item.rule_key == rule_key:
            return item.success_rate
    return 0.5


def generate_recommendations(
    projects: list[Project],
    risks: list[RiskItem],
    templates: list[ProcessTemplate],
    feedback: Iterable[RuleFeedback],
) -> list[Recommendation]:
    recommendations: list[Recommendation] = []
    risk_map: dict[int, float] = {}
    risk_category_count: dict[str, int] = {}

    for risk in risks:
        risk_map.setdefault(risk.project_id, 0.0)
        risk_map[risk.project_id] += risk.probability * (risk.impact_cost + risk.impact_days * 1000)
        risk_category_count[risk.category] = risk_category_count.get(risk.category, 0) + 1

    for project in projects:
        kpi = calculate_kpi(project)
        client_priority = project.client.strategic_priority if project.client else 1
        if kpi.spi < 0.9 and client_priority >= 4:
            rule_key = "schedule_slip_priority"
            recommendations.append(
                Recommendation(
                    decision_type="escalate",
                    affected_project_ids=[project.id],
                    expected_impact={"schedule_recovery_days": 10, "resource_shift": "increase"},
                    explanation=(
                        f"SPI {kpi.spi:.2f} below 0.90 with client priority {client_priority}; "
                        "recommend escalation and resource reallocation."
                    ),
                    confidence=_rule_confidence(rule_key, feedback),
                    rule_key=rule_key,
                )
            )

        if kpi.cpi < 0.9:
            rule_key = "cost_overrun"
            recommendations.append(
                Recommendation(
                    decision_type="risk_mitigation",
                    affected_project_ids=[project.id],
                    expected_impact={"cost_control": True, "target_cpi": 0.95},
                    explanation=(
                        f"CPI {kpi.cpi:.2f} below 0.90; recommend cost controls and risk mitigation actions."
                    ),
                    confidence=_rule_confidence(rule_key, feedback),
                    rule_key=rule_key,
                )
            )

    if risk_category_count.get("schedule", 0) >= 3 and templates:
        template = templates[0]
        rule_key = "standardize_schedule_controls"
        recommendations.append(
            Recommendation(
                decision_type="standardize_process",
                affected_project_ids=[p.id for p in projects],
                expected_impact={"template_id": template.id, "adoption_target": 0.75},
                explanation=(
                    "Schedule risks recurring across portfolio; recommend standardizing process "
                    f"using template '{template.name}'."
                ),
                confidence=_rule_confidence(rule_key, feedback),
                rule_key=rule_key,
            )
        )

    if risk_category_count.get("scope", 0) >= 3:
        rule_key = "staff_training_gap"
        recommendations.append(
            Recommendation(
                decision_type="staffing_training",
                affected_project_ids=[p.id for p in projects],
                expected_impact={"training_focus": "scope control", "target_completion": "Q4"},
                explanation="Repeated scope-related risks suggest a skill gap; recommend training program.",
                confidence=_rule_confidence(rule_key, feedback),
                rule_key=rule_key,
            )
        )

    return recommendations


def update_rule_feedback(rule_key: str, was_successful: bool, feedback: RuleFeedback) -> RuleFeedback:
    adjustment = 0.05 if was_successful else -0.05
    feedback.success_rate = min(max(feedback.success_rate + adjustment, 0.1), 0.9)
    return feedback
