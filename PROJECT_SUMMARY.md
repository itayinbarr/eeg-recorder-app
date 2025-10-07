# Project Summary: EEG Recorder App with Post-Processing Pipeline

## 🎉 Complete EEG Recording & Analysis System

A production-ready, open-source solution for recording and analyzing EEG data from the Muse 2 headset. Built with [web-muse](https://github.com/itayinbarr/web-muse) for seamless Web Bluetooth connectivity and powered by scientific-grade analysis tools.

## 📦 What Was Built

### 1. **React Recording App** (Web-based)

A beautiful, modern web application for recording EEG data:

- ✅ Web Bluetooth connectivity to Muse 2
- ✅ Configurable recording duration (1-300 seconds, default: 10s)
- ✅ Preparation phase with countdown and tips
- ✅ Real-time recording with progress tracking
- ✅ Beautiful multi-channel EEG visualization
- ✅ CSV export with all 4 electrodes
- ✅ Statistics and quality metrics

**Location**: `src/` directory  
**Run with**: `npm run dev`  
**Access at**: https://localhost:3000

### 2. **Python Post-Processing Pipeline**

Complete scientific analysis pipeline:

- ✅ CSV to EDF conversion (standard format)
- ✅ AutoReject preprocessing (automatic artifact removal)
- ✅ Welch PSD analysis (2s window, 1s overlap)
- ✅ Band power calculation (Delta, Theta, Alpha, Beta, Gamma)
- ✅ Clinical ratios (DAR, TAR)
- ✅ Batch processing support
- ✅ Comprehensive CSV output

**Location**: `post-recording/` directory  
**Run with**: `python process_eeg.py <csv_file>`

## 🗂️ Project Structure

```
eeg-recorder-app/
├── 📱 React App (Frontend)
│   ├── src/
│   │   ├── App.jsx              # Main application
│   │   ├── components/          # Phase components
│   │   │   ├── SetupPhase.jsx
│   │   │   ├── PreparationPhase.jsx
│   │   │   ├── RecordingPhase.jsx
│   │   │   ├── ResultsPhase.jsx
│   │   │   └── EEGPlot.jsx
│   │   ├── utils/
│   │   │   ├── dataRecorder.js  # EEG data recording
│   │   │   └── csvExport.js     # CSV generation
│   │   └── styles.css           # Modern UI styling
│   ├── vite.config.js           # Vite + HTTPS config
│   └── package.json
│
├── 🔬 Python Post-Processing
│   ├── process_eeg.py          # Main pipeline (all-in-one)
│   ├── batch_process.py        # Process multiple files
│   ├── csv_to_edf.py           # Format conversion
│   ├── preprocessing.py        # AutoReject + filtering
│   ├── psd_analysis.py         # PSD + band powers
│   ├── install.sh              # One-click setup
│   ├── requirements.txt        # Python dependencies
│   └── README.md               # Detailed docs
│
├── 🎧 Web Muse Library
│   └── web-muse/               # Muse 2 Bluetooth library
│       ├── src/lib/
│       │   ├── MuseDevice.js
│       │   ├── CircularBuffer.js
│       │   └── eeg.js
│       └── docs/API.md
│
├── 💾 Data Directory
│   └── data/                   # Your recordings
│
└── 📚 Documentation
    ├── README.md               # Main documentation
    ├── QUICKSTART.md           # 10-minute guide
    └── PROJECT_SUMMARY.md      # This file
```

## 🚀 Quick Start Commands

### Recording

```bash
npm run dev
# Open https://localhost:3000
```

### Processing

```bash
cd post-recording
./install.sh
source venv/bin/activate
python process_eeg.py ../data/eeg_recording_*.csv
```

## 📊 Output Files

### From Web App

- `eeg_recording_<timestamp>.csv` - Raw EEG data with 4 channels

### From Post-Processing

- `<filename>.edf` - Standard EDF format (universal compatibility)
- `<filename>_band_powers.csv` - Detailed epoch-by-epoch results
- `<filename>_summary.csv` - Channel-averaged statistics

## 🎓 Key Features

### Recording App Features

1. **Bluetooth Web Integration** - No drivers, works in browser
2. **Professional UI** - Modern, gradient design with animations
3. **Guided Workflow** - 4 phases: Setup → Preparation → Recording → Results
4. **Real-time Visualization** - Canvas-based multi-channel plot
5. **Quality Feedback** - Live statistics and validation

### Post-Processing Features

1. **Automatic Quality Control** - AutoReject removes bad epochs
2. **Standard Format Support** - EDF export for other tools
3. **Clinical Metrics** - DAR and TAR ratios
4. **Flexible Parameters** - Customizable windows and bands
5. **Batch Processing** - Process multiple files at once

## 📈 Analysis Outputs

### Band Powers (Absolute, µV²)

- **Delta (0.5-4 Hz)**: Sleep, deep relaxation
- **Theta (4-8 Hz)**: Meditation, creativity
- **Alpha (8-13 Hz)**: Relaxed wakefulness
- **Beta (13-30 Hz)**: Active thinking, focus
- **Gamma (30-50 Hz)**: Cognitive processing

### Clinical Ratios

- **DAR (Delta/Alpha)**: Alertness indicator
- **TAR (Theta/Alpha)**: Attention/fatigue marker

## 🔧 Technical Specifications

### Recording

- **Sampling Rate**: ~256 Hz (auto-detected)
- **Channels**: 4 (TP9, AF7, AF8, TP10)
- **Data Format**: CSV with timestamps
- **Units**: Microvolts (µV)

### Processing

- **Preprocessing**: 0.5-50 Hz bandpass filter
- **Epoch Duration**: 2 seconds
- **PSD Method**: Welch with 2s window, 1s overlap
- **Artifact Removal**: AutoReject + amplitude thresholding

## 🌐 Browser Compatibility

| Browser | Recording App | Reason                     |
| ------- | ------------- | -------------------------- |
| Chrome  | ✅ Yes        | Full Web Bluetooth support |
| Edge    | ✅ Yes        | Full Web Bluetooth support |
| Opera   | ✅ Yes        | Full Web Bluetooth support |
| Firefox | ❌ No         | No Web Bluetooth           |
| Safari  | ❌ No         | No Web Bluetooth           |

## 📦 Dependencies

### Frontend

- React 18
- Vite (with HTTPS)
- vite-plugin-mkcert (SSL certificates)

### Backend/Analysis

- Python 3.8+
- MNE-Python (EEG analysis)
- AutoReject (artifact removal)
- NumPy, Pandas, SciPy
- PyEDFLib (EDF export)

## 🎯 Use Cases

1. **Research**: Collect EEG data for experiments
2. **Neurofeedback**: Real-time brain state monitoring
3. **Meditation Training**: Track alpha/theta states
4. **Cognitive Studies**: Analyze attention and focus
5. **Education**: Learn about brain signals
6. **Clinical**: Preliminary screening (not for diagnosis)

## 📝 Sample Workflow

1. **Prepare**: Fit Muse 2 headset, ensure good contact
2. **Connect**: Open web app, connect via Bluetooth
3. **Configure**: Set recording duration (e.g., 60 seconds)
4. **Record**: Follow preparation phase, stay still
5. **Export**: Download CSV to data folder
6. **Analyze**: Run post-processing pipeline
7. **Interpret**: Review band powers and ratios
8. **Iterate**: Record more sessions, compare results

## 🔬 Scientific Validity

### Quality Assurance

- ✅ Standard frequency bands (peer-reviewed definitions)
- ✅ Welch's method (gold standard for PSD)
- ✅ AutoReject (validated artifact removal)
- ✅ EDF export (universal format)
- ✅ Proper preprocessing (filtering, epoching)

### Limitations

- ⚠️ Consumer-grade device (not clinical)
- ⚠️ Limited channels (4 vs 64+ in research)
- ⚠️ Not for medical diagnosis
- ⚠️ Best for relative comparisons within-subject

## 📚 Documentation

- **[README.md](README.md)** - Full project documentation
- **[QUICKSTART.md](QUICKSTART.md)** - 10-minute getting started
- **[post-recording/README.md](post-recording/README.md)** - Analysis details
- **[web-muse/docs/API.md](web-muse/docs/API.md)** - Device API reference

## 🎉 What Makes This Special

1. **End-to-End Solution**: From recording to publication-ready analysis
2. **Web-Based**: No software installation for recording
3. **Scientific Rigor**: Validated methods and automatic QC
4. **User-Friendly**: Beautiful UI with guided workflow
5. **Open Source**: Fully transparent and customizable
6. **Production Ready**: Proper error handling and validation
7. **Well Documented**: Comprehensive guides and examples

## 🚀 Next Steps

### Immediate

- [x] Record your first EEG session
- [ ] Process the recording
- [ ] Review the results
- [ ] Experiment with different conditions

### Advanced

- [ ] Batch process multiple sessions
- [ ] Compare eyes-open vs eyes-closed
- [ ] Track meditation progress
- [ ] Analyze attention during tasks
- [ ] Export to other analysis tools

### Customization

- [ ] Modify frequency bands for specific research
- [ ] Add custom visualization
- [ ] Implement real-time feedback
- [ ] Add more clinical ratios

## 💡 Tips for Success

1. **Good Contact**: Moisten electrodes if needed
2. **Stay Still**: Minimize movement during recording
3. **Consistent Conditions**: Same environment for comparisons
4. **Longer Recordings**: 60+ seconds for stable estimates
5. **Multiple Sessions**: Track changes over time

## 🤝 Contributing

This is a complete, working system, but there's always room for improvement! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Ideas for contributions:

- Real-time frequency band visualization
- Mobile browser optimization
- Additional analysis metrics
- Better error handling
- UI/UX improvements
- Documentation and tutorials

## 📚 Key Technologies

- **[web-muse](https://github.com/itayinbarr/web-muse)**: Modern, actively maintained Muse connectivity library
- **[React 18](https://react.dev/)**: Modern UI framework
- **[Web Bluetooth API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API)**: Direct device-to-browser connection
- **[MNE-Python](https://mne.tools/)**: Gold-standard EEG analysis library
- **[AutoReject](https://autoreject.github.io/)**: Automated artifact removal
- **[Vite](https://vitejs.dev/)**: Fast development server with HTTPS support

## 📄 License

ISC License - Free and open source. See [LICENSE](LICENSE) for details.

---

**Ready to explore your brain?** Start recording and analyzing your brain activity today! 🧠✨

Questions? Open an [issue](https://github.com/itayinbarr/eeg-recorder-app/issues) or start a [discussion](https://github.com/itayinbarr/eeg-recorder-app/discussions)!
