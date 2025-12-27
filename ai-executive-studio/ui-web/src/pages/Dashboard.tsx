import { useEffect, useState } from 'react';
import api from '../services/api';
import { PortfolioKPIs, Recommendation } from '../types';

const Dashboard = () => {
  const [kpis, setKpis] = useState<PortfolioKPIs | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [ranking, setRanking] = useState<Array<{ project_id: number; attention_score: number }>>([]);

  useEffect(() => {
    api.get('/analytics/kpis').then((res) => setKpis(res.data));
    api.get('/recommendations').then((res) => setRecommendations(res.data));
    api.get('/analytics/portfolio-ranking').then((res) => setRanking(res.data.ranking || []));
  }, []);

  return (
    <div className="grid grid-2">
      <section className="card">
        <h2>Portfolio KPIs</h2>
        {kpis ? (
          <div className="grid">
            <div className="badge">CPI: {kpis.totals.cpi?.toFixed(2)}</div>
            <div className="badge">SPI: {kpis.totals.spi?.toFixed(2)}</div>
            <p>EV: {kpis.totals.ev?.toFixed(0)}</p>
            <p>AC: {kpis.totals.ac?.toFixed(0)}</p>
            <p>CV: {kpis.totals.cv?.toFixed(0)}</p>
            <p>SV: {kpis.totals.sv?.toFixed(0)}</p>
          </div>
        ) : (
          <p>Loading KPI summary...</p>
        )}
      </section>
      <section className="card">
        <h2>Latest Recommendations</h2>
        {recommendations.length === 0 ? (
          <p>No recommendations yet.</p>
        ) : (
          <ul>
            {recommendations.slice(0, 4).map((rec, index) => (
              <li key={index}>
                <strong>{rec.decision_type}</strong>: {rec.explanation}
              </li>
            ))}
          </ul>
        )}
      </section>
      <section className="card">
        <h2>Top Risk Projects</h2>
        {ranking.length === 0 ? (
          <p>No ranking available.</p>
        ) : (
          <ol>
            {ranking.slice(0, 5).map((item) => (
              <li key={item.project_id}>
                Project {item.project_id} — Attention score {item.attention_score.toFixed(1)}
              </li>
            ))}
          </ol>
        )}
      </section>
    </div>
  );
};

export default Dashboard;
