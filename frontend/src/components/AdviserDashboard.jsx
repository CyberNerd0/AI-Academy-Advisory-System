import React, { useState } from 'react';
import axios from 'axios';
import Chatbot from './Chatbot';

const AdviserDashboard = () => {
    const [studentId, setStudentId] = useState(1);
    const [studentData, setStudentData] = useState(null);
    const [loading, setLoading] = useState(false);

    const fetchStudent = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`/api/adviser/student/${studentId}`);
            setStudentData(response.data);
        } catch (error) {
            alert("Student not found");
            setStudentData(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <main>
            <header>
                <h1>Adviser Portal</h1>
                <p>Managing Students</p>
            </header>

            <div className="card">
                <h2>Student Lookup</h2>
                <div className="chat-input-area" style={{ marginBottom: '1rem' }}>
                    <input
                        type="number"
                        value={studentId}
                        onChange={(e) => setStudentId(e.target.value)}
                        placeholder="Enter Student ID"
                    />
                    <button onClick={fetchStudent} disabled={loading}>
                        {loading ? 'Loading...' : 'Load Student'}
                    </button>
                </div>

                {studentData && (
                    <div style={{ marginTop: '2rem' }}>
                        <h3 style={{ borderBottom: '1px solid #eee', paddingBottom: '0.5rem' }}>
                            Viewing: {studentData.student_profile.name} (ID: {studentId})
                        </h3>
                        <p><strong>CGPA:</strong> {studentData.academic_performance.cgpa.toFixed(2)}</p>

                        <div style={{ marginTop: '1.5rem' }}>
                            <h4>AI Simulation</h4>
                            <p style={{ marginBottom: '1rem', color: '#666' }}>
                                Ask a question on behalf of this student to verify advisory logic.
                            </p>
                            <Chatbot studentId={studentId} role="adviser" />
                        </div>
                    </div>
                )}
            </div>
        </main>
    );
};

export default AdviserDashboard;
