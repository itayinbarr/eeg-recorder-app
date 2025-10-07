import React from 'react';
import { exportToCSV, getCSVStats } from '../utils/csvExport';
import EEGPlot from './EEGPlot';

export default function ResultsPhase({ recordedData, onRestart }) {
  const stats = getCSVStats(recordedData);

  const handleExport = () => {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
    const filename = `eeg_recording_${timestamp}.csv`;
    exportToCSV(recordedData, filename);
  };

  if (!recordedData || recordedData.length === 0) {
    return (
      <div className="phase-container">
        <h2 style={{ fontSize: '2rem', color: '#333', marginBottom: '30px' }}>
          No Data Recorded
        </h2>
        <p style={{ color: '#666', marginBottom: '30px' }}>
          Something went wrong during the recording. Please try again.
        </p>
        <button className="button" onClick={onRestart}>
          Start New Recording
        </button>
      </div>
    );
  }

  return (
    <div className="phase-container">
      <h2 style={{ fontSize: '2rem', color: '#333', marginBottom: '30px' }}>
        Recording Complete
      </h2>

      <div className="success-message">
        ✓ Successfully recorded {stats.totalSamples} samples over {stats.duration} seconds
      </div>

      {/* EEG Plot */}
      <div className="chart-container">
        <h3 style={{ marginBottom: '20px', color: '#333' }}>EEG Signal Visualization</h3>
        <EEGPlot recordedData={recordedData} />
      </div>

      {/* Statistics */}
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Duration</h3>
          <p>{stats.duration}s</p>
        </div>
        <div className="stat-card">
          <h3>Total Samples</h3>
          <p>{stats.totalSamples}</p>
        </div>
        <div className="stat-card">
          <h3>Sample Rate</h3>
          <p>{stats.sampleRate} Hz</p>
        </div>
        <div className="stat-card">
          <h3>Channels</h3>
          <p>4</p>
        </div>
      </div>

      {/* Channel Statistics */}
      <div style={{ width: '100%', marginTop: '30px' }}>
        <h3 style={{ marginBottom: '20px', color: '#333' }}>Channel Statistics</h3>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '15px',
        }}>
          {stats.channels.map((channel) => (
            <div key={channel.name} className="stat-card" style={{ textAlign: 'left' }}>
              <h3 style={{ marginBottom: '10px', fontSize: '1.1rem' }}>{channel.name}</h3>
              <div style={{ fontSize: '0.9rem', color: '#666' }}>
                <p>Mean: <strong>{channel.mean} µV</strong></p>
                <p>Std Dev: <strong>{channel.std} µV</strong></p>
                <p>Min: <strong>{channel.min} µV</strong></p>
                <p>Max: <strong>{channel.max} µV</strong></p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="button-group">
        <button className="button" onClick={handleExport}>
          📥 Download CSV
        </button>
        <button className="button button-secondary" onClick={onRestart}>
          🔄 New Recording
        </button>
      </div>

      <p style={{ color: '#666', marginTop: '20px', fontSize: '0.9rem', textAlign: 'center' }}>
        CSV file includes timestamps and data for all 4 electrodes (TP9, AF7, AF8, TP10)
      </p>
    </div>
  );
}

