"""
Power Spectral Density analysis using Welch's method.
"""

import numpy as np
import pandas as pd
import mne
from scipy import signal


# Frequency bands definition
FREQ_BANDS = {
    'delta': (0.5, 4),
    'theta': (4, 8),
    'alpha': (8, 13),
    'beta': (13, 30),
    'gamma': (30, 40)
}


def compute_psd_welch(epochs, fmin=0.5, fmax=40, window_sec=2.0, overlap_sec=1.0):
    """
    Compute Power Spectral Density using Welch's method.
    
    Parameters
    ----------
    epochs : mne.Epochs
        Epoched EEG data
    fmin : float
        Minimum frequency of interest (Hz)
    fmax : float
        Maximum frequency of interest (Hz)
    window_sec : float
        Window length for Welch's method in seconds (default: 2.0)
    overlap_sec : float
        Overlap between windows in seconds (default: 1.0)
    
    Returns
    -------
    psds : ndarray
        Power spectral densities (n_epochs, n_channels, n_freqs)
    freqs : ndarray
        Frequencies corresponding to PSD values
    """
    print("\n" + "=" * 60)
    print("COMPUTING POWER SPECTRAL DENSITY (Welch's Method)")
    print("=" * 60)
    
    sfreq = epochs.info['sfreq']
    n_fft = int(window_sec * sfreq)
    n_overlap = int(overlap_sec * sfreq)
    
    print(f"\nParameters:")
    print(f"  Sampling frequency: {sfreq} Hz")
    print(f"  Window length: {window_sec}s ({n_fft} samples)")
    print(f"  Overlap: {overlap_sec}s ({n_overlap} samples)")
    print(f"  Frequency range: {fmin}-{fmax} Hz")
    
    # Compute PSD using MNE's implementation of Welch
    # API changed in MNE 1.6+
    try:
        # Try new API (MNE 1.6+)
        spectrum = epochs.compute_psd(
            method='welch',
            fmin=fmin,
            fmax=fmax,
            n_fft=n_fft,
            n_overlap=n_overlap,
            n_per_seg=n_fft,
            verbose=False
        )
        psds = spectrum.get_data()
        freqs = spectrum.freqs
    except AttributeError:
        # Fall back to old API (MNE < 1.6)
        psds, freqs = mne.time_frequency.psd_welch(
            epochs,
            fmin=fmin,
            fmax=fmax,
            n_fft=n_fft,
            n_overlap=n_overlap,
            n_per_seg=n_fft,
            verbose=False
        )
    
    # Convert from V²/Hz to µV²/Hz (MNE works in volts internally)
    psds = psds * 1e12  # V² to µV²
    
    print(f"\nOutput shape:")
    print(f"  PSDs: {psds.shape} (epochs × channels × frequencies)")
    print(f"  Frequencies: {len(freqs)} points from {freqs[0]:.2f} to {freqs[-1]:.2f} Hz")
    
    print("\n✓ PSD computation complete!")
    print("=" * 60)
    
    return psds, freqs


def compute_band_powers(psds, freqs, bands=None):
    """
    Compute absolute power in frequency bands.
    
    Parameters
    ----------
    psds : ndarray
        Power spectral densities (n_epochs, n_channels, n_freqs)
    freqs : ndarray
        Frequencies corresponding to PSD values
    bands : dict, optional
        Dictionary of frequency bands. If None, uses default bands.
    
    Returns
    -------
    band_powers : dict
        Dictionary with band names as keys and power arrays as values
        Each array has shape (n_epochs, n_channels)
    """
    if bands is None:
        bands = FREQ_BANDS
    
    print("\n" + "=" * 60)
    print("COMPUTING BAND POWERS")
    print("=" * 60)
    
    band_powers = {}
    
    for band_name, (fmin, fmax) in bands.items():
        # Find frequency indices for this band
        freq_mask = (freqs >= fmin) & (freqs <= fmax)
        
        # Integrate power in this band (sum across frequencies)
        # Using trapezoidal integration for more accurate results
        freq_res = freqs[1] - freqs[0]
        band_power = np.trapz(psds[:, :, freq_mask], dx=freq_res, axis=2)
        
        band_powers[band_name] = band_power
        
        # Print statistics
        mean_power = np.mean(band_power)
        print(f"\n{band_name.upper()} ({fmin}-{fmax} Hz):")
        print(f"  Mean power: {mean_power:.2f} µV²")
        print(f"  Shape: {band_power.shape} (epochs × channels)")
    
    print("\n✓ Band power computation complete!")
    print("=" * 60)
    
    return band_powers


def compute_ratios(band_powers):
    """
    Compute DAR (Delta/Alpha Ratio) and TAR (Theta/Alpha Ratio).
    
    Parameters
    ----------
    band_powers : dict
        Dictionary of band powers from compute_band_powers
    
    Returns
    -------
    ratios : dict
        Dictionary containing DAR and TAR arrays (n_epochs, n_channels)
    """
    print("\n" + "=" * 60)
    print("COMPUTING POWER RATIOS")
    print("=" * 60)
    
    # Add small epsilon to avoid division by zero
    epsilon = 1e-10
    
    delta = band_powers['delta']
    theta = band_powers['theta']
    alpha = band_powers['alpha']
    
    dar = delta / (alpha + epsilon)
    tar = theta / (alpha + epsilon)
    
    ratios = {
        'DAR': dar,
        'TAR': tar
    }
    
    print(f"\nDAR (Delta/Alpha Ratio):")
    print(f"  Mean: {np.mean(dar):.3f}")
    print(f"  Std: {np.std(dar):.3f}")
    print(f"  Range: [{np.min(dar):.3f}, {np.max(dar):.3f}]")
    
    print(f"\nTAR (Theta/Alpha Ratio):")
    print(f"  Mean: {np.mean(tar):.3f}")
    print(f"  Std: {np.std(tar):.3f}")
    print(f"  Range: [{np.min(tar):.3f}, {np.max(tar):.3f}]")
    
    print("\n✓ Ratio computation complete!")
    print("=" * 60)
    
    return ratios


def create_results_dataframe(epochs, band_powers, ratios):
    """
    Create a pandas DataFrame with all results.
    
    Parameters
    ----------
    epochs : mne.Epochs
        Epoched EEG data (for channel names)
    band_powers : dict
        Dictionary of band powers
    ratios : dict
        Dictionary of power ratios
    
    Returns
    -------
    df : pd.DataFrame
        DataFrame with all power and ratio values
    """
    ch_names = epochs.ch_names
    n_epochs = len(epochs)
    
    results = []
    
    for epoch_idx in range(n_epochs):
        for ch_idx, ch_name in enumerate(ch_names):
            row = {
                'epoch': epoch_idx,
                'channel': ch_name,
                'delta_power': band_powers['delta'][epoch_idx, ch_idx],
                'theta_power': band_powers['theta'][epoch_idx, ch_idx],
                'alpha_power': band_powers['alpha'][epoch_idx, ch_idx],
                'beta_power': band_powers['beta'][epoch_idx, ch_idx],
                'gamma_power': band_powers['gamma'][epoch_idx, ch_idx],
                'DAR': ratios['DAR'][epoch_idx, ch_idx],
                'TAR': ratios['TAR'][epoch_idx, ch_idx],
            }
            results.append(row)
    
    df = pd.DataFrame(results)
    
    return df


if __name__ == "__main__":
    import sys
    from pathlib import Path
    from csv_to_edf import csv_to_edf
    from preprocessing import preprocess_raw
    
    if len(sys.argv) < 2:
        print("Usage: python psd_analysis.py <input_csv_or_edf> [output_csv]")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output_csv = sys.argv[2] if len(sys.argv) > 2 else input_file.stem + '_psd_results.csv'
    
    # Load data
    if input_file.suffix == '.csv':
        print("Loading CSV and converting to MNE format...")
        raw = csv_to_edf(input_file)
    else:
        print("Loading EDF file...")
        raw = mne.io.read_raw_edf(input_file, preload=True)
    
    # Preprocess
    epochs_clean, _ = preprocess_raw(raw, epoch_duration=2.0)
    
    # Compute PSD
    psds, freqs = compute_psd_welch(epochs_clean, window_sec=2.0, overlap_sec=1.0)
    
    # Compute band powers
    band_powers = compute_band_powers(psds, freqs)
    
    # Compute ratios
    ratios = compute_ratios(band_powers)
    
    # Create results DataFrame
    df = create_results_dataframe(epochs_clean, band_powers, ratios)
    
    # Save to CSV
    print(f"\nSaving results to: {output_csv}")
    df.to_csv(output_csv, index=False)
    print("✓ Results saved!")
    
    # Print summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS (averaged across epochs and channels)")
    print("=" * 60)
    print("\nBand Powers (µV²):")
    for band in ['delta', 'theta', 'alpha', 'beta', 'gamma']:
        col = f"{band}_power"
        print(f"  {band.capitalize():8s}: {df[col].mean():.2e} ± {df[col].std():.2e}")
    
    print("\nPower Ratios:")
    print(f"  DAR: {df['DAR'].mean():.3f} ± {df['DAR'].std():.3f}")
    print(f"  TAR: {df['TAR'].mean():.3f} ± {df['TAR'].std():.3f}")

