import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';

const initialEmployees = [
  { id: 1, name: "John Doe", freeDays: 20, absences: [], messages: [] },
  { id: 2, name: "Jane Smith", freeDays: 20, absences: [], messages: [] },
];

const App = () => {
  const [employees, setEmployees] = useState(() => {
    const saved = localStorage.getItem('employees');
    return saved ? JSON.parse(saved) : initialEmployees;
  });
  const [currentUser, setCurrentUser] = useState(initialEmployees[0]);
  const [formData, setFormData] = useState({ type: 'free', date: '', reason: '' });
  const [messageData, setMessageData] = useState({ recipientId: '', content: '' });

  useEffect(() => {
    localStorage.setItem('employees', JSON.stringify(employees));
  }, [employees]);

  const handleRequestSubmit = (e) => {
    e.preventDefault();
    if (!formData.date || !formData.reason) return alert("Please fill all fields");

    setEmployees(employees.map(emp => {
      if (emp.id === currentUser.id) {
        if (formData.type === 'free' && emp.freeDays > 0) {
          return {
            ...emp,
            freeDays: emp.freeDays - 1,
            absences: [...emp.absences, { date: formData.date, reason: formData.reason, type: 'Free Day' }]
          };
        } else if (formData.type === 'absence') {
          return {
            ...emp,
            absences: [...emp.absences, { date: formData.date, reason: formData.reason, type: 'Absence' }]
          };
        }
      }
      return emp;
    }));
    setFormData({ type: 'free', date: '', reason: '' });
    alert("Request submitted successfully!");
  };

  const handleMessageSubmit = (e) => {
    e.preventDefault();
    if (!messageData.recipientId || !messageData.content) return alert("Please fill all fields");

    setEmployees(employees.map(emp => {
      if (emp.id === parseInt(messageData.recipientId)) {
        return {
          ...emp,
          messages: [...emp.messages, {
            sender: currentUser.name,
            content: messageData.content,
            timestamp: new Date().toLocaleString()
          }]
        };
      }
      return emp;
    }));
    setMessageData({ recipientId: '', content: '' });
    alert("Message sent successfully!");
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-center">Employee Management System</h1>
      
      {/* User Selection */}
      <div className="card">
        <div className="form-group">
          <label>Select User:</label>
          <select
            value={currentUser.id}
            onChange={(e) => setCurrentUser(employees.find(emp => emp.id === parseInt(e.target.value)))}
            className="form-group"
          >
            {employees.map(emp => (
              <option key={emp.id} value={emp.id}>{emp.name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Free Days Info */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Welcome, {currentUser.name}</h2>
        <p className="text-lg">Remaining Free Days: <span className="font-bold">{currentUser.freeDays}</span></p>
      </div>

      {/* Request Form */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Request Free Day or Absence</h2>
        <form onSubmit={handleRequestSubmit} className="space-y-4">
          <div className="form-group">
            <label>Request Type:</label>
            <select
              value={formData.type}
              onChange={(e) => setFormData({ ...formData, type: e.target.value })}
              className="form-group"
            >
              <option value="free">Free Day</option>
              <option value="absence">Absence</option>
            </select>
          </div>
          <div className="form-group">
            <label>Date:</label>
            <input
              type="date"
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              className="form-group"
            />
          </div>
          <div className="form-group">
            <label>Reason:</label>
            <input
              type="text"
              value={formData.reason}
              onChange={(e) => setFormData({ ...formData, reason: e.target.value })}
              className="form-group"
              placeholder="Enter reason"
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Submit Request
          </button>
        </form>
      </div>

      {/* Absence History */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Absence History</h2>
        {currentUser.absences.length > 0 ? (
          <ul className="space-y-2">
            {currentUser.absences.map((absence, index) => (
              <li key={index} className="list-item">
                <p><strong>Type:</strong> {absence.type}</p>
                <p><strong>Date:</strong> {absence.date}</p>
                <p><strong>Reason:</strong> {absence.reason}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No absences recorded.</p>
        )}
      </div>

      {/* Messaging System */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Messages</h2>
        <form onSubmit={handleMessageSubmit} className="space-y-4 mb-6">
          <div className="form-group">
            <label>Recipient:</label>
            <select
              value={messageData.recipientId}
              onChange={(e) => setMessageData({ ...messageData, recipientId: e.target.value })}
              className="form-group"
            >
              <option value="">Select recipient</option>
              {employees.filter(emp => emp.id !== currentUser.id).map(emp => (
                <option key={emp.id} value={emp.id}>{emp.name}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Message:</label>
            <textarea
              value={messageData.content}
              onChange={(e) => setMessageData({ ...messageData, content: e.target.value })}
              className="form-group"
              placeholder="Type your message"
            />
          </div>
          <button type="submit" className="btn btn-secondary">
            Send Message
          </button>
        </form>
        <h3 className="text-lg font-medium mb-2">Received Messages</h3>
        {currentUser.messages.length > 0 ? (
          <ul className="space-y-2">
            {currentUser.messages.map((msg, index) => (
              <li key={index} className="list-item">
                <p><strong>From:</strong> {msg.sender}</p>
                <p><strong>Time:</strong> {msg.timestamp}</p>
                <p><strong>Message:</strong> {msg.content}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No messages received.</p>
        )}
      </div>
    </div>
  );
};

const root = createRoot(document.getElementById('root'));
root.render(<App />);