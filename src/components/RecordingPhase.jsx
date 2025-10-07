import React, { useState, useEffect } from 'react';

export default function RecordingPhase({ duration, recorder, onComplete }) {
  const [timeLeft, setTimeLeft] = useState(duration);
  const [samplesCollected, setSamplesCollected] = useState(0);

  useEffect(() => {
    if (timeLeft === 0) {
      onComplete();
      return;
    }

    const timer = setTimeout(() => {
      setTimeLeft(timeLeft - 1);
    }, 1000);

    return () => clearTimeout(timer);
  }, [timeLeft, onComplete]);

  const progress = ((duration - timeLeft) / duration) * 100;

  return (
    <div className="phase-container">
      <h2 style={{ fontSize: '2rem', color: '#333', marginBottom: '30px' }}>
        Recording in Progress
      </h2>

      <div className="status-indicator">
        <div className="status-dot"></div>
        <span>Recording EEG data...</span>
      </div>

      <div className={`countdown ${timeLeft <= 3 ? 'warning' : ''}`}>
        {timeLeft}
      </div>

      <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '20px' }}>
        seconds remaining
      </p>

      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress}%` }}></div>
      </div>

      <div className="recording-info">
        <p style={{ color: '#999', fontSize: '0.9rem' }}>
          Stay still and maintain focus
        </p>
      </div>

      <div className="stats-grid" style={{ maxWidth: '600px' }}>
        <div className="stat-card">
          <h3>Duration</h3>
          <p>{duration}s</p>
        </div>
        <div className="stat-card">
          <h3>Elapsed</h3>
          <p>{duration - timeLeft}s</p>
        </div>
        <div className="stat-card">
          <h3>Progress</h3>
          <p>{Math.round(progress)}%</p>
        </div>
      </div>
    </div>
  );
}

