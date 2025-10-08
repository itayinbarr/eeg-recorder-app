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


