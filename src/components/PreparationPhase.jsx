import React, { useState, useEffect } from 'react';

export default function PreparationPhase({ onComplete }) {
  const [countdown, setCountdown] = useState(5);
  const [message, setMessage] = useState('Get ready...');

  useEffect(() => {
    const messages = [
      'Get ready...',
      'Relax your muscles...',
      'Keep your eyes open and steady...',
      'Recording will start soon...',
      'Almost ready...',
    ];

    setMessage(messages[5 - countdown] || 'Get ready...');

    if (countdown === 0) {
      onComplete();
      return;
    }

    const timer = setTimeout(() => {
      setCountdown(countdown - 1);
    }, 1000);

    return () => clearTimeout(timer);
  }, [countdown, onComplete]);

  return (
    <div className="phase-container">
      <h2 style={{ fontSize: '2rem', color: '#333', marginBottom: '30px' }}>
        Preparation
      </h2>

      <div className="preparation-text">{message}</div>

      <div className={`countdown ${countdown <= 2 ? 'warning' : ''}`}>
        {countdown}
      </div>

      <div className="status-indicator">
        <div className="status-dot"></div>
        <span>Preparing to record...</span>
      </div>

      <div style={{ marginTop: '40px', maxWidth: '500px', textAlign: 'center' }}>
        <p style={{ color: '#666', lineHeight: '1.6' }}>
          <strong>Tips for best results:</strong>
        </p>
        <ul style={{ 
          color: '#666', 
          lineHeight: '1.8', 
          textAlign: 'left',
          marginTop: '15px',
          paddingLeft: '20px'
        }}>
          <li>Sit comfortably and stay still</li>
          <li>Relax your jaw and facial muscles</li>
          <li>Keep your eyes open and focused on a point</li>
          <li>Breathe naturally and calmly</li>
        </ul>
      </div>
    </div>
  );
}

