# EEG Post-Processing Pipeline

Complete Python pipeline for processing EEG recordings from Muse 2 headset.

## Features

- ✅ **CSV to EDF Conversion**: Convert recorded CSV files to EDF format
- 🧹 **Preprocessing**: AutoReject for automatic bad epoch detection and removal
- 📊 **Power Spectral Density**: Welch's method with configurable window and overlap
- 🎵 **Band Power Analysis**: Delta, Theta, Alpha, Beta, Gamma bands
- 📈 **Clinical Ratios**: DAR (Delta/Alpha Ratio) and TAR (Theta/Alpha Ratio)
- 💾 **Results Export**: Comprehensive CSV output with all metrics

## Installation

1. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
cd post-recording
pip install -r requirements.txt
```

## Quick Start

### Process a Single Recording

The easiest way to process an EEG recording is using the main pipeline script:

```bash
python process_eeg.py ../data/eeg_recording_2025-10-07T22-30-47.csv
```

This will:

1. Convert CSV to EDF format (extracts AF7 and AF8 frontal electrodes only)
2. Apply preprocessing with artifact rejection (skips AutoReject for 2-channel data)
3. Compute PSD using Welch's method (2s window, 1s overlap)
4. Calculate band powers for all frequency bands (Delta, Theta, Alpha, Beta, Gamma)
5. Calculate DAR and TAR ratios (per-electrode and averaged across AF7 and AF8 only)
6. Save results to CSV files and generate summary plots

### Specify Output Directory

```bash
python process_eeg.py ../data/eeg_recording.csv ../data/results/
```

## Output Files

The pipeline generates the following files:

1. **`<filename>.edf`**: Converted EEG data in EDF format
2. **`<filename>_band_powers.csv`**: Detailed results with columns:

   - `epoch`: Epoch number
   - `channel`: Channel name (AF7, AF8 - frontal electrodes only)
   - `delta_power`: Delta band power (1.0-4 Hz)
   - `theta_power`: Theta band power (4-8 Hz)
   - `alpha_power`: Alpha band power (8-13 Hz)
   - `beta_power`: Beta band power (13-30 Hz)
   - `gamma_power`: Gamma band power (30-50 Hz)
   - `DAR`: Delta/Alpha Ratio
   - `TAR`: Theta/Alpha Ratio

3. **`<filename>_summary.csv`**: Summary statistics averaged by channel

4. **`<filename>_summary_plot.png`**: 4-subplot visualization showing:

   - Raw EEG signal (AF7, AF8 frontal electrodes on same scale)
   - Filtered EEG (after bandpass 1.0-50 Hz)
   - PSD before artifact removal
   - PSD after cleaning with frequency bands highlighted

## Individual Scripts

You can also run individual processing steps:

### 1. CSV to EDF Conversion

```bash
python csv_to_edf.py ../data/eeg_recording.csv output.edf
```

### 2. Preprocessing Only

```bash
python preprocessing.py ../data/eeg_recording.csv
```

### 3. PSD Analysis

```bash
python psd_analysis.py ../data/eeg_recording.csv output_results.csv
```

### 4. Batch Processing

Process multiple recordings at once:

```bash
python batch_process.py ../data/ ../data/results/
```

This will process all `eeg_recording_*.csv` files in the directory.

## Processing Parameters

### Welch PSD Parameters

- **Window length**: 2 seconds (512 samples at 256 Hz)
- **Overlap**: 1 second (256 samples)
- **Frequency range**: 1.0-40 Hz

### Frequency Bands

- **Delta**: 1.0-4 Hz
- **Theta**: 4-8 Hz
- **Alpha**: 8-13 Hz
- **Beta**: 13-30 Hz
- **Gamma**: 30-40 Hz

### Preprocessing

- **Bandpass filter**: 1.0-40 Hz
- **Epoch duration**: 2 seconds
- **AutoReject**: Automatic bad channel interpolation and epoch rejection
- **Amplitude threshold**: Automatic calculation based on data distribution

## Understanding the Output

### Band Powers

Band powers are reported in µV² (microvolt squared). Higher values indicate more activity in that frequency band.

### DAR (Delta/Alpha Ratio)

- Ratio of Delta power to Alpha power
- Higher values may indicate drowsiness or reduced alertness
- Commonly used in clinical applications

### TAR (Theta/Alpha Ratio)

- Ratio of Theta power to Alpha power
- Used in attention and cognitive load studies
- Higher values may indicate mental fatigue

## Data Quality

The pipeline automatically handles data quality:

1. **AutoReject**: Identifies and interpolates bad channels
2. **Epoch Rejection**: Removes epochs with extreme artifacts
3. **Bad Epoch Removal**: Additional amplitude-based rejection

Typical rejection rates of 10-30% are normal and indicate good quality control.

## Channel Locations

The pipeline analyzes the 2 frontal electrodes from the Muse 2 headset:

- **AF7**: Left frontal (left forehead) - Used for analysis
- **AF8**: Right frontal (right forehead) - Used for analysis

Note: TP9 (left ear) and TP10 (right ear) are excluded from analysis as they are primarily reference electrodes and more susceptible to artifacts.

## Example Output

```
Processing Statistics:
  Original epochs: 5
  Epochs after cleaning: 4
  Rejection rate: 20.0%
  Final duration: 8.0s

Band Powers (averaged across epochs and channels, µV²):
  Delta   : 1022 ± 456
  Theta   : 508 ± 321
  Alpha   : 347 ± 210
  Beta    : 2252 ± 1230
  Gamma   : 71421 ± 12500

Power Ratios (averaged across epochs and channels - AF7, AF8 only):
  DAR (Delta/Alpha): 2.534 ± 0.523
  TAR (Theta/Alpha): 1.202 ± 0.412
```

## Troubleshooting

### Import Errors

Make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Memory Issues

For very long recordings, the pipeline processes data in epochs to manage memory efficiently.

### Sampling Rate Issues

The pipeline automatically detects sampling rate from timestamps. Irregular sampling is handled through interpolation.

### Too Many Rejected Epochs

If rejection rate is >50%, consider:

- Checking electrode contact quality
- Reducing recording duration
- Reviewing raw data for systematic artifacts

## Advanced Usage

### Custom Frequency Bands

Edit `FREQ_BANDS` in `psd_analysis.py`:

```python
FREQ_BANDS = {
    'custom_band': (5, 10),  # 5-10 Hz
    # ... other bands
}
```

### Different Window Parameters

Modify the parameters in `process_eeg.py`:

```python
psds, freqs = compute_psd_welch(
    epochs_clean,
    window_sec=4.0,      # 4 second window
    overlap_sec=2.0      # 2 second overlap
)
```

### Apply ICA

Enable ICA in preprocessing:

```python
epochs_clean, _ = preprocess_raw(
    raw,
    apply_ica=True  # Enable ICA
)
```

## File Structure

```
post-recording/
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── install.sh               # Installation script
├── process_eeg.py           # Main pipeline script
├── batch_process.py         # Batch processing script
├── csv_to_edf.py            # CSV to EDF converter
├── preprocessing.py          # Preprocessing with autoreject
├── psd_analysis.py          # PSD and band power analysis
└── visualization.py         # Plot generation utilities
```

## References

- **MNE-Python**: Gramfort et al. (2013). MEG and EEG data analysis with MNE-Python. Frontiers in Neuroscience.
- **AutoReject**: Jas et al. (2017). Autoreject: Automated artifact rejection for MEG and EEG data. NeuroImage.
- **Welch's Method**: Welch (1967). The use of fast Fourier transform for the estimation of power spectra. IEEE Transactions on Audio and Electroacoustics.

## License

ISC

## Support

For issues or questions about the post-processing pipeline, please check:

1. Data format matches expected CSV structure
2. All dependencies are installed
3. Python version is 3.8 or higher
