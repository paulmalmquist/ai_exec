import { NavLink, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Projects from './pages/Projects';
import Recommendations from './pages/Recommendations';
import Decisions from './pages/Decisions';
import GapCapture from './pages/GapCapture';
import ProcessTemplates from './pages/ProcessTemplates';

const App = () => {
  return (
    <div className="app">
      <header className="app-header">
        <div>
          <h1>AI Executive (PDS Ops)</h1>
          <p>Executive decision intelligence inspired by Gelino & Kessling.</p>
        </div>
        <nav>
          <NavLink to="/" end>Dashboard</NavLink>
          <NavLink to="/projects">Projects</NavLink>
          <NavLink to="/recommendations">Recommendations</NavLink>
          <NavLink to="/decisions">Decisions</NavLink>
          <NavLink to="/gaps">Gap Capture</NavLink>
          <NavLink to="/process">Process Templates</NavLink>
        </nav>
      </header>
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/decisions" element={<Decisions />} />
          <Route path="/gaps" element={<GapCapture />} />
          <Route path="/process" element={<ProcessTemplates />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;
