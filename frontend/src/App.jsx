import React, { useState } from 'react';
import StudentDashboard from './components/StudentDashboard';
import AdviserDashboard from './components/AdviserDashboard';
import './index.css';

function App() {
  const [role, setRole] = useState('student');
  const [studentId, setStudentId] = useState(1);

  return (
    <div id="app">
      <nav>
        <div className="logo">🎓 Academic Advisor</div>
        <div className="user-selector">
          <label style={{ marginRight: '0.5rem' }}>View as:</label>
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            style={{ padding: '0.25rem', borderRadius: '0.25rem' }}
          >
            <option value="student">Student (John Doe)</option>
            <option value="adviser">Adviser (Dr. Smith)</option>
          </select>
        </div>
      </nav>

      {role === 'student' ? (
        <StudentDashboard studentId={studentId} studentName="John Doe" />
      ) : (
        <AdviserDashboard />
      )}
    </div>
  );
}

export default App;
