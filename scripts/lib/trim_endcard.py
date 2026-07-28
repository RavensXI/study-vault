"""Detect and trim the NotebookLM/Google logo endcard off a short.

Every NLM short ends with a HARD CUT to a logo card lasting a fixed ~2.07s.
The card is white in light-theme shorts and BLACK in dark-theme ones, and
the logo animates in — so absolute brightness tests are brittle. Instead:

1. prior: the cut sits at duration - 2.07s (constant across the bank);
2. find the exact boundary as the maximal consecutive-frame difference
   inside a +/-0.55s window around the prior (colour-agnostic);
3. confirm the post-cut frame is near-uniform (flat white/black card);
4. trim: lossless stream-copy when a keyframe sits on the cut (encoders
   put one on hard cuts ~80% of the time), else re-encode video only;
5. verify: trimmed duration sane AND the trimmed file's last frame matches
   the original's last pre-cut frame — a misdetection can never ship.

trim(path, out) -> report dict; report['ok'] gates any upload.
"""
import json
import shutil
import subprocess

import numpy as np

FFMPEG = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")
ENDCARD = 2.067        # fixed NLM endcard length (measured across the bank)
WINDOW = 0.55          # search this far either side of the prior
SNAP_BEFORE = 0.25     # accept a keyframe up to this much before the cut
CUT_MIN_DIFF = 8.0     # a real hard cut, absolute floor (0-255 scale) — pale
                       # white-bg content vs the white card can dip to ~10;
                       # the flat-card + tail-verify checks carry the safety
FLAT_STD_MAX = 28.0    # post-cut card frame must be near-uniform


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
    for cand in range(80, 160):
        if len(raw) % (width * cand * 3) == 0:
            h = cand
            break
    if h is None:
        return []
    n = len(raw) // (width * h * 3)
    a = np.frombuffer(raw, dtype=np.uint8).reshape(n, h, width, 3).astype(np.int16)
    return [(start + i / fps, a[i]) for i in range(n)]


def detect_cut(path, dur=None):
    """Return (cut_time, endcard_len) or (None, reason)."""
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
    # the hard cut = the dominant difference spike in the window
    dmax, imax = max(diffs)
    med = float(np.median([d for d, _ in diffs]))
    if dmax < max(CUT_MIN_DIFF, 4 * med):
        return None, f"no hard cut in window (max diff {dmax:.1f}, median {med:.1f})"
    card = fr[imax][1]
    if float(card.std(axis=(0, 1)).mean()) > FLAT_STD_MAX or \
       float(np.abs(card - card.mean(axis=(0, 1))).mean()) > FLAT_STD_MAX:
        return None, "post-cut frame is not a flat card"
    # cut just after the LAST CONTENT sample — the sampling grid can land the
    # first card sample one source frame late, and cutting there ships a
    # single card frame (caught by verify, but avoid it in the first place)
    cut = fr[imax - 1][0] + 0.005
    if not (1.6 <= dur - cut <= 2.7):
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
    # up to one source frame above the (last-content) cut is still safe: a
    # keyframe there is the card's own scene-cut keyframe, which -to excludes
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
    # the frame the trimmed file must end on (just before the cut)
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
    # verify: sane length + the new last frame IS the pre-cut content frame
    newdur = duration(out)
    if not (1.4 <= orig - newdur <= 2.8):
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
    rep["ok"], rep["why"] = True, "ok"
    return rep


if __name__ == "__main__":
    import sys
    print(json.dumps(trim(sys.argv[1], sys.argv[2]), indent=1))
