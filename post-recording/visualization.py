"""
Visualization utilities for EEG processing results.
"""

import numpy as np
import matplotlib.pyplot as plt
import mne
from pathlib import Path


def create_processing_summary_plot(raw_original, raw_filtered, epochs_clean, 
                                   psds_raw, freqs_raw, psds_clean, freqs_clean,
                                   output_path):
    """
    Create a comprehensive 4-subplot figure showing the processing pipeline.
    
    Parameters
    ----------
    raw_original : mne.io.Raw
        Original raw data
    raw_filtered : mne.io.Raw
        Filtered raw data (after bandpass)
    epochs_clean : mne.Epochs
        Cleaned epochs after artifact removal
    psds_raw : ndarray
        PSD of raw data (before cleaning)
    freqs_raw : ndarray
        Frequencies for raw PSD
    psds_clean : ndarray
        PSD of cleaned data (after artifact removal)
    freqs_clean : ndarray
        Frequencies for cleaned PSD
    output_path : str or Path
        Path to save the figure
    """
    # Create figure with 4 subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('EEG Processing Pipeline Summary', fontsize=16, fontweight='bold')
    
    # Channel information (only frontal electrodes)
    ch_names = raw_original.ch_names
    colors = ['#f093fb', '#4caf50']  # AF7 (pink), AF8 (green)
    
    # Subplot 1: Raw EEG (frontal electrodes only)
    ax1 = axes[0, 0]
    plot_eeg_timeseries(raw_original, ax1, colors, 
                       title='1. Raw EEG Signal (AF7, AF8)',
                       ylabel='Amplitude (µV)')
    
    # Subplot 2: Cleaned EEG after bandpass filtering
    ax2 = axes[0, 1]
    plot_eeg_timeseries(raw_filtered, ax2, colors,
                       title='2. After Bandpass Filter (0.5-40 Hz)',
                       ylabel='Amplitude (µV)')
    
    # Subplot 3: PSD before cleaning
    ax3 = axes[1, 0]
    plot_psd(psds_raw, freqs_raw, ch_names, colors, ax3,
            title='3. PSD Before Artifact Removal',
            ylabel='Power (µV²/Hz)')
    
    # Subplot 4: PSD after cleaning
    ax4 = axes[1, 1]
    plot_psd(psds_clean, freqs_clean, ch_names, colors, ax4,
            title='4. PSD After Artifact Removal',
            ylabel='Power (µV²/Hz)')
    
    plt.tight_layout()
    
    # Save figure
    output_path = Path(output_path)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Summary plot saved to: {output_path}")
    
    plt.close()


def plot_eeg_timeseries(raw, ax, colors, title='EEG Signal', ylabel='Amplitude (µV)'):
    """
    Plot EEG time series without offset (all on same scale).
    
    Parameters
    ----------
    raw : mne.io.Raw
        Raw EEG data
    ax : matplotlib.axes.Axes
        Axis to plot on
    colors : list
        List of colors for each channel
    title : str
        Plot title
    ylabel : str
        Y-axis label
    """
    data, times = raw.get_data(return_times=True)
    data = data * 1e6  # Convert to microvolts
    
    ch_names = raw.ch_names
    
    # Plot all channels on same scale (no offset)
    for i, (channel_data, ch_name, color) in enumerate(zip(data, ch_names, colors)):
        ax.plot(times, channel_data, color=color, linewidth=1.0, label=ch_name, alpha=0.8)
    
    ax.set_xlabel('Time (s)', fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(times[0], times[-1])  # Show full recording duration
    
    # Add horizontal line at 0
    ax.axhline(y=0, color='k', linewidth=0.5, alpha=0.3)


def plot_psd(psds, freqs, ch_names, colors, ax, title='Power Spectral Density', 
             ylabel='Power (µV²/Hz)'):
    """
    Plot Power Spectral Density for all channels.
    
    Parameters
    ----------
    psds : ndarray
        PSD data (epochs × channels × frequencies) or (channels × frequencies)
    freqs : ndarray
        Frequency values
    ch_names : list
        Channel names
    colors : list
        Colors for each channel
    ax : matplotlib.axes.Axes
        Axis to plot on
    title : str
        Plot title
    ylabel : str
        Y-axis label
    """
    # Average across epochs if needed
    if psds.ndim == 3:
        psds_avg = np.mean(psds, axis=0)  # Average across epochs
    else:
        psds_avg = psds
    
    for i, (ch_name, color) in enumerate(zip(ch_names, colors)):
        ax.plot(freqs, psds_avg[i], color=color, linewidth=2, label=ch_name, alpha=0.8)
    
    # Add frequency band shading
    add_frequency_bands(ax)
    
    ax.set_xlabel('Frequency (Hz)', fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlim(0.5, 40)
    ax.set_yscale('log')
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3, which='both')


def add_frequency_bands(ax):
    """
    Add shaded regions for frequency bands.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axis to add bands to
    """
    bands = {
        'Delta': (0.5, 4, '#E8F5E9'),
        'Theta': (4, 8, '#E3F2FD'),
        'Alpha': (8, 13, '#FFF3E0'),
        'Beta': (13, 30, '#FCE4EC'),
        'Gamma': (30, 40, '#F3E5F5')
    }
    
    y_limits = ax.get_ylim()
    
    for band_name, (fmin, fmax, color) in bands.items():
        ax.axvspan(fmin, fmax, alpha=0.15, color=color)
        # Add band label
        mid_freq = (fmin + fmax) / 2
        ax.text(mid_freq, y_limits[1] * 0.8, band_name, 
               ha='center', va='top', fontsize=8, style='italic', alpha=0.6)


def compute_raw_psd(raw, fmin=0.5, fmax=40, n_fft=512):
    """
    Compute PSD for raw data.
    
    Parameters
    ----------
    raw : mne.io.Raw
        Raw EEG data
    fmin : float
        Minimum frequency
    fmax : float
        Maximum frequency
    n_fft : int
        FFT length
    
    Returns
    -------
    psds : ndarray
        PSD values (channels × frequencies)
    freqs : ndarray
        Frequency values
    """
    # Create epochs for PSD computation
    events = mne.make_fixed_length_events(raw, duration=2.0)
    epochs_temp = mne.Epochs(raw, events, tmin=0, tmax=2.0, 
                            baseline=None, preload=True, verbose=False)
    
    # Adjust n_fft if it's too large for the data
    n_times = epochs_temp.get_data().shape[2]
    n_fft = min(n_fft, n_times)
    n_per_seg = n_fft
    n_overlap = n_fft // 2
    
    # Compute PSD using new API
    try:
        spectrum = epochs_temp.compute_psd(
            method='welch',
            fmin=fmin,
            fmax=fmax,
            n_fft=n_fft,
            n_per_seg=n_per_seg,
            n_overlap=n_overlap,
            verbose=False
        )
        psds = spectrum.get_data()
        freqs = spectrum.freqs
    except AttributeError:
        # Fall back to old API
        psds, freqs = mne.time_frequency.psd_welch(
            epochs_temp,
            fmin=fmin,
            fmax=fmax,
            n_fft=n_fft,
            n_per_seg=n_per_seg,
            n_overlap=n_overlap,
            verbose=False
        )
    
    # Convert from V²/Hz to µV²/Hz (MNE works in volts internally)
    psds = psds * 1e12  # V² to µV²
    
    return psds, freqs


if __name__ == "__main__":
    import sys
    from csv_to_edf import csv_to_edf
    from preprocessing import preprocess_raw
    
    if len(sys.argv) < 2:
        print("Usage: python visualization.py <input_csv>")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    # Load and process data
    print("Loading data...")
    raw_original = csv_to_edf(input_file)
    
    print("\nPreprocessing...")
    raw_filtered = raw_original.copy()
    raw_filtered.filter(l_freq=0.5, h_freq=50.0, fir_design='firwin', verbose=False)
    
    epochs_clean, _ = preprocess_raw(raw_original, epoch_duration=2.0)
    
    print("\nComputing PSDs...")
    psds_raw, freqs_raw = compute_raw_psd(raw_original)
    
    # Compute PSD from cleaned epochs
    try:
        spectrum = epochs_clean.compute_psd(method='welch', verbose=False)
        psds_clean = spectrum.get_data()
        freqs_clean = spectrum.freqs
    except AttributeError:
        psds_clean, freqs_clean = mne.time_frequency.psd_welch(
            epochs_clean, verbose=False
        )
    
    print("\nCreating visualization...")
    output_path = input_file.parent / f"{input_file.stem}_summary_plot.png"
    create_processing_summary_plot(
        raw_original, raw_filtered, epochs_clean,
        psds_raw, freqs_raw, psds_clean, freqs_clean,
        output_path
    )
    
    print("\n✓ Visualization complete!")

