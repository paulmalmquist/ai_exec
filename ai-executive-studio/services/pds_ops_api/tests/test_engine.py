from datetime import date

from app.engine.analytics import calculate_kpi, monte_carlo, portfolio_ranking
from app.models.models import Project, RiskItem, Client


def make_project():
    client = Client(id=1, name="Test Client", strategic_priority=5, satisfaction_score=4.0, pipeline_value=100000)
    return Project(
        id=1,
        client_id=1,
        client=client,
        region="NA",
        sector="Office",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        baseline_budget=1000,
        current_forecast=1100,
        actual_spend=400,
        baseline_schedule_days=365,
        forecast_schedule_days=380,
        percent_complete=0.4,
        safety_incidents=0,
        status="active",
    )


def test_kpi_calculation():
    project = make_project()
    kpi = calculate_kpi(project, as_of=date(2024, 4, 1))
    assert round(kpi.ev, 2) == 400.0
    assert round(kpi.ac, 2) == 400.0
    assert round(kpi.cv, 2) == 0.0


def test_monte_carlo():
    project = make_project()
    risks = [RiskItem(project_id=1, category="cost", probability=1.0, impact_cost=100, impact_days=10)]
    output = monte_carlo(project, risks, iterations=10, seed=42)
    assert output["p50_cost"] >= project.current_forecast
    assert output["p80_cost"] >= output["p50_cost"]


def test_portfolio_ranking():
    project = make_project()
    ranking = portfolio_ranking([project], [])
    assert ranking[0]["project_id"] == project.id
