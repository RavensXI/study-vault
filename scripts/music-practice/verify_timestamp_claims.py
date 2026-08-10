# -*- coding: utf-8 -*-
"""Second-by-second envelope around the claimed moments, so the corrected
timestamps are measured rather than guessed."""
import subprocess, sys, os, tempfile, urllib.request
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np

R2 = "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/music-aqa/western-classical-1650-1910/"
JOBS = [
    ("Haydn 94 mvt 2 — 'surprise' chord", "lesson-04.mp3", 20, 55, "claimed 0:27"),
    ("Handel Zadok — choir entry", "lesson-05.mp3", 80, 110, "claimed 1:30"),
    ("Beethoven Sym 1 — Adagio into Allegro", "lesson-01.mp3", 55, 130, "claimed 1:10 and 1:50"),
]
SR = 8000


def fmt(t):
    return "%d:%02d" % (int(t // 60), int(t % 60))


for label, name, t0, t1, claim in JOBS:
    tmp = os.path.join(tempfile.gettempdir(), "chk_" + name)
    if not os.path.exists(tmp):
        req = urllib.request.Request(R2 + name, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "wb") as f:
            f.write(r.read())
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", tmp, "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], stdout=subprocess.PIPE, check=True).stdout
    a = np.frombuffer(raw, dtype="<f4")
    print("=" * 74)
    print("%s   (%s)" % (label, claim))
    step = 1.0 if (t1 - t0) <= 40 else 2.0
    peak_prev = None
    for t in np.arange(t0, t1, step):
        seg = np.abs(a[int(t * SR):int((t + step) * SR)])
        pk = float(seg.max()) if seg.size else 0.0
        jump = "" if peak_prev in (None, 0) else ("   <== x%.1f" % (pk / peak_prev) if pk > peak_prev * 2.5 else "")
        print("  %-6s %.3f  %s%s" % (fmt(t), pk, "#" * int(pk * 60), jump))
        peak_prev = pk
    print()
