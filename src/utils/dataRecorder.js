// Utility for recording EEG data from Muse device

export class EEGDataRecorder {
  constructor() {
    this.recordedData = [];
    this.isRecording = false;
    this.startTime = null;
    this.intervalId = null;
    this.sampleRate = 256; // Muse 2 samples at 256 Hz
  }

  start(museDevice, onProgress) {
    if (this.isRecording) {
      return;
    }

    this.recordedData = [];
    this.isRecording = true;
    this.startTime = Date.now();

    // Record EEG data at approximately the sample rate
    this.intervalId = setInterval(() => {
      if (!museDevice || !museDevice.eeg) {
        return;
      }

      // Read from all 4 main EEG channels (TP9, AF7, AF8, TP10)
      const sample = {
        timestamp: Date.now() - this.startTime,
        channels: [
          museDevice.eeg[0].read() || 0,
          museDevice.eeg[1].read() || 0,
          museDevice.eeg[2].read() || 0,
          museDevice.eeg[3].read() || 0,
        ],
      };

      this.recordedData.push(sample);

      if (onProgress) {
        onProgress(this.recordedData.length);
      }
    }, 1000 / this.sampleRate);
  }

  stop() {
    if (!this.isRecording) {
      return this.recordedData;
    }

    this.isRecording = false;
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }

    return this.recordedData;
  }

  getData() {
    return this.recordedData;
  }

  getChannelData(channelIndex) {
    return this.recordedData.map((sample) => ({
      timestamp: sample.timestamp,
      value: sample.channels[channelIndex],
    }));
  }

  getDuration() {
    if (this.recordedData.length === 0) {
      return 0;
    }
    const lastSample = this.recordedData[this.recordedData.length - 1];
    return lastSample.timestamp / 1000; // Convert to seconds
  }
}
