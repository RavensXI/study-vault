# -*- coding: utf-8 -*-
"""Independent check of the agent's claim that Beethoven L3's exposition-repeat
pin (data-t=242) should be ~232.5s.

The agent used chroma cross-correlation plus an RMS attack-shape match. I use a
different feature space — correlation of log-magnitude spectrogram frames — so
this is a genuinely independent corroboration rather than a re-run.

Method: take the first-subject statement as a reference window, slide it across
the candidate region, and score cosine similarity at every offset. A real repeat
of the same material should give one sharp peak.
"""
import subprocess, sys, os, tempfile, urllib.request
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np

URL = ("https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/"
       "music-aqa/western-classical-1650-1910/lesson-01.mp3")
SR, N, HOP = 22050, 2048, 512
REF_START, REF_LEN = 107.0, 10.0       # first subject, per the lesson's own pin c2 (data-t=107)
SCAN_FROM, SCAN_TO = 215.0, 265.0

tmp = os.path.join(tempfile.gettempdir(), "chk_lesson-01.mp3")
if not os.path.exists(tmp):
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=180) as r, open(tmp, "wb") as f:
        f.write(r.read())

raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", tmp, "-ac", "1", "-ar", str(SR),
                      "-f", "f32le", "-"], stdout=subprocess.PIPE, check=True).stdout
a = np.frombuffer(raw, dtype="<f4").astype(np.float64)
print("duration %.1fs" % (a.size / SR))

win = np.hanning(N)
frames = 1 + (a.size - N) // HOP
S = np.empty((frames, N // 2 + 1), dtype=np.float32)
for i in range(frames):
    S[i] = np.abs(np.fft.rfft(a[i * HOP:i * HOP + N] * win)).astype(np.float32)
S = np.log1p(S * 50)
# coarse frequency bands: robust to small tuning/tempo differences between takes
bands = np.add.reduceat(S, np.arange(0, S.shape[1], 8), axis=1)
bands /= (np.linalg.norm(bands, axis=1, keepdims=True) + 1e-9)
fps = SR / float(HOP)

r0 = int(REF_START * fps)
rlen = int(REF_LEN * fps)
ref = bands[r0:r0 + rlen]

print()
print("similarity of the first-subject window (%.0f-%.0fs) against each offset:"
      % (REF_START, REF_START + REF_LEN))
scores = []
t = SCAN_FROM
while t < SCAN_TO:
    i = int(t * fps)
    seg = bands[i:i + rlen]
    if seg.shape[0] < rlen:
        break
    scores.append((t, float((ref * seg).sum() / rlen)))
    t += 0.5

best = max(scores, key=lambda x: x[1])
for t, s in scores:
    if abs(t - best[0]) < 12 or abs(t - 242) < 4 or abs(t - 232.5) < 4:
        mark = ""
        if t == best[0]:
            mark = "  <== BEST"
        elif abs(t - 242.0) < 0.26:
            mark = "  <-- current pin (242)"
        elif abs(t - 232.5) < 0.26:
            mark = "  <-- agent's proposal (232.5)"
        print("   %6.1fs  %.4f  %s%s" % (t, s, "#" * int(max(0, (s - 0.55)) * 300), mark))

cur = [s for t, s in scores if abs(t - 242.0) < 0.26]
prop = [s for t, s in scores if abs(t - 232.5) < 0.26]
print()
print("best match      : %.1fs  (%.4f)" % (best[0], best[1]))
if cur:
    print("current pin 242 : %.4f" % cur[0])
if prop:
    print("proposed 232.5  : %.4f" % prop[0])
print()
print("VERDICT:", "agent corroborated" if abs(best[0] - 232.5) <= 2.0 else
      ("current pin stands" if abs(best[0] - 242.0) <= 2.0 else "neither — best is %.1fs" % best[0]))
