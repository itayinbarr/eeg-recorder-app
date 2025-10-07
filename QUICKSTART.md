# ⚡ Quick Start Guide

**Get up and running with EEG recording and analysis in 10 minutes!**

No complex software installation. No drivers. Just open your browser and start recording your brain activity.

> Built with [web-muse](https://github.com/itayinbarr/web-muse) for seamless Web Bluetooth connectivity.

## Part 1: Recording EEG Data (5 minutes)

### 1. Install and Run the Web App

```bash
# Install dependencies
npm install

# Start the app
npm run dev
```

Open your browser to **https://localhost:3000**

### 2. Record Your First EEG Session

1. Click **"Connect Muse 2 Headset"**
2. Select your Muse device from the Bluetooth pairing dialog
3. Set recording duration (default: 10 seconds)
4. Click **"Start Recording Session"**
5. Follow the 5-second preparation countdown
6. Stay still during recording
7. View your results and click **"Download CSV"**

Your CSV file will be saved to your Downloads folder!

## Part 2: Analyzing Your Data (5 minutes)

### 1. Set Up Post-Processing (One Time Only)

```bash
cd post-recording
./install.sh
```

This installs all required Python packages (MNE, AutoReject, etc.)

### 2. Move Your Recording to the Data Folder

Your CSV downloads to `~/Downloads/`. Move it to the `data/` folder:

```bash
# Move your downloaded CSV to data folder
mv ~/Downloads/eeg_recording_*.csv data/
```

**Or** manually drag and drop the file from Downloads into the `data/` folder.

### 3. Activate Python Environment

```bash
source post-recording/venv/bin/activate
```

You'll see `(venv)` in your terminal prompt.

### 4. Process Your Recording

```bash
python post-recording/process_eeg.py data/eeg_recording_YYYY-MM-DDTHH-MM-SS.csv
```

**Real example:**

```bash
python post-recording/process_eeg.py data/eeg_recording_2025-10-07T22-30-47.csv
```

**Tip:** Type `python post-recording/process_eeg.py data/eeg_` and press Tab to autocomplete!

### 5. View Your Results

The pipeline outputs 4 files in the `data/` folder:

- ✅ `.edf` - Standard EEG format
- ✅ `_band_powers.csv` - Detailed band powers per epoch
- ✅ `_summary.csv` - Averaged statistics
- ✅ `_summary_plot.png` - Beautiful 4-panel visualization

The terminal will show:

- Preprocessing statistics (epochs kept/rejected)
- Band powers (Delta, Theta, Alpha, Beta, Gamma)
- Clinical ratios (DAR, TAR)

Open the CSV files in Excel, Google Sheets, or your favorite analysis tool!

## What's Next?

### Record More Data

- Try different durations
- Record under different conditions (eyes open/closed, relaxed/focused)
- Compare your results

### Advanced Analysis

- Use the individual scripts for specific analyses
- Batch process multiple recordings
- Customize frequency bands and parameters
- Export to other analysis tools

### Learn More

- [Main README](README.md) - Full documentation
- [Post-Processing README](post-recording/README.md) - Detailed analysis guide
- [Web Muse API](web-muse/docs/API.md) - Low-level device control

## Common Questions

**Q: My connection fails**  
A: Make sure your Muse 2 is powered on, Bluetooth is enabled, and you're using Chrome/Edge/Opera.

**Q: Too many epochs are rejected**  
A: Check electrode contact quality. Try moistening the contacts slightly.

**Q: What do the band powers mean?**  
A: Higher values indicate more activity in that frequency range. Alpha (8-13 Hz) is typically associated with relaxed wakefulness.

**Q: How do I batch process multiple files?**  
A: Use `python batch_process.py ../data/` to process all recordings at once.

## Tips for Best Results

### During Recording

1. Ensure good electrode contact (especially TP9/TP10 behind ears)
2. Sit still and relax
3. Minimize muscle tension (jaw, forehead)
4. Keep eyes steady (blinking is okay)

### For Analysis

1. Record at least 10 seconds for meaningful band power analysis
2. Check preprocessing rejection rates (<30% is good)
3. Compare recordings under similar conditions
4. Use summary statistics for between-session comparisons

## 🎯 What's Next?

### Explore the App

- Try different recording durations
- Compare eyes-open vs eyes-closed states
- Track your meditation progress over time
- Record during different activities

### Dive Deeper

- Read the [full README](README.md) for all features
- Check [post-recording/README.md](post-recording/README.md) for analysis details
- Learn about the [web-muse library](https://github.com/itayinbarr/web-muse) powering connectivity
- Explore the [MNE-Python documentation](https://mne.tools/) for advanced analysis

## 💬 Need Help?

- **Issues**: [GitHub Issues](https://github.com/itayinbarr/eeg-recorder-app/issues)
- **Questions**: [GitHub Discussions](https://github.com/itayinbarr/eeg-recorder-app/discussions)
- **Connectivity**: Check the [web-muse repository](https://github.com/itayinbarr/web-muse)

### Common Troubleshooting

- Ensure Node.js v18+ and Python 3.8+
- Use Chrome, Edge, or Opera (not Firefox/Safari)
- Check Muse 2 battery and firmware
- Verify HTTPS connection (required for Web Bluetooth)

---

**Happy EEG recording!** 🧠✨

Start exploring your brain activity now and share your discoveries with the community!
