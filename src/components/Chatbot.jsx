import React, { useState } from 'react';
import axios from 'axios';

const Chatbot = ({ studentId, role }) => {
    const [messages, setMessages] = useState([
        { text: "Hello! I can help you with course planning or explain your GPA. Ask me anything!", sender: 'ai' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMsg = { text: input, sender: 'user' };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        try {
            // Include question in body
            const response = await axios.post(`http://127.0.0.1:8000/ask/${studentId}`, {
                question: userMsg.text
            });

            const aiMsg = { text: response.data.response, sender: 'ai' };
            setMessages(prev => [...prev, aiMsg]);
        } catch (error) {
            setMessages(prev => [...prev, { text: "Error: Could not reach the advisor AI.", sender: 'ai' }]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') sendMessage();
    };

    return (
        <div className="card chat-card">
            <h2>{role === 'adviser' ? 'AI Simulation' : 'Ask AI Advisor'}</h2>
            <div className="chat-history">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender}`}>
                        {msg.text}
                    </div>
                ))}
                {loading && <div className="message ai">Thinking...</div>}
            </div>
            <div className="chat-input-area">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="e.g., Why can't I take CSC401?"
                />
                <button onClick={sendMessage} disabled={loading}>Send</button>
            </div>
        </div>
    );
};

export default Chatbot;
