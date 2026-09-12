import { useState, useEffect } from 'react'
import './index.css'

function App() {
  const [systemTime, setSystemTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const timer = setInterval(() => setSystemTime(new Date().toLocaleTimeString()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="dashboard-container">
      
      <div className="header glass-card">
        <h1>KALMIYA V4.0 - Neural Dashboard</h1>
        <div className="time" style={{fontSize: '1.2rem', fontWeight: 'bold'}}>{systemTime}</div>
      </div>

      <div className="main-content">
        <div className="agent-grid">
          
          <div className="agent-card glass-card">
            <div className="agent-icon">🧠</div>
            <h2>Main Assistant</h2>
            <p className="agent-status status-active">Online - Ready</p>
          </div>

          <div className="agent-card glass-card">
            <div className="agent-icon">🔍</div>
            <h2>Investigator Agent</h2>
            <p className="agent-status">Standby</p>
          </div>

          <div className="agent-card glass-card">
            <div className="agent-icon">💻</div>
            <h2>Coder Agent</h2>
            <p className="agent-status">Standby</p>
          </div>

        </div>
      </div>

      <div className="sidebar">
        
        <div className="glass-card">
          <h3 style={{marginBottom: '15px', color: 'var(--accent)'}}>System Metrics</h3>
          <div className="metric-row">
            <span>CPU Usage</span>
            <span className="status-active">14%</span>
          </div>
          <div className="metric-row">
            <span>Memory (RAM)</span>
            <span style={{color: '#f59e0b'}}>68%</span>
          </div>
          <div className="metric-row">
            <span>Disk I/O</span>
            <span>2%</span>
          </div>
        </div>

        <div className="glass-card">
          <h3 style={{marginBottom: '15px', color: '#10b981'}}>Vision Sensor</h3>
          <div style={{textAlign: 'center', fontSize: '2rem', margin: '10px 0'}}>
            👁️
          </div>
          <p style={{textAlign: 'center', fontSize: '0.9rem', color: 'var(--text-secondary)'}}>Scanning for user...</p>
        </div>

      </div>

    </div>
  )
}

export default App
