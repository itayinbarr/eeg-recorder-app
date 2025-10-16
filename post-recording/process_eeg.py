#!/usr/bin/env python3
"""
Main pipeline for processing EEG recordings.

This script processes CSV EEG recordings through the complete pipeline:
1. Convert CSV to EDF format
2. Preprocess with autoreject and bad epoch removal
3. Compute Power Spectral Density using Welch's method
4. Calculate band powers (Delta, Theta, Alpha, Beta, Gamma)
5. Calculate DAR and TAR ratios
6. Save results to CSV

Usage:
    python process_eeg.py <input_csv> [output_dir] [--seconds N]
    
Example:
    python process_eeg.py ../data/eeg_recording.csv ../data/results/ --seconds 60
"""

import argparse
from pathlib import Path
import sys

# Import local modules
from csv_to_edf import csv_to_edf
from preprocessing import preprocess_raw, get_preprocessing_report
from psd_analysis import (
    compute_psd_welch,
    compute_band_powers,
    compute_ratios,
    create_results_dataframe
)
from visualization import create_processing_summary_plot, compute_raw_psd


def process_eeg_recording(input_csv, output_dir=None, seconds=None):
    """
    Process a single EEG recording through the complete pipeline.
    
    Parameters
    ----------
    input_csv : str or Path
        Path to the input CSV file
    output_dir : str or Path, optional
        Directory for output files. If None, uses same directory as input.
    seconds : float, optional
        If provided, only the first N seconds of the recording will be used
        for PSD, band power calculations, and DAR/TAR ratios.
    
    Returns
    -------
    results : dict
        Dictionary containing paths to output files and processing statistics
    """
    input_csv = Path(input_csv)
    
    if output_dir is None:
        output_dir = input_csv.parent
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    base_name = input_csv.stem
    
    print("\n" + "=" * 70)
    print(" " * 20 + "EEG PROCESSING PIPELINE")
    print("=" * 70)
    print(f"\nInput file: {input_csv}")
    print(f"Output directory: {output_dir}")
    print()
    
    results = {
        'input_file': str(input_csv),
        'output_dir': str(output_dir),
    }
    
    # Step 1: Convert CSV to EDF
    print("\n" + ">" * 70)
    print("STEP 1: Converting CSV to EDF")
    print(">" * 70)
    
    edf_path = output_dir / f"{base_name}.edf"
    raw = csv_to_edf(input_csv, edf_path)
    results['edf_file'] = str(edf_path)
    
    # If requested, limit to the first N seconds of data for all downstream analyses
    if seconds is not None:
        if seconds <= 0:
            raise ValueError("seconds must be greater than 0")
        try:
            total_duration_sec = float(raw.times[-1])
        except Exception:
            total_duration_sec = float(raw.n_times) / float(raw.info['sfreq'])
        tmax = min(float(seconds), total_duration_sec)
        print(f"\nLimiting analysis to first {tmax:.2f}s out of {total_duration_sec:.2f}s")
        raw.crop(tmin=0.0, tmax=tmax)
    
    # Keep original for visualization
    raw_original = raw.copy()
    
    # Step 2: Preprocess with autoreject
    print("\n" + ">" * 70)
    print("STEP 2: Preprocessing with AutoReject")
    print(">" * 70)
    
    # Create filtered version for visualization
    raw_filtered = raw.copy()
    raw_filtered.filter(l_freq=0.5, h_freq=40.0, fir_design='firwin', verbose=False)
    
    epochs_clean, reject_log = preprocess_raw(
        raw,
        epoch_duration=2.0,
        baseline=None,
        apply_ica=False
    )
    
    preprocessing_report = get_preprocessing_report(epochs_clean, reject_log)
    results['preprocessing'] = preprocessing_report
    
    # Step 3: Compute PSD using Welch's method
    print("\n" + ">" * 70)
    print("STEP 3: Computing Power Spectral Density")
    print(">" * 70)
    
    psds, freqs = compute_psd_welch(
        epochs_clean,
        fmin=0.5,
        fmax=40,
        window_sec=2.0,
        overlap_sec=1.0
    )
    
    # Step 4: Compute band powers
    print("\n" + ">" * 70)
    print("STEP 4: Computing Band Powers")
    print(">" * 70)
    
    band_powers = compute_band_powers(psds, freqs)
    
    # Step 5: Compute ratios
    print("\n" + ">" * 70)
    print("STEP 5: Computing Power Ratios (DAR, TAR)")
    print(">" * 70)
    
    # Get channel names for per-electrode reporting
    channel_names = epochs_clean.ch_names
    print(f"\nAnalyzing {len(channel_names)} channels: {channel_names}")
    ratios = compute_ratios(band_powers, channel_names)
    
    # Step 6: Create visualization
    print("\n" + ">" * 70)
    print("STEP 6: Creating Summary Visualization")
    print(">" * 70)
    
    print("\nComputing PSDs for visualization...")
    # Compute PSD from original raw data
    psds_raw, freqs_raw = compute_raw_psd(raw_original, fmin=0.5, fmax=40, n_fft=512)
    
    # Create visualization
    plot_path = output_dir / f"{base_name}_summary_plot.png"
    create_processing_summary_plot(
        raw_original, raw_filtered, epochs_clean,
        psds_raw, freqs_raw, psds, freqs,
        plot_path
    )
    results['plot_file'] = str(plot_path)
    
    # Step 7: Create and save results
    print("\n" + ">" * 70)
    print("STEP 7: Saving Results")
    print(">" * 70)
    
    df = create_results_dataframe(epochs_clean, band_powers, ratios)
    
    results_csv = output_dir / f"{base_name}_band_powers.csv"
    df.to_csv(results_csv, index=False)
    results['results_csv'] = str(results_csv)
    
    print(f"\n✓ Results saved to: {results_csv}")
    
    # Save summary statistics
    summary_csv = output_dir / f"{base_name}_summary.csv"
    summary = df.groupby('channel').mean().round(6)
    summary.to_csv(summary_csv)
    results['summary_csv'] = str(summary_csv)
    
    print(f"✓ Summary statistics saved to: {summary_csv}")
    
    # Print final summary
    print("\n" + "=" * 70)
    print(" " * 25 + "FINAL SUMMARY")
    print("=" * 70)
    
    print(f"\nProcessing Statistics:")
    print(f"  Original epochs: {preprocessing_report['n_epochs_rejected'] + preprocessing_report['n_epochs_final']}")
    print(f"  Epochs after cleaning: {preprocessing_report['n_epochs_final']}")
    print(f"  Rejection rate: {preprocessing_report['rejection_rate']:.1f}%")
    print(f"  Final duration: {preprocessing_report['duration']:.1f}s")
    
    print(f"\nBand Powers (averaged across epochs and channels, µV²):")
    for band in ['delta', 'theta', 'alpha', 'beta', 'gamma']:
        col = f"{band}_power"
        print(f"  {band.capitalize():8s}: {df[col].mean():.2e} ± {df[col].std():.2e}")
    
    print(f"\nPower Ratios (averaged across epochs and channels):")
    print(f"  DAR (Delta/Alpha): {df['DAR'].mean():.3f} ± {df['DAR'].std():.3f}")
    print(f"  TAR (Theta/Alpha): {df['TAR'].mean():.3f} ± {df['TAR'].std():.3f}")
    
    # Per-electrode ratios
    if 'channel' in df.columns:
        print(f"\nPer-electrode Power Ratios:")
        for ch in df['channel'].unique():
            ch_data = df[df['channel'] == ch]
            print(f"  {ch}:")
            print(f"    DAR: {ch_data['DAR'].mean():.3f} ± {ch_data['DAR'].std():.3f}")
            print(f"    TAR: {ch_data['TAR'].mean():.3f} ± {ch_data['TAR'].std():.3f}")
    
    print("\n" + "=" * 70)
    print("✓ PROCESSING COMPLETE!")
    print("=" * 70)
    
    return results


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Process EEG recordings through the complete pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python process_eeg.py ../data/eeg_recording.csv
  python process_eeg.py ../data/eeg_recording.csv ../data/results/
        """
    )
    
    parser.add_argument(
        'input_csv',
        type=str,
        help='Path to the input CSV file'
    )
    
    parser.add_argument(
        'output_dir',
        type=str,
        nargs='?',
        default=None,
        help='Output directory (default: same as input file)'
    )
    
    parser.add_argument(
        '--seconds',
        type=float,
        default=None,
        help='If set, use only the first N seconds of the recording'
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    input_path = Path(args.input_csv)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    if not input_path.suffix == '.csv':
        print(f"Error: Input file must be a CSV file")
        sys.exit(1)
    
    # Process the recording
    try:
        results = process_eeg_recording(args.input_csv, args.output_dir, args.seconds)
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

