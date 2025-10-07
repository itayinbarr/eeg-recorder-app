import React, { useState } from 'react';

export default function SetupPhase({ onConnect, onStart }) {
  const [duration, setDuration] = useState(10);
  const [isConnecting, setIsConnecting] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);

  const handleConnect = async () => {
    setIsConnecting(true);
    setError(null);

    try {
      await onConnect();
      setIsConnected(true);
    } catch (err) {
      setError(err.message || 'Failed to connect to Muse device');
      console.error('Connection error:', err);
    } finally {
      setIsConnecting(false);
    }
  };

  const handleStart = () => {
    if (duration < 1) {
      setError('Duration must be at least 1 second');
      return;
    }
    if (duration > 300) {
      setError('Duration cannot exceed 5 minutes (300 seconds)');
      return;
    }
    onStart(duration);
  };

  return (
    <div className="phase-container">
      <h2 style={{ fontSize: '2rem', color: '#333', marginBottom: '30px' }}>
        Setup Your Recording
      </h2>

      {!isConnected ? (
        <>
          <p style={{ color: '#666', marginBottom: '30px', textAlign: 'center', maxWidth: '500px' }}>
            Connect your Muse 2 headset via Bluetooth to begin recording EEG data.
            Make sure your device is powered on and in pairing mode.
          </p>

          {error && <div className="error-message">{error}</div>}

          <button
            className="button"
            onClick={handleConnect}
            disabled={isConnecting}
          >
            {isConnecting ? 'Connecting...' : 'Connect Muse 2 Headset'}
          </button>

          <p style={{ color: '#999', marginTop: '20px', fontSize: '0.9rem' }}>
            Note: Web Bluetooth requires HTTPS
          </p>
        </>
      ) : (
        <>
          <div className="success-message">
            ✓ Muse 2 headset connected successfully!
          </div>

          <div className="input-group">
            <label htmlFor="duration">Recording Duration (seconds)</label>
            <input
              id="duration"
              type="number"
              min="1"
              max="300"
              value={duration}
              onChange={(e) => setDuration(parseInt(e.target.value) || 0)}
            />
            <p style={{ color: '#666', fontSize: '0.9rem', marginTop: '5px' }}>
              Default: 10 seconds (Range: 1-300 seconds)
            </p>
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="button-group">
            <button className="button" onClick={handleStart}>
              Start Recording Session
            </button>
          </div>

          <p style={{ color: '#666', marginTop: '30px', textAlign: 'center', maxWidth: '500px' }}>
            You will have a preparation phase before the recording begins,
            allowing you to settle and prepare for data collection.
          </p>
        </>
      )}
    </div>
  );
}

