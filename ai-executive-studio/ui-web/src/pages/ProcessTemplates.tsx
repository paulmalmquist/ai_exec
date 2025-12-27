import { useEffect, useState } from 'react';
import api from '../services/api';
import { ProcessTemplate } from '../types';

const ProcessTemplates = () => {
  const [templates, setTemplates] = useState<ProcessTemplate[]>([]);

  useEffect(() => {
    api.get('/process-templates').then((res) => setTemplates(res.data));
  }, []);

  return (
    <div className="card">
      <h2>Process Templates</h2>
      <table className="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Adoption</th>
          </tr>
        </thead>
        <tbody>
          {templates.map((template) => (
            <tr key={template.id}>
              <td>{template.name}</td>
              <td>{template.description}</td>
              <td>{(template.adoption_rate_pct * 100).toFixed(0)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ProcessTemplates;
