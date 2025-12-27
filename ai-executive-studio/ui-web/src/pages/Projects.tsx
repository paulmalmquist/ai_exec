import { useEffect, useState } from 'react';
import api from '../services/api';
import { Project, ScenarioResult, KPIResult } from '../types';

const Projects = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [scenario, setScenario] = useState<Record<number, ScenarioResult>>({});
  const [kpis, setKpis] = useState<Record<number, KPIResult>>({});

  useEffect(() => {
    api.get('/projects').then((res) => setProjects(res.data));
    api.get('/analytics/kpis').then((res) => {
      const map: Record<number, KPIResult> = {};
      res.data.kpis.forEach((kpi: KPIResult) => {
        map[kpi.project_id] = kpi;
      });
      setKpis(map);
    });
  }, []);

  const runScenario = async (projectId: number) => {
    const res = await api.get('/analytics/scenario', { params: { project_id: projectId } });
    if (Array.isArray(res.data) && res.data[0]) {
      setScenario((prev) => ({ ...prev, [projectId]: res.data[0] }));
    }
  };

  return (
    <div className="card">
      <h2>Projects</h2>
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Region</th>
            <th>Sector</th>
            <th>Forecast</th>
            <th>Completion</th>
            <th>EVM (CPI/SPI)</th>
            <th>Scenario</th>
          </tr>
        </thead>
        <tbody>
          {projects.map((project) => (
            <tr key={project.id}>
              <td>{project.id}</td>
              <td>{project.region}</td>
              <td>{project.sector}</td>
              <td>${project.current_forecast.toLocaleString()}</td>
              <td>
                {project.percent_complete > 1
                  ? `${project.percent_complete.toFixed(0)}%`
                  : `${Math.round(project.percent_complete * 100)}%`}
              </td>
              <td>
                {kpis[project.id] ? (
                  <>
                    {kpis[project.id].cpi.toFixed(2)} / {kpis[project.id].spi.toFixed(2)}
                  </>
                ) : (
                  '—'
                )}
              </td>
              <td>
                <button onClick={() => runScenario(project.id)}>Run P50/P80</button>
                {scenario[project.id] && (
                  <div>
                    P50: ${scenario[project.id].p50_cost.toFixed(0)} / {scenario[project.id].p50_days.toFixed(0)}d
                    <br />
                    P80: ${scenario[project.id].p80_cost.toFixed(0)} / {scenario[project.id].p80_days.toFixed(0)}d
                  </div>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Projects;
