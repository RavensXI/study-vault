"""
Batch convert all narration WAV files to MP3 using ffmpeg.
Deletes the original WAV after successful conversion.

Usage:
    python scripts/convert_wav_to_mp3.py              # Convert all WAVs in project
    python scripts/convert_wav_to_mp3.py --keep-wav    # Keep WAVs after conversion
"""

import io
import os
import subprocess
import sys
import time

# Fix Windows console encoding
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Directories containing narration WAVs
UNIT_DIRS = [
    "history/conflict-tension",
    "history/health-people",
    "history/elizabethan",
    "history/america",
    "business/theme-1",
    "business/theme-2",
    "geography/paper-1",
    "geography/paper-2",
    "sport-science/r180",
]

def convert_file(wav_path, keep_wav=False):
    """Convert a single WAV to MP3. Returns (success, mp3_size_bytes)."""
    mp3_path = wav_path.rsplit(".", 1)[0] + ".mp3"

    if os.path.exists(mp3_path):
        return True, os.path.getsize(mp3_path)

    args = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", wav_path,
        "-codec:a", "libmp3lame",
        "-b:a", "96k",
        "-ar", "24000",
        "-ac", "1",
        mp3_path,
    ]

    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  FAILED: {os.path.basename(wav_path)} — {result.stderr.strip()}")
        return False, 0

    mp3_size = os.path.getsize(mp3_path)

    if not keep_wav:
        os.remove(wav_path)

    return True, mp3_size


def main():
    keep_wav = "--keep-wav" in sys.argv

    print("WAV → MP3 Batch Converter")
    print(f"Mode: {'keep WAVs' if keep_wav else 'delete WAVs after conversion'}")
    print()

    total_start = time.time()
    total_converted = 0
    total_skipped = 0
    total_failed = 0
    total_wav_size = 0
    total_mp3_size = 0

    for unit_dir in UNIT_DIRS:
        full_dir = os.path.join(PROJECT_ROOT, unit_dir)
        if not os.path.isdir(full_dir):
            continue

        wav_files = sorted(
            f for f in os.listdir(full_dir)
            if f.startswith("narration_") and f.endswith(".wav")
        )

        if not wav_files:
            continue

        print(f"  {unit_dir}: {len(wav_files)} WAVs")
        unit_converted = 0

        for wav_name in wav_files:
            wav_path = os.path.join(full_dir, wav_name)
            wav_size = os.path.getsize(wav_path)
            total_wav_size += wav_size

            mp3_path = wav_path.rsplit(".", 1)[0] + ".mp3"
            if os.path.exists(mp3_path):
                total_skipped += 1
                total_mp3_size += os.path.getsize(mp3_path)
                continue

            success, mp3_size = convert_file(wav_path, keep_wav)
            if success:
                total_converted += 1
                unit_converted += 1
                total_mp3_size += mp3_size
            else:
                total_failed += 1

        print(f"    → {unit_converted} converted" +
              (f", {total_skipped} already MP3" if total_skipped else ""))

    elapsed = time.time() - total_start

    print(f"\n{'=' * 45}")
    print(f"SUMMARY")
    print(f"{'=' * 45}")
    print(f"Converted:  {total_converted}")
    print(f"Skipped:    {total_skipped} (MP3 already exists)")
    print(f"Failed:     {total_failed}")
    print(f"WAV total:  {total_wav_size / 1024 / 1024:.0f} MB")
    print(f"MP3 total:  {total_mp3_size / 1024 / 1024:.0f} MB")
    if total_wav_size > 0:
        print(f"Reduction:  {(1 - total_mp3_size / total_wav_size) * 100:.0f}%")
    print(f"Time:       {elapsed:.1f}s")
    print(f"\nDone!")


if __name__ == "__main__":
    main()
