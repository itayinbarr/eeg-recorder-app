#!/usr/bin/env python3
"""
Batch process multiple EEG recordings.

Usage:
    python batch_process.py <input_directory> [output_directory]
    
Example:
    python batch_process.py ../data/ ../data/results/
"""

import argparse
from pathlib import Path
import sys
from process_eeg import process_eeg_recording


def batch_process_recordings(input_dir, output_dir=None):
    """
    Process all CSV files in a directory.
    
    Parameters
    ----------
    input_dir : str or Path
        Directory containing CSV files
    output_dir : str or Path, optional
        Directory for output files. If None, creates 'results' subdirectory.
    """
    input_dir = Path(input_dir)
    
    if output_dir is None:
        output_dir = input_dir / 'results'
    else:
        output_dir = Path(output_dir)
    
    # Find all CSV files
    csv_files = list(input_dir.glob('eeg_recording_*.csv'))
    
    if not csv_files:
        print(f"No EEG recording CSV files found in {input_dir}")
        return
    
    print("\n" + "=" * 70)
    print(f" BATCH PROCESSING: {len(csv_files)} files")
    print("=" * 70)
    
    results = []
    
    for i, csv_file in enumerate(csv_files, 1):
        print(f"\n{'#' * 70}")
        print(f"# Processing file {i}/{len(csv_files)}: {csv_file.name}")
        print(f"{'#' * 70}")
        
        try:
            result = process_eeg_recording(csv_file, output_dir)
            results.append({
                'file': csv_file.name,
                'status': 'success',
                'output': result
            })
        except Exception as e:
            print(f"\n❌ Error processing {csv_file.name}: {e}")
            results.append({
                'file': csv_file.name,
                'status': 'failed',
                'error': str(e)
            })
    
    # Print summary
    print("\n" + "=" * 70)
    print(" BATCH PROCESSING SUMMARY")
    print("=" * 70)
    
    successful = sum(1 for r in results if r['status'] == 'success')
    failed = sum(1 for r in results if r['status'] == 'failed')
    
    print(f"\nTotal files: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if failed > 0:
        print("\nFailed files:")
        for r in results:
            if r['status'] == 'failed':
                print(f"  - {r['file']}: {r['error']}")
    
    print("\n✓ Batch processing complete!")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Batch process multiple EEG recordings',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python batch_process.py ../data/
  python batch_process.py ../data/ ../data/results/
        """
    )
    
    parser.add_argument(
        'input_dir',
        type=str,
        help='Directory containing CSV files'
    )
    
    parser.add_argument(
        'output_dir',
        type=str,
        nargs='?',
        default=None,
        help='Output directory (default: <input_dir>/results/)'
    )
    
    args = parser.parse_args()
    
    # Check if input directory exists
    input_path = Path(args.input_dir)
    if not input_path.exists() or not input_path.is_dir():
        print(f"Error: Input directory not found: {input_path}")
        sys.exit(1)
    
    # Process recordings
    try:
        batch_process_recordings(args.input_dir, args.output_dir)
    except Exception as e:
        print(f"\n❌ Error during batch processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

