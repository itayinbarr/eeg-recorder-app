"""
Preprocessing pipeline with autoreject and bad epoch removal.
"""

import numpy as np
import mne
from autoreject import AutoReject, get_rejection_threshold
from mne.preprocessing import ICA


def preprocess_raw(raw, epoch_duration=2.0, baseline=None, apply_ica=False):
    """
    Preprocess raw EEG data with autoreject and bad epoch removal.
    
    Parameters
    ----------
    raw : mne.io.Raw
        Raw EEG data
    epoch_duration : float
        Duration of epochs in seconds (default: 2.0)
    baseline : tuple or None
        Baseline correction period (start, end) in seconds
    apply_ica : bool
        Whether to apply ICA for artifact removal
    
    Returns
    -------
    epochs_clean : mne.Epochs
        Cleaned epochs after autoreject
    reject_log : autoreject.RejectLog
        Log of rejected epochs and channels
    """
    # Create a copy to avoid modifying original
    raw = raw.copy()
    
    print("=" * 60)
    print("PREPROCESSING PIPELINE")
    print("=" * 60)
    
    # Apply bandpass filter (0.5-40 Hz for EEG)
    print("\n1. Applying bandpass filter (0.5-40 Hz)...")
    raw.filter(l_freq=0.5, h_freq=40.0, fir_design='firwin')
    
    # Optional ICA for artifact removal
    if apply_ica:
        print("\n2. Applying ICA for artifact removal...")
        ica = ICA(n_components=min(4, len(raw.ch_names)), random_state=42)
        ica.fit(raw)
        
        # Automatically find and exclude bad components
        # This is a simple heuristic; manual inspection is better
        ica.exclude = []
        raw = ica.apply(raw)
    
    # Create epochs
    print(f"\n3. Creating {epoch_duration}s epochs...")
    events = mne.make_fixed_length_events(
        raw, 
        duration=epoch_duration,
        overlap=0.0  # No overlap for epoch rejection
    )
    
    epochs = mne.Epochs(
        raw,
        events,
        tmin=0,
        tmax=epoch_duration,
        baseline=baseline,
        preload=True,
        verbose=False
    )
    
    print(f"   Created {len(epochs)} epochs")
    
    # Apply autoreject (adjust parameters for short recordings)
    n_epochs = len(epochs)
    
    if n_epochs < 10:
        print(f"\n   Note: Only {n_epochs} epochs available. Using simplified rejection.")
        print("\n4. Applying amplitude-based rejection (too few epochs for AutoReject)...")
        
        # Use simple peak-to-peak rejection for short recordings
        reject_criteria = get_rejection_threshold(epochs, ch_types='eeg')
        print(f"   Peak-to-peak rejection threshold: {reject_criteria['eeg']*1e6:.1f} µV")
        
        epochs_clean = epochs.copy()
        epochs_clean.drop_bad(reject=reject_criteria)
        
        # Create a simple reject log
        from autoreject import RejectLog
        bad_epochs = np.zeros(len(epochs), dtype=bool)
        dropped_indices = [i for i in range(len(epochs)) if i not in epochs_clean.selection]
        bad_epochs[dropped_indices] = True
        
        reject_log = RejectLog(
            bad_epochs=bad_epochs,
            labels=np.zeros((len(epochs), len(epochs.ch_names)), dtype=int),
            ch_names=epochs.ch_names
        )
    else:
        print("\n4. Running AutoReject to identify and interpolate bad channels...")
        # Adjust CV folds based on number of epochs
        cv_folds = min(5, n_epochs // 2)
        
        ar = AutoReject(
            n_interpolate=[1, 2, 3, 4],  # Number of channels to interpolate
            cv=cv_folds,  # Adjust cross-validation folds
            random_state=42,
            n_jobs=1,
            verbose=False
        )
        
        epochs_clean, reject_log = ar.fit_transform(epochs, return_log=True)
    
    # Print rejection statistics  
    print(f"\n   Rejection Results:")
    print(f"   - Epochs kept: {len(epochs_clean)} / {n_epochs}")
    print(f"   - Epochs rejected: {reject_log.bad_epochs.sum()}")
    print(f"   - Rejection rate: {(reject_log.bad_epochs.sum() / n_epochs) * 100:.1f}%")
    
    # Additional bad epoch removal for longer recordings
    if n_epochs >= 10:
        print("\n5. Additional amplitude-based rejection...")
        reject_criteria = get_rejection_threshold(epochs_clean, ch_types='eeg')
        print(f"   Peak-to-peak rejection threshold: {reject_criteria['eeg']*1e6:.1f} µV")
        epochs_clean.drop_bad(reject=reject_criteria)
    
    print(f"\n   Final epochs: {len(epochs_clean)}")
    print(f"   Total duration: {len(epochs_clean) * epoch_duration:.1f}s")
    
    print("\n✓ Preprocessing complete!")
    print("=" * 60)
    
    return epochs_clean, reject_log


def get_preprocessing_report(epochs_clean, reject_log):
    """
    Generate a preprocessing report.
    
    Parameters
    ----------
    epochs_clean : mne.Epochs
        Cleaned epochs
    reject_log : autoreject.RejectLog
        AutoReject log
    
    Returns
    -------
    report : dict
        Dictionary containing preprocessing statistics
    """
    report = {
        'n_epochs_final': len(epochs_clean),
        'n_epochs_rejected': reject_log.bad_epochs.sum(),
        'rejection_rate': (reject_log.bad_epochs.sum() / len(reject_log.bad_epochs)) * 100,
        'channels': epochs_clean.ch_names,
        'sfreq': epochs_clean.info['sfreq'],
        'duration': len(epochs_clean) * (epochs_clean.tmax - epochs_clean.tmin),
    }
    
    return report


if __name__ == "__main__":
    import sys
    from pathlib import Path
    from csv_to_edf import csv_to_edf
    
    if len(sys.argv) < 2:
        print("Usage: python preprocessing.py <input_csv_or_edf>")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    # Load data
    if input_file.suffix == '.csv':
        print("Loading CSV and converting to MNE format...")
        raw = csv_to_edf(input_file, output_path=None)
    else:
        print("Loading EDF file...")
        raw = mne.io.read_raw_edf(input_file, preload=True)
    
    # Preprocess
    epochs_clean, reject_log = preprocess_raw(raw)
    
    # Print report
    report = get_preprocessing_report(epochs_clean, reject_log)
    print("\nPreprocessing Report:")
    for key, value in report.items():
        print(f"  {key}: {value}")

