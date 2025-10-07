import React, { useEffect, useRef } from 'react';

export default function EEGPlot({ recordedData }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current || !recordedData || recordedData.length === 0) {
      return;
    }

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, width, height);

    // Channel configuration
    const channels = [
      { name: 'TP9 (Left Ear)', color: '#667eea' },
      { name: 'AF7 (Left Forehead)', color: '#f093fb' },
      { name: 'AF8 (Right Forehead)', color: '#4caf50' },
      { name: 'TP10 (Right Ear)', color: '#ff9800' },
    ];

    const channelHeight = height / channels.length;
    const offset = 300; // Vertical offset between channels

    // Calculate time axis
    const duration = recordedData[recordedData.length - 1].timestamp;
    const timeStep = duration / width;

    // Draw each channel
    channels.forEach((channel, channelIdx) => {
      const baselineY = (channelIdx + 0.5) * channelHeight;

      // Draw channel label and baseline
      ctx.fillStyle = '#333';
      ctx.font = '14px sans-serif';
      ctx.fillText(channel.name, 10, baselineY - offset / 2 + 5);

      ctx.strokeStyle = '#e0e0e0';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(0, baselineY);
      ctx.lineTo(width, baselineY);
      ctx.stroke();

      // Draw EEG signal
      ctx.strokeStyle = channel.color;
      ctx.lineWidth = 1.5;
      ctx.beginPath();

      let started = false;
      recordedData.forEach((sample, idx) => {
        const x = (sample.timestamp / duration) * width;
        const value = sample.channels[channelIdx];
        // Scale the value to fit within the channel height
        const y = baselineY - (value / offset) * (channelHeight * 0.4);

        if (!started) {
          ctx.moveTo(x, y);
          started = true;
        } else {
          ctx.lineTo(x, y);
        }
      });

      ctx.stroke();
    });

    // Draw time axis
    ctx.strokeStyle = '#333';
    ctx.fillStyle = '#333';
    ctx.font = '12px sans-serif';
    ctx.lineWidth = 1;

    const numTicks = 10;
    for (let i = 0; i <= numTicks; i++) {
      const x = (i / numTicks) * width;
      const time = (i / numTicks) * (duration / 1000); // Convert to seconds

      ctx.beginPath();
      ctx.moveTo(x, height - 20);
      ctx.lineTo(x, height - 15);
      ctx.stroke();

      ctx.fillText(time.toFixed(1) + 's', x - 15, height - 5);
    }

    // Draw axis line
    ctx.beginPath();
    ctx.moveTo(0, height - 20);
    ctx.lineTo(width, height - 20);
    ctx.stroke();

  }, [recordedData]);

  return (
    <canvas
      ref={canvasRef}
      width={1000}
      height={600}
      style={{
        width: '100%',
        maxWidth: '1000px',
        height: 'auto',
        border: '1px solid #e0e0e0',
        borderRadius: '10px',
        background: '#ffffff',
      }}
    />
  );
}

