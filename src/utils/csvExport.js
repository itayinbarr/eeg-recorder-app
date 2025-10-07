// Utility for exporting EEG data to CSV

export function exportToCSV(recordedData, filename = "eeg_recording.csv") {
  if (!recordedData || recordedData.length === 0) {
    console.error("No data to export");
    return;
  }

  // Create CSV header
  const headers = [
    "Timestamp (ms)",
    "TP9 (left ear)",
    "AF7 (left forehead)",
    "AF8 (right forehead)",
    "TP10 (right ear)",
  ];

  // Create CSV rows
  const rows = recordedData.map((sample) => {
    return [
      sample.timestamp,
      sample.channels[0],
      sample.channels[1],
      sample.channels[2],
      sample.channels[3],
    ].join(",");
  });

  // Combine header and rows
  const csvContent = [headers.join(","), ...rows].join("\n");

  // Create blob and download
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");
  const url = URL.createObjectURL(blob);

  link.setAttribute("href", url);
  link.setAttribute("download", filename);
  link.style.visibility = "hidden";

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  URL.revokeObjectURL(url);
}

export function getCSVStats(recordedData) {
  if (!recordedData || recordedData.length === 0) {
    return null;
  }

  const stats = {
    totalSamples: recordedData.length,
    duration: (recordedData[recordedData.length - 1].timestamp / 1000).toFixed(
      2
    ),
    sampleRate: (
      recordedData.length /
      (recordedData[recordedData.length - 1].timestamp / 1000)
    ).toFixed(2),
    channels: [],
  };

  // Calculate stats for each channel
  const channelNames = ["TP9", "AF7", "AF8", "TP10"];
  for (let i = 0; i < 4; i++) {
    const values = recordedData.map((sample) => sample.channels[i]);
    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    const min = Math.min(...values);
    const max = Math.max(...values);
    const std = Math.sqrt(
      values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) /
        values.length
    );

    stats.channels.push({
      name: channelNames[i],
      mean: mean.toFixed(2),
      std: std.toFixed(2),
      min: min.toFixed(2),
      max: max.toFixed(2),
    });
  }

  return stats;
}
