# 🧠 EEG Recorder App

[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](https://opensource.org/licenses/ISC)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776ab.svg)](https://www.python.org/)
[![Web Bluetooth](https://img.shields.io/badge/Web%20Bluetooth-Enabled-4285f4.svg)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API)

**Record and analyze your brain activity in minutes—no complex software required.**

A complete web-based solution for recording EEG data from the Muse 2 headset and processing it with scientific-grade analysis. Built with [web-muse](https://github.com/itayinbarr/web-muse), this app lets you collect and analyze EEG data entirely in your browser, then dive deeper with our Python post-processing pipeline.

![EEG Processing Pipeline](data/eeg_recording_2025-10-07T22-38-11_summary_plot.png)
_Example output: Raw signal, filtered signal, and power spectral density analysis_

## 📸 App Screenshots

The app guides you through four intuitive phases:

### 1️⃣ Setup Phase - Connect Your Muse 2

<table>
<tr>
<td width="50%">
<img src="screenshots/01-setup-initial.png" alt="Setup Initial" />
<p align="center"><em>Initial setup screen - ready to connect</em></p>
</td>
<td width="50%">
<img src="screenshots/02-setup-connected.png" alt="Setup Connected" />
<p align="center"><em>Connected!</em></p>
</td>
</tr>
</table>

### 2️⃣ Preparation Phase - Get Ready

<img src="screenshots/03-preparation.png" alt="Preparation Phase" width="600" />

_Configure your recording duration_

### 3️⃣ Recording Phase - Capture Your Brain Activity

<img src="screenshots/04-recording.png" alt="Recording Phase" width="600" />

_5-second countdown with helpful tips to ensure quality recording_

### 4️⃣ Results Phase - Visualize & Export

<table>
<tr>
<td width="33%">
<img src="screenshots/05-results-visualization.png" alt="Results Visualization" />
<p align="center"><em>Real-time progress tracking during your recording session</em></p>
</td>
<td width="33%">
<img src="screenshots/06-results-statistics.png" alt="Results Statistics" />
<p align="center"><em>Beautiful EEG visualization</em></p>
</td>
<td width="33%">
<img src="screenshots/07-results-export.png" alt="Results Export" />
<p align="center"><em>Detailed channel statistics, download your data as CSV</em></p>
</td>
</tr>
</table>


## ⚡ Quick Start

### 1. Record EEG (2 minutes)

```bash
npm install
npm run dev
```

Open **https://localhost:3000**, connect your Muse 2, and start recording!

### 2. Analyze Data (3 minutes)

```bash
cd post-recording
./install.sh
source venv/bin/activate
python process_eeg.py ../data/your_recording.csv
```

Get instant results: band powers, clinical ratios, and beautiful visualizations.

→ **[Full Quick Start Guide](QUICKSTART.md)**


## 📋 Prerequisites

- **Hardware**: Muse 2 or Muse S headset
- **Browser**: Chrome, Edge, or Opera (Web Bluetooth required)
- **Software**:
  - Node.js v18+ (for web app)
  - Python 3.8+ (for analysis, optional)

## CSV Format

The exported CSV file contains:

- **Column 1**: Timestamp (milliseconds)
- **Column 2**: TP9 - Left ear (µV)
- **Column 3**: AF7 - Left forehead (µV)
- **Column 4**: AF8 - Right forehead (µV)
- **Column 5**: TP10 - Right ear (µV)

Sample rate: ~256 Hz


## 🔬 Post-Processing Your Recordings

After recording EEG data, process it with our scientific-grade Python pipeline to extract meaningful insights.

### Step-by-Step Guide

#### 1. Install Post-Processing Tools (One Time Only)

```bash
cd post-recording
./install.sh
```

This creates a Python virtual environment and installs all required dependencies (MNE-Python, AutoReject, etc.).

#### 2. Move Your Recording to the Data Folder

After recording in the web app, your CSV file downloads to your Downloads folder. Move it to the `data/` folder:

```bash
# Option A: Using command line
mv ~/Downloads/eeg_recording_*.csv data/

# Option B: Manually
# Drag and drop the CSV file from Downloads into the 'data' folder
```

#### 3. Activate the Python Environment

```bash
source post-recording/venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

#### 4. Run the Processing Pipeline

```bash
python post-recording/process_eeg.py data/eeg_recording_YYYY-MM-DDTHH-MM-SS.csv
```

**Example with actual filename:**

```bash
python post-recording/process_eeg.py data/eeg_recording_2025-10-07T22-30-47.csv
```

**Pro tip:** Use tab completion! Type `python post-recording/process_eeg.py data/eeg_` and press Tab to autocomplete.

#### 5. View Your Results

The pipeline will automatically generate:

- ✅ `<filename>.edf` - Standard EDF format (universal compatibility)
- ✅ `<filename>_band_powers.csv` - Detailed band powers per epoch and channel
- ✅ `<filename>_summary.csv` - Summary statistics averaged by channel
- ✅ `<filename>_summary_plot.png` - 4-panel visualization (see example above)

All files are saved in the same `data/` folder as your input CSV.

### What the Pipeline Does

1. **Converts CSV to EDF** - Standard format compatible with other EEG tools
2. **Applies Bandpass Filter** - 0.5-40 Hz to remove noise
3. **AutoReject Preprocessing** - Automatically detects and removes bad epochs
4. **Welch PSD Analysis** - Calculates power spectral density (2s window, 1s overlap)
5. **Band Power Extraction** - Computes Delta, Theta, Alpha, Beta, Gamma powers
6. **Clinical Ratios** - Calculates DAR and TAR ratios
7. **Generates Visualization** - Creates comprehensive 4-panel summary plot

### Need More Details?

See [post-recording/README.md](post-recording/README.md) for:

- Custom frequency bands
- Advanced parameters
- Troubleshooting
- Individual script usage

## 📁 Project Structure

```
eeg-recorder-app/
├── src/                    # React app source code
│   ├── components/         # React components (4 recording phases)
│   ├── utils/             # Data recording and CSV export utilities
│   ├── App.jsx            # Main app component
│   └── styles.css         # Modern UI styling
├── web-muse/              # Web Bluetooth Muse connectivity library
├── post-recording/        # Python post-processing pipeline
│   ├── process_eeg.py     # Main processing script
│   ├── csv_to_edf.py      # CSV to EDF converter
│   ├── preprocessing.py   # AutoReject preprocessing
│   ├── psd_analysis.py    # PSD and band power analysis
│   ├── visualization.py   # Summary plot generation
│   └── README.md          # Post-processing documentation
├── data/                  # Your recorded EEG data (gitignored)
├── README.md              # This file
├── QUICKSTART.md          # 10-minute getting started guide
└── PROJECT_SUMMARY.md     # Detailed project overview
```

## 💡 Tips for Best Results

### Recording

- Ensure good electrode contact (especially behind the ears)
- Sit still and relax during recording
- Minimize jaw clenching and facial movements
- Record for at least 30-60 seconds for reliable analysis

### Analysis

- Check that epoch rejection rate is <30%
- Compare recordings under similar conditions
- Use longer recordings for more stable power estimates
- Export to EDF format for compatibility with other tools

## 🤝 Contributing

Contributions are welcome! This project aims to make EEG recording accessible to everyone. Feel free to:

- Report bugs or suggest features via GitHub issues
- Submit pull requests with improvements
- Share your use cases and results
- Improve documentation

## 📚 Learn More

- **[QUICKSTART.md](QUICKSTART.md)**: Get recording in 10 minutes
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**: Detailed technical overview
- **[post-recording/README.md](post-recording/README.md)**: Analysis pipeline documentation
- **[web-muse](https://github.com/itayinbarr/web-muse)**: The Muse connectivity library powering this app

## ⚠️ Important Notes

- **Not for Medical Use**: This is a consumer-grade device for research and personal exploration only
- **HTTPS Required**: Web Bluetooth only works over secure connections
- **Data Privacy**: All data stays on your device—nothing is uploaded anywhere
- **Research Tool**: Best for within-subject comparisons and learning about EEG

## 📄 License

ISC License - see LICENSE file for details

## 🙏 Credits

- Built with **[web-muse](https://github.com/itayinbarr/web-muse)** - A modern, actively maintained library for Muse connectivity
- Powered by **[MNE-Python](https://mne.tools/)** - The leading EEG/MEG analysis library
- Artifact removal via **[AutoReject](https://autoreject.github.io/)** - Automated quality control for EEG

---

**Made with ❤️ for the neuroscience and maker communities**

