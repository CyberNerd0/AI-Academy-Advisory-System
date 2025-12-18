const API_BASE = 'http://127.0.0.1:8000';

// Initialize with default student ID for MVP demo
let currentStudentId = 1;
let currentRole = 'student';

// --- State Management ---
function switchRole() {
    const selector = document.getElementById('userRole');
    currentRole = selector.value;
    
    if (currentRole === 'student') {
        document.getElementById('studentView').style.display = 'block';
        document.getElementById('adviserView').style.display = 'none';
        loadStudentData(currentStudentId);
    } else {
        document.getElementById('studentView').style.display = 'none';
        document.getElementById('adviserView').style.display = 'block';
    }
}

// --- Student View Functions ---
async function loadStudentData(studentId) {
    try {
        const response = await fetch(`${API_BASE}/dashboard/student/${studentId}`);
        if (!response.ok) throw new Error('Failed to load data');
        
        const data = await response.json();
        renderDashboard(data);
    } catch (error) {
        console.error("Error:", error);
        alert("Could not connect to backend. Make sure the FastAPI server is running.");
    }
}

function renderDashboard(data) {
    // 1. Update Profile & KPIs
    document.getElementById('studentName').innerText = data.student_profile.name;
    document.getElementById('cgpaValue').innerText = data.academic_performance.cgpa.toFixed(2);
    document.getElementById('creditsValue').innerText = data.academic_performance.total_credits_attempted;
    
    // Simple logic for status: 2.0+ is "Good Standing", below is "Probation"
    const status = data.academic_performance.cgpa >= 2.0 ? "Good Standing" : "Probation";
    document.getElementById('statusValue').innerText = status;
    document.getElementById('statusValue').style.color = data.academic_performance.cgpa >= 2.0 ? "#059669" : "#dc2626";

    // 2. Render Courses
    const tbody = document.getElementById('courseTableBody');
    tbody.innerHTML = ''; // Clear previous

    data.course_recommendations.forEach(course => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${course.course_code}</strong></td>
            <td>${course.course_name}</td>
            <td>${course.credits}</td>
            <td><span class="status-badge status-${course.status}">${course.status}</span></td>
            <td>${course.reason}</td>
        `;
        tbody.appendChild(tr);
    });
}

// --- Chatbot Functions ---
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    if (!text) return;

    // Add User Message
    addMessageToChat(text, 'user');
    input.value = '';

    // Call API
    try {
        const response = await fetch(`${API_BASE}/ask/${currentStudentId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: text })
        });
        
        const data = await response.json();
        addMessageToChat(data.response, 'ai');
    } catch (error) {
        addMessageToChat("Error: Could not reach the advisor AI.", 'ai');
    }
}

function addMessageToChat(text, sender) {
    const history = document.getElementById('chatHistory');
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    div.innerText = text;
    history.appendChild(div);
    history.scrollTop = history.scrollHeight;
}

function handleEnter(event) {
    if (event.key === 'Enter') sendMessage();
}

// --- Adviser View Functions ---
async function loadAdviserView() {
    const studentId = document.getElementById('adviserStudentId').value;
    try {
        const response = await fetch(`${API_BASE}/adviser/student/${studentId}`);
        if (!response.ok) throw new Error("Student not found");
        
        const data = await response.json();
        
        document.getElementById('adviserContent').style.display = 'block';
        document.getElementById('adviserStudentName').innerText = data.student_profile.name;
        document.getElementById('adviserCgpa').innerText = data.academic_performance.cgpa.toFixed(2);
    } catch (error) {
        alert("Student not found");
    }
}

async function sendAdviserMessage() {
    const studentId = document.getElementById('adviserStudentId').value;
    const input = document.getElementById('adviserChatInput');
    const text = input.value.trim();
    if (!text) return;
    
    // Call API
    try {
        const response = await fetch(`${API_BASE}/ask/${studentId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: text })
        });
        
        const data = await response.json();
        const output = document.getElementById('adviserChatOutput');
        output.innerHTML += `<p><strong>You asked:</strong> ${text}<br><strong>AI Answer:</strong> ${data.response}</p>`;
        input.value = '';
    } catch (error) {
        alert("Error invoking AI");
    }
}

// Start
loadStudentData(currentStudentId);
