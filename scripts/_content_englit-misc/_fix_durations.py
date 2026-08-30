"""Write ffprobe-measured durations for the four re-narrated clips.

lib.narration.get_mp3_duration mis-measured three of the four (the known
"narration durations unreliable" wart): it reported 58.56s for a 39.24s clip
and 20.23s for a 40.61s one. js/main.js sums manifest[i].duration to build the
narration scrubber's total length and per-clip offsets, so a wrong value skews
the scrubber. Scope is deliberately limited to the clips this session touched.
"""
import json, os, subprocess, sys
os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPT_DIR)
from lib.supabase_client import get_client

FFPROBE = (r"C:\Users\tshau\AppData\Local\Microsoft\WinGet\Packages"
           r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
           r"\ffmpeg-8.0.1-full_build\bin\ffprobe.exe")

TARGETS = [
    ("0581f441-6e06-475c-b1b3-36d8184b8673", "n13", "frankenstein L6"),
    ("dfc930cd-8246-46cc-9d9b-4fc16885d08e", "n3", "leave-taking L5"),
    ("c81cefe5-ecc1-4cc0-a8c6-1e30dbb7aee5", "n28", "boys-dont-cry L6"),
    ("07d83404-fde9-43ab-8461-2064e8bb282b", "n13", "frankenstein L2"),
]

sb = get_client()
for lid, nid, label in TARGETS:
    row = sb.table("lessons").select("narration_manifest").eq(
        "id", lid).single().execute().data
    manifest = [dict(e) for e in row["narration_manifest"]]
    idx = next(i for i, e in enumerate(manifest) if e["id"] == nid)
    src = manifest[idx]["src"]
    out = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", src],
        capture_output=True, text=True, check=True)
    true_dur = round(float(out.stdout.strip()), 2)
    stored = manifest[idx]["duration"]
    if abs(true_dur - stored) < 0.05:
        print(f"  {label} {nid}: already accurate ({stored}s)")
        continue
    manifest[idx]["duration"] = true_dur
    sb.table("lessons").update({"narration_manifest": manifest}).eq("id", lid).execute()
    print(f"  {label} {nid}: {stored}s -> {true_dur}s  (ffprobe)")
print("\nDone.")
