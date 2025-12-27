import { useEffect, useState } from 'react';
import api from '../services/api';
import { GapInput } from '../types';

const GapCapture = () => {
  const [gaps, setGaps] = useState<GapInput[]>([]);
  const [step, setStep] = useState(0);
  const [form, setForm] = useState({
    category: 'data_access',
    question: '',
    dataSource: 'project_management',
    access: 'yes',
    confidence: 0.5
  });

  const steps = [
    {
      label: 'What data source would improve this decision?',
      field: 'dataSource'
    },
    {
      label: 'Do you have access?',
      field: 'access'
    },
    {
      label: 'If yes, what fields/tables?',
      field: 'detailsYes'
    },
    {
      label: 'If no, who owns access?',
      field: 'detailsNo'
    },
    {
      label: 'Any policy constraints?',
      field: 'policy'
    }
  ];

  const [details, setDetails] = useState({
    detailsYes: '',
    detailsNo: '',
    policy: ''
  });

  const fetchGaps = () => {
    api.get('/gaps').then((res) => setGaps(res.data));
  };

  useEffect(() => {
    fetchGaps();
  }, []);

  const handleNext = () => {
    setStep((prev) => Math.min(prev + 1, steps.length - 1));
  };

  const handleBack = () => {
    setStep((prev) => Math.max(prev - 1, 0));
  };

  const saveGap = async () => {
    const answerText = [
      `Access: ${form.access}`,
      `Yes details: ${details.detailsYes}`,
      `No owner: ${details.detailsNo}`,
      `Policy: ${details.policy}`
    ].join('\n');
    await api.post('/gaps', {
      category: form.category,
      question: `${form.dataSource} - ${form.question}`,
      answer: answerText,
      confidence: form.confidence
    });
    setForm({ ...form, question: '', access: 'yes', dataSource: 'project_management', confidence: 0.5 });
    setDetails({ detailsYes: '', detailsNo: '', policy: '' });
    setStep(0);
    fetchGaps();
  };

  return (
    <div className="grid grid-2">
      <section className="card">
        <h2>Gap Capture Wizard</h2>
        <div className="notice">
          Capture missing data, access constraints, and policy constraints. This keeps proprietary details out of code.
        </div>
        <div>
          <label>
            Category
            <select
              value={form.category}
              onChange={(event) => setForm({ ...form, category: event.target.value })}
            >
              <option value="data_access">Data access</option>
              <option value="process">Process</option>
              <option value="policy">Policy</option>
              <option value="metric">Metric</option>
            </select>
          </label>
        </div>
        <div style={{ marginTop: '1rem' }}>
          <label>
            {steps[step].label}
            {steps[step].field === 'dataSource' && (
              <>
                <select
                  value={form.dataSource}
                  onChange={(event) => setForm({ ...form, dataSource: event.target.value })}
                >
                  <option value=\"project_management\">Project management platform</option>
                  <option value=\"finance\">Finance system</option>
                  <option value=\"resource_planning\">Resource planning</option>
                  <option value=\"risk_register\">Risk register</option>
                  <option value=\"other\">Other</option>
                </select>
                <textarea
                  placeholder=\"Add context or specific system name\"\n                  value={form.question}
                  onChange={(event) => setForm({ ...form, question: event.target.value })}
                />
              </>
            )}
            {steps[step].field === 'access' && (
              <select
                value={form.access}
                onChange={(event) => setForm({ ...form, access: event.target.value })}
              >
                <option value=\"yes\">Yes</option>
                <option value=\"no\">No</option>
              </select>
            )}
            {steps[step].field === 'detailsYes' && (
              <textarea
                value={details.detailsYes}
                onChange={(event) => setDetails({ ...details, detailsYes: event.target.value })}
              />
            )}
            {steps[step].field === 'detailsNo' && (
              <textarea
                value={details.detailsNo}
                onChange={(event) => setDetails({ ...details, detailsNo: event.target.value })}
              />
            )}
            {steps[step].field === 'policy' && (
              <textarea
                value={details.policy}
                onChange={(event) => setDetails({ ...details, policy: event.target.value })}
              />
            )}
          </label>
        </div>
        <div style={{ marginTop: '1rem' }}>
          <label>
            Confidence: {form.confidence.toFixed(2)}
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={form.confidence}
              onChange={(event) => setForm({ ...form, confidence: Number(event.target.value) })}
            />
          </label>
        </div>
        <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem' }}>
          <button onClick={handleBack}>Back</button>
          {step < steps.length - 1 ? (
            <button onClick={handleNext}>Next</button>
          ) : (
            <button onClick={saveGap}>Save Gap</button>
          )}
        </div>
      </section>
      <section className="card">
        <h2>Gap Backlog</h2>
        <ul>
          {gaps.map((gap) => (
            <li key={gap.id}>
              <strong>{gap.category}</strong> - {gap.question}
              <br />
              <small>Confidence {gap.confidence}</small>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
};

export default GapCapture;
