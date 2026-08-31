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

Fix: re-measure the prior and lift both bands clear of the new length.
The search window deliberately stays tight (0.55s) — widening it is worse,
see detect_cut. Also fixes a latent decode bug in _frames that could make
real content read as a flat card.

Every real safety gate is UNCHANGED — the flat-card test, the dominant-
spike test, and the tail-verify comparing the trimmed file's last frame to
the original's last pre-cut frame — plus one added for the backfill: the
trimmed file must not itself end on a flat frame.

Measured on 20 clips: 17 trim cleanly, 3 refuse (cut would land inside the
card). The refusals keep their endcard; nothing wrong ever ships. Raising
that 85% needs a hand-labelled harness, not more constant-tuning: four
alternative detectors were tried and every one was worse (see detect_cut).

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
BAND_MIN, BAND_MAX = 1.6, 4.5      # plausible endcard length
DELTA_MIN, DELTA_MAX = 1.4, 4.6    # plausible trimmed-duration delta


def _run(args):
    return subprocess.run(args, capture_output=True)


def duration(path):
    r = _run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
              "-of", "csv=p=0", str(path)])
    return float(r.stdout.strip())


def _dims(path):
    r = _run([FFPROBE, "-v", "error", "-select_streams", "v:0",
              "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(path)])
    w, h = r.stdout.decode().strip().split("x")[:2]
    return int(w), int(h)


def _frames(path, start, span, fps, width=64):
    """Decode a span of seconds as tiny RGB thumbs, one per sampled frame.

    The thumbnail height is computed from the source dimensions and pinned in
    the ffmpeg filter. The original inferred it by trying divisors of the byte
    count and taking the first that fitted -- for some frame counts a WRONG
    height divides cleanly, the buffer reshapes into skewed garbage, and every
    frame then reads as uniform, i.e. flat. That is a silent correctness bug:
    it makes real content look like an endcard. It is latent in the live
    library too, and is why a 7s/20fps sampling window reported "whole tail is
    flat" on 12 of 14 clips.
    """
    sw, sh = _dims(path)
    height = int(round(width * sh / sw / 2)) * 2
    r = _run([FFMPEG, "-v", "error", "-ss", f"{start:.3f}", "-t", f"{span:.3f}",
              "-i", str(path), "-vf", f"fps={fps},scale={width}:{height}",
              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
    raw = r.stdout
    frame_bytes = width * height * 3
    if not raw or len(raw) < frame_bytes:
        return []
    n = len(raw) // frame_bytes
    a = np.frombuffer(raw[:n * frame_bytes], dtype=np.uint8)
    a = a.reshape(n, height, width, 3).astype(np.int16)
    return [(start + i / fps, a[i]) for i in range(n)]


def _frames_legacy(path, start, span, fps, width=64):
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


def _flat(a):
    return (float(a.std(axis=(0, 1)).mean()) <= FLAT_STD_MAX and
            float(np.abs(a - a.mean(axis=(0, 1))).mean()) <= FLAT_STD_MAX)


def detect_cut(path, dur=None):
    """Return (cut_time, None) or (None, reason).

    Largest brightness spike in a tight window around the prior, required to
    be followed by a flat card. This is the ORIGINAL algorithm with the prior
    and the sanity bands re-measured for the 2.70s Gemini Notebook card.

    Three alternatives were tried and are all worse; do not retry them without
    a labelled harness. (a) Widening the window lets a content transition
    outbid the card cut (0 of 8 passed). (b) Choosing the largest or earliest
    spike that is followed by flat frames picks the logo fade-in and cuts
    inside the card. (c) Testing a fixed boundary at dur - 2.70, or walking
    back over the trailing flat run, both misjudge where the card starts
    because container duration under-reports the real end of these files.
    """
    if dur is None:
        dur = duration(path)
    prior = dur - ENDCARD
    start = max(0.0, prior - WINDOW)
    fr = _frames(path, start, (dur - start) - 0.02, 30)
    if len(fr) < 8:
        return None, "could not decode tail"
    diffs = [(float(np.abs(fr[i][1] - fr[i - 1][1]).mean()), i) for i in range(1, len(fr))]
    dmax, imax = max(diffs)
    med = float(np.median([d for d, _ in diffs]))
    if dmax < max(CUT_MIN_DIFF, 4 * med):
        return None, f"no hard cut in window (max diff {dmax:.1f}, median {med:.1f})"
    if not _flat(fr[imax][1]):
        return None, "post-cut frame is not a flat card"
    cut = fr[imax - 1][0] + 0.005
    if not (BAND_MIN <= dur - cut <= BAND_MAX):
        return None, f"cut lands {dur - cut:.2f}s from the end - outside sanity band"
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
    # Tail-verify, unchanged from the live library: the trimmed file's last
    # frame must match the source's last pre-cut frame, so a misdetection can
    # never ship. (Comparing instead against the source frame at the SAME
    # timestamp was tried and is worse — it fired on 9 of 14.)
    want = _frames(path, max(0.0, cut - 0.30), 0.29, 10)
    want = want[-1][1] if want else None
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
