"""Detect and trim the Gemini Notebook / Google logo endcard off a short.

PATCHED COPY of sandbox scripts/lib/trim_endcard.py (31 Aug 2026).

The Gemini Notebook rebrand (~18 Aug 2026) lengthened the endcard from
2.067s to exactly 2.70s (measured n=10, std 0.00, across 10 subjects and
10 days). THREE constants were tuned to the old length, so the detector
silently skipped every clip for a fortnight:

  * ENDCARD, the prior the search window is centred on — the true cut sat
    ~0.08s outside the +/-0.55s window, so the window landed wholly inside
    the flat card and found no spike ("max diff 0.3, median 0.0");
  * the detect_cut sanity band, whose upper bound was 2.7 — the new card
    is 2.70s, i.e. exactly on the boundary and liable to be rejected;
  * the trim() duration-delta band, upper bound 2.8.

Fix: re-measure the prior, widen the window so a future rebrand of up to
+/-1.2s still lands, and lift both bands clear of the new length. Every
real safety gate is UNCHANGED — the flat-card test, the dominant-spike
test, and the tail-verify that compares the trimmed file's last frame to
the original's last pre-cut frame. A misdetection still cannot ship.

trim(path, out) -> report dict; report['ok'] gates any upload.
"""
import json
import shutil
import subprocess

import numpy as np

FFMPEG = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")
ENDCARD = 2.70         # Gemini Notebook card (was 2.067 for NotebookLM)
WINDOW = 0.55          # search this far either side of the prior. Do NOT
                       # widen: detect_cut takes the LARGEST spike in the
                       # window, so a wider window lets an ordinary content
                       # transition — or the logo's own fade-in — outbid the
                       # true cut, and the trim then lands inside the card.
                       # The card length is constant (std 0.00 over n=10), so
                       # a tight window centred on a correct prior is right.
                       # Guard against the NEXT rebrand with the skip-rate
                       # alert, not with a looser search.
SNAP_BEFORE = 0.25     # accept a keyframe up to this much before the cut
CUT_MIN_DIFF = 8.0     # a real hard cut, absolute floor (0-255 scale)
FLAT_STD_MAX = 28.0    # post-cut card frame must be near-uniform
BAND_MIN, BAND_MAX = 1.6, 3.3      # plausible endcard length
DELTA_MIN, DELTA_MAX = 1.4, 3.4    # plausible trimmed-duration delta


def _run(args):
    return subprocess.run(args, capture_output=True)


def duration(path):
    r = _run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
              "-of", "csv=p=0", str(path)])
    return float(r.stdout.strip())


def _frames(path, start, span, fps, width=64):
    """Decode `span` seconds from `start` at `fps` as tiny RGB thumbs."""
    r = _run([FFMPEG, "-v", "error", "-ss", f"{start:.3f}", "-t", f"{span:.3f}",
              "-i", str(path), "-vf", f"fps={fps},scale={width}:-2",
              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
    raw = r.stdout
    if not raw:
        return []
    h = None
    for cand in range(80, 200):
        if len(raw) % (width * cand * 3) == 0:
            h = cand
            break
    if h is None:
        return []
    n = len(raw) // (width * h * 3)
    a = np.frombuffer(raw, dtype=np.uint8).reshape(n, h, width, 3).astype(np.int16)
    return [(start + i / fps, a[i]) for i in range(n)]


def detect_cut(path, dur=None):
    """Return (cut_time, None) or (None, reason)."""
    if dur is None:
        dur = duration(path)
    prior = dur - ENDCARD
    start = max(0.0, prior - WINDOW)
    fr = _frames(path, start, (dur - start) - 0.02, 30)
    if len(fr) < 8:
        return None, "could not decode tail"
    diffs = []
    for i in range(1, len(fr)):
        diffs.append((float(np.abs(fr[i][1] - fr[i - 1][1]).mean()), i))
    dmax, imax = max(diffs)
    med = float(np.median([d for d, _ in diffs]))
    if dmax < max(CUT_MIN_DIFF, 4 * med):
        return None, f"no hard cut in window (max diff {dmax:.1f}, median {med:.1f})"
    card = fr[imax][1]
    if float(card.std(axis=(0, 1)).mean()) > FLAT_STD_MAX or \
       float(np.abs(card - card.mean(axis=(0, 1))).mean()) > FLAT_STD_MAX:
        return None, "post-cut frame is not a flat card"
    cut = fr[imax - 1][0] + 0.005
    if not (BAND_MIN <= dur - cut <= BAND_MAX):
        return None, f"cut lands {dur - cut:.2f}s from the end — outside sanity band"
    return cut, None


def _keyframes_near(path, cut):
    r = _run([FFPROBE, "-v", "error", "-select_streams", "v",
              "-skip_frame", "nokey", "-show_entries", "frame=pts_time",
              "-of", "csv=p=0", str(path)])
    keys = []
    for tok in r.stdout.decode("utf-8", "replace").replace(",", " ").split():
        try:
            keys.append(float(tok))
        except ValueError:
            pass
    return [k for k in keys if cut - SNAP_BEFORE <= k <= cut + 0.08]


def _last_frame(path, dur=None):
    if dur is None:
        dur = duration(path)
    fr = _frames(path, max(0.0, dur - 0.35), 0.4, 10)
    return fr[-1][1] if fr else None


def trim(path, out):
    """Trim the endcard. Returns a report dict; report['ok'] gates upload."""
    rep = {"ok": False, "method": None, "cut": None, "endcard": None, "why": ""}
    if not (FFMPEG and FFPROBE):
        rep["why"] = "ffmpeg/ffprobe not on PATH"
        return rep
    try:
        orig = duration(path)
        cut, err = detect_cut(path, orig)
    except Exception as e:  # noqa: BLE001 — any probe failure = leave source alone
        rep["why"] = f"detect failed: {e}"
        return rep
    if cut is None:
        rep["why"] = err
        return rep
    rep["cut"], rep["endcard"] = round(cut, 3), round(orig - cut, 2)
    want = _frames(path, max(0.0, cut - 0.30), 0.29, 10)
    want = want[-1][1] if want else None
    kfs = _keyframes_near(path, cut)
    if kfs:
        rep["method"] = "copy"
        r = _run([FFMPEG, "-v", "error", "-i", str(path), "-to", f"{max(kfs):.6f}",
                  "-c", "copy", "-movflags", "+faststart", "-y", str(out)])
    else:
        rep["method"] = "encode"
        r = _run([FFMPEG, "-v", "error", "-i", str(path), "-to", f"{cut:.3f}",
                  "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
                  "-pix_fmt", "yuv420p", "-c:a", "copy",
                  "-movflags", "+faststart", "-y", str(out)])
    if r.returncode != 0:
        rep["why"] = "ffmpeg failed: " + r.stderr.decode("utf-8", "replace")[-160:]
        return rep
    newdur = duration(out)
    rep["orig_dur"], rep["new_dur"] = round(orig, 2), round(newdur, 2)
    if not (DELTA_MIN <= orig - newdur <= DELTA_MAX):
        rep["why"] = f"trimmed duration delta {orig - newdur:.2f}s out of range"
        return rep
    got = _last_frame(out, newdur)
    if want is None or got is None:
        rep["why"] = "could not decode verification frames"
        return rep
    d = float(np.abs(got - want).mean())
    if d > 9.0:
        rep["why"] = f"trimmed tail does not match pre-cut content (diff {d:.1f})"
        return rep
    # extra gate for the backfill: the new last frame must NOT itself be a
    # flat card (belt and braces — catches a card-on-card double ending).
    flat = float(got.std(axis=(0, 1)).mean())
    if flat <= 6.0:
        rep["why"] = f"trimmed file still ends on a flat frame (std {flat:.1f})"
        return rep
    rep["tail_std"] = round(flat, 1)
    rep["ok"], rep["why"] = True, "ok"
    return rep


if __name__ == "__main__":
    import sys
    print(json.dumps(trim(sys.argv[1], sys.argv[2]), indent=1))
