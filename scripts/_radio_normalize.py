"""Normalise the Revision Radio station library.
Walks design-lab/assets/radio/{station}/ for new .wav/.m4a/.mp3 drops (Flow
exports etc.), loudness-normalises to -16 LUFS, transcodes to 192k MP3 with
the same name, and parks the original in design-lab/assets/radio-masters/.
A ledger avoids re-processing. Safe to run any time; run after every drop.

Usage: python scripts/_radio_normalize.py
"""
import os, json, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RADIO = os.path.join(ROOT, "design-lab", "assets", "radio")
MASTERS = os.path.join(ROOT, "design-lab", "assets", "radio-masters")
LEDGER = os.path.join(RADIO, "_normalized.json")

done = {}
if os.path.exists(LEDGER):
    done = json.load(open(LEDGER, encoding="utf-8"))

count = 0
for station in sorted(os.listdir(RADIO)):
    sdir = os.path.join(RADIO, station)
    if not os.path.isdir(sdir) or station.startswith("_"):
        continue
    for f in sorted(os.listdir(sdir)):
        stem, ext = os.path.splitext(f)
        if ext.lower() not in (".mp3", ".m4a", ".wav"):
            continue
        key = f"{station}/{stem}"
        if done.get(key):
            continue
        src = os.path.join(sdir, f)
        tmp = os.path.join(sdir, stem + ".norm.mp3")
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src,
                            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                            "-codec:a", "libmp3lame", "-b:a", "192k", tmp])
        if r.returncode != 0:
            print(f"FAIL  {key}"); continue
        mdir = os.path.join(MASTERS, station)
        os.makedirs(mdir, exist_ok=True)
        shutil.move(src, os.path.join(mdir, f))          # keep the master
        shutil.move(tmp, os.path.join(sdir, stem + ".mp3"))
        done[key] = True; count += 1
        print(f"ok    {key}")

json.dump(done, open(LEDGER, "w", encoding="utf-8"), indent=1)
print(f"done: {count} new track(s) normalised")
