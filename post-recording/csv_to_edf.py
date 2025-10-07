"""
Convert CSV EEG recordings to EDF format.
"""

import numpy as np
import pandas as pd
import mne
from pathlib import Path


def csv_to_edf(csv_path, output_path=None):
    """
    Convert CSV EEG recording to EDF format.
    
    Parameters
    ----------
    csv_path : str or Path
        Path to the CSV file
    output_path : str or Path, optional
        Path for the output EDF file. If None, uses same name with .edf extension
    
    Returns
    -------
    raw : mne.io.Raw
        MNE Raw object containing the EEG data
    """
    csv_path = Path(csv_path)
    
    if output_path is None:
        output_path = csv_path.with_suffix('.edf')
    else:
        output_path = Path(output_path)
    
    # Read CSV
    print(f"Reading CSV file: {csv_path}")
    df = pd.read_csv(csv_path)
    
    # Extract channel names and data - ONLY FRONTAL ELECTRODES (AF7, AF8)
    all_channel_names = ['TP9', 'AF7', 'AF8', 'TP10']
    channel_names = ['AF7', 'AF8']  # Only frontal electrodes
    channel_indices = [1, 2]  # AF7 is column 2, AF8 is column 3 (0-indexed: 1, 2)
    
    # Get timestamps and calculate sampling frequency
    timestamps = df['Timestamp (ms)'].values / 1000.0  # Convert to seconds
    time_diffs = np.diff(timestamps)
    mean_diff = np.mean(time_diffs)
    calculated_sfreq = 1.0 / mean_diff if mean_diff > 0 else 256.0
    
    # Round to nearest standard EEG sampling rate for EDF compatibility
    # Common rates: 250, 256, 500, 512 Hz
    standard_rates = [250, 256, 500, 512]
    sfreq = min(standard_rates, key=lambda x: abs(x - calculated_sfreq))
    
    print(f"Calculated sampling frequency: {calculated_sfreq:.2f} Hz")
    print(f"Rounded to standard rate: {sfreq} Hz (for EDF compatibility)")
    print(f"Mean sampling interval: {mean_diff*1000:.2f} ms")
    print(f"Using frontal electrodes only: {channel_names}")
    
    # Extract EEG data (in microvolts) - only AF7 and AF8
    data = df.iloc[:, [i+1 for i in channel_indices]].values.T  # Transpose to (n_channels, n_samples)
    
    # Convert from microvolts to volts (MNE expects volts)
    data = data * 1e-6
    
    print(f"Data shape: {data.shape} (channels x samples)")
    print(f"Duration: {timestamps[-1]:.2f} seconds")
    
    # Create MNE info structure
    info = mne.create_info(
        ch_names=channel_names,
        sfreq=sfreq,
        ch_types='eeg'
    )
    
    # Set montage for Muse 2 electrode positions
    # Standard 10-20 positions for these electrodes
    montage = mne.channels.make_standard_montage('standard_1020')
    
    # Create Raw object
    raw = mne.io.RawArray(data, info)
    raw.set_montage(montage, match_case=False, on_missing='ignore')
    
    # Resample to exact integer rate if needed for EDF compatibility
    if calculated_sfreq != sfreq:
        print(f"Resampling from {calculated_sfreq:.2f} Hz to {sfreq} Hz for EDF compatibility...")
        raw.resample(sfreq, npad='auto')
    
    # Add reference information
    raw.info['description'] = 'Muse 2 EEG Recording'
    
    # Export to EDF
    print(f"Saving EDF file: {output_path}")
    mne.export.export_raw(output_path, raw, fmt='edf', overwrite=True)
    
    print("✓ Conversion complete!")
    
    return raw


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python csv_to_edf.py <input_csv> [output_edf]")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    raw = csv_to_edf(csv_file, output_file)
    print(f"\nData info:")
    print(raw.info)

