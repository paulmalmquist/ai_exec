import { useEffect, useState } from 'react';
import api from '../services/api';
import { Decision } from '../types';

const Decisions = () => {
  const [decisions, setDecisions] = useState<Decision[]>([]);
  const [notes, setNotes] = useState<Record<number, string>>({});

  const fetchDecisions = () => {
    api.get('/decisions').then((res) => setDecisions(res.data));
  };

  useEffect(() => {
    fetchDecisions();
  }, []);

  const executeDecision = async (id: number) => {
    await api.post(`/decisions/${id}/execute`);
    fetchDecisions();
  };

  const recordOutcome = async (id: number) => {
    await api.post(`/decisions/${id}/outcomes`, {
      decision_id: id,
      kpi_before_json: { placeholder: true },
      kpi_after_json: { placeholder: true },
      notes: notes[id] || ''
    });
    setNotes((prev) => ({ ...prev, [id]: '' }));
    fetchDecisions();
  };

  return (
    <div className="card">
      <h2>Decisions Pipeline</h2>
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Type</th>
            <th>Status</th>
            <th>Owner</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {decisions.map((decision) => (
            <tr key={decision.id}>
              <td>{decision.id}</td>
              <td>{decision.decision_type}</td>
              <td>{decision.status}</td>
              <td>{decision.owner}</td>
              <td>
                <button onClick={() => executeDecision(decision.id)}>Mark Executed</button>
                <div>
                  <textarea
                    placeholder="Outcome notes"
                    value={notes[decision.id] || ''}
                    onChange={(event) =>
                      setNotes((prev) => ({ ...prev, [decision.id]: event.target.value }))
                    }
                  />
                  <button onClick={() => recordOutcome(decision.id)}>Save Outcome</button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Decisions;
