import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Chatbot from './Chatbot';

const StudentDashboard = ({ studentId, studentName }) => {
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`/api/dashboard/student/${studentId}`);
                setData(response.data);
            } catch (err) {
                setError("Failed to load dashboard data. Ensure backend is running.");
            }
        };
        fetchData();
    }, [studentId]);

    if (error) return <div className="card">{error}</div>;
    if (!data) return <div className="card">Loading...</div>;

    const { academic_performance, course_recommendations } = data;
    const status = academic_performance.cgpa >= 2.0 ? "Good Standing" : "Probation";
    const statusColor = academic_performance.cgpa >= 2.0 ? "#059669" : "#dc2626";

    return (
        <main>
            <header>
                <h1>My Dashboard</h1>
                <p>Welcome back, <span style={{ fontWeight: 'bold' }}>{data.student_profile.name}</span></p>
            </header>

            <div className="kpi-grid">
                <div className="card kpi">
                    <h3>Current CGPA</h3>
                    <div className="value">{academic_performance.cgpa.toFixed(2)}</div>
                    <small>All-time average</small>
                </div>
                <div className="card kpi">
                    <h3>Credits Earned</h3>
                    <div className="value">{academic_performance.total_credits_attempted}</div>
                    <small>Total Units</small>
                </div>
                <div className="card kpi">
                    <h3>Status</h3>
                    <div className="value" style={{ color: statusColor }}>{status}</div>
                    <small>Academic Standing</small>
                </div>
            </div>

            <div className="content-grid">
                <div className="card">
                    <h2>Course Eligibility</h2>
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>Code</th>
                                <th>Course</th>
                                <th>Credits</th>
                                <th>Status</th>
                                <th>Reason</th>
                            </tr>
                        </thead>
                        <tbody>
                            {course_recommendations.map((course, index) => (
                                <tr key={index}>
                                    <td><strong>{course.course_code}</strong></td>
                                    <td>{course.course_name}</td>
                                    <td>{course.credits}</td>
                                    <td>
                                        <span className={`status-badge status-${course.status}`}>
                                            {course.status}
                                        </span>
                                    </td>
                                    <td>{course.reason}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <Chatbot studentId={studentId} role="student" />
            </div>
        </main>
    );
};

export default StudentDashboard;
