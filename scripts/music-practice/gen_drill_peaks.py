# -*- coding: utf-8 -*-
"""Waveform peaks for every audio file used by the Music AQA practice drills.

R2 serves no Access-Control-Allow-Origin header, so the browser cannot fetch a
.peaks.json cross-origin. Peaks therefore travel INLINE inside the passage HTML
(same trick the Guided Listening dock uses). This script builds the manifest;
apply_inline_player.py embeds it.

Output: scripts/music-practice/_drill_peaks.json  { url: {peaks: [...], duration: float} }

Usage:  python scripts/music-practice/gen_drill_peaks.py
        python scripts/music-practice/gen_drill_peaks.py --force   (re-do all)
"""
import json, os, re, subprocess, sys, tempfile, urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np
from lib.supabase_client import get_client

UNITS = ["western-classical-1650-1910", "aos-listening", "listening-skills", "score-reading"]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_drill_peaks.json")
N_PEAKS = 260          # inline player is ~600px wide; 260 bars keeps each payload ~1.3KB
SR = 8000              # plenty for an envelope
MP3 = re.compile(r'https?://[^"\s\\)]+\.mp3')


def collect_urls():
    sb = get_client()
    urls = []
    for slug in UNITS:
        unit = [u for u in sb.table("units").select("id,slug").execute().data if u["slug"] == slug][0]
        for les in sb.table("lessons").select("practice_data").eq("unit_id", unit["id"]).execute().data:
            for m in MP3.findall(json.dumps(les["practice_data"] or {}, ensure_ascii=False)):
                if m not in urls:
                    urls.append(m)
    return urls


def peaks_for(path):
    """Decode to mono f32 and reduce to N_PEAKS envelope values in 0..1."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "quiet", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
        stdout=subprocess.PIPE, check=True).stdout
    a = np.frombuffer(raw, dtype="<f4")
    if a.size == 0:
        raise RuntimeError("decoded to zero samples")
    dur = a.size / float(SR)
    # pad so the split is exact, then take max(abs) per bucket
    pad = (-a.size) % N_PEAKS
    if pad:
        a = np.concatenate([a, np.zeros(pad, dtype=a.dtype)])
    env = np.abs(a.reshape(N_PEAKS, -1)).max(axis=1)
    top = float(env.max())
    if top > 0:
        env = env / top
    # gentle compression so quiet passages stay visible
    env = np.power(env, 0.7)
    return [round(float(v), 3) for v in env], round(dur, 2)


def main():
    force = "--force" in sys.argv
    done = {}
    if os.path.exists(OUT) and not force:
        with open(OUT, "r", encoding="utf-8") as f:
            done = json.load(f)
    urls = collect_urls()
    print("distinct audio files referenced by the drills:", len(urls))
    todo = [u for u in urls if u not in done]
    print("already have peaks for:", len(urls) - len(todo), "| to build:", len(todo))
    fails = []
    for i, url in enumerate(todo, 1):
        name = url.rsplit("/", 1)[-1]
        tmp = os.path.join(tempfile.gettempdir(), "svpk_" + name)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=90) as r, open(tmp, "wb") as f:
                f.write(r.read())
            pk, dur = peaks_for(tmp)
            done[url] = {"peaks": pk, "duration": dur}
            print("  [%2d/%2d] %-42s %6.1fs  ok" % (i, len(todo), name[:42], dur))
        except Exception as e:
            fails.append((url, str(e)[:90]))
            print("  [%2d/%2d] %-42s FAILED: %s" % (i, len(todo), name[:42], str(e)[:60]))
        finally:
            if os.path.exists(tmp):
                try: os.remove(tmp)
                except Exception: pass
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(done, f)   # checkpoint every file — downloads are the slow part

    print()
    print("manifest:", OUT)
    print("total entries:", len(done))
    if fails:
        print("FAILURES (%d) — these will keep their plain audio element:" % len(fails))
        for u, e in fails:
            print("   ", u.rsplit("/", 1)[-1], "|", e)
        sys.exit(1)
    print("all peaks built")


if __name__ == "__main__":
    main()
