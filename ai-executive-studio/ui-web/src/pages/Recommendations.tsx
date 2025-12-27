import { useEffect, useState } from 'react';
import api from '../services/api';
import { Recommendation } from '../types';

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);

  useEffect(() => {
    api.get('/recommendations').then((res) => setRecommendations(res.data));
  }, []);

  const promoteDecision = async (rec: Recommendation) => {
    await api.post('/decisions', {
      decision_type: rec.decision_type,
      rationale: rec.explanation,
      expected_impact_json: rec.expected_impact,
      status: 'proposed',
      owner: 'executive',
      related_project_ids: rec.affected_project_ids,
      related_risk_ids: []
    });
    alert('Decision created');
  };

  return (
    <div className="card">
      <h2>Recommendations</h2>
      <table className="table">
        <thead>
          <tr>
            <th>Type</th>
            <th>Explanation</th>
            <th>Confidence</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {recommendations.map((rec, index) => (
            <tr key={index}>
              <td>{rec.decision_type}</td>
              <td>{rec.explanation}</td>
              <td>{(rec.confidence * 100).toFixed(0)}%</td>
              <td>
                <button onClick={() => promoteDecision(rec)}>Promote</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Recommendations;
