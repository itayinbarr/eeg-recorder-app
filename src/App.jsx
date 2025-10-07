import React, { useState, useRef } from 'react';
import { connectMuse } from '../web-muse/src/lib/MuseDevice';
import { EEGDataRecorder } from './utils/dataRecorder';
import SetupPhase from './components/SetupPhase';
import PreparationPhase from './components/PreparationPhase';
import RecordingPhase from './components/RecordingPhase';
import ResultsPhase from './components/ResultsPhase';

const PHASES = {
  SETUP: 'setup',
  PREPARATION: 'preparation',
  RECORDING: 'recording',
  RESULTS: 'results',
};

export default function App() {
  const [currentPhase, setCurrentPhase] = useState(PHASES.SETUP);
  const [duration, setDuration] = useState(10);
  const [recordedData, setRecordedData] = useState(null);
  
  const museDeviceRef = useRef(null);
  const recorderRef = useRef(new EEGDataRecorder());

  const handleConnect = async () => {
    try {
      const muse = await connectMuse();
      museDeviceRef.current = muse;
      console.log('Muse device connected:', muse);
    } catch (error) {
      console.error('Failed to connect to Muse:', error);
      throw error;
    }
  };

  const handleStartSession = (recordingDuration) => {
    setDuration(recordingDuration);
    setCurrentPhase(PHASES.PREPARATION);
  };

  const handlePreparationComplete = () => {
    // Start recording
    if (museDeviceRef.current) {
      recorderRef.current.start(museDeviceRef.current, (sampleCount) => {
        // Optional: track progress
      });
      setCurrentPhase(PHASES.RECORDING);
    } else {
      console.error('Muse device not connected');
    }
  };

  const handleRecordingComplete = () => {
    // Stop recording
    const data = recorderRef.current.stop();
    setRecordedData(data);
    setCurrentPhase(PHASES.RESULTS);
  };

  const handleRestart = () => {
    setRecordedData(null);
    setCurrentPhase(PHASES.SETUP);
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1>EEG Recorder</h1>
        <p>Record and analyze EEG data from your Muse 2 headset</p>
      </div>

      {currentPhase === PHASES.SETUP && (
        <SetupPhase
          onConnect={handleConnect}
          onStart={handleStartSession}
        />
      )}

      {currentPhase === PHASES.PREPARATION && (
        <PreparationPhase onComplete={handlePreparationComplete} />
      )}

      {currentPhase === PHASES.RECORDING && (
        <RecordingPhase
          duration={duration}
          recorder={recorderRef.current}
          onComplete={handleRecordingComplete}
        />
      )}

      {currentPhase === PHASES.RESULTS && (
        <ResultsPhase
          recordedData={recordedData}
          onRestart={handleRestart}
        />
      )}
    </div>
  );
}

