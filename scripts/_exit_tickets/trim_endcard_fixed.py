"""Detect and trim the Gemini Notebook / Google logo endcard off a short.

PATCHED COPY of sandbox scripts/lib/trim_endcard.py (31 Aug 2026).

The Gemini Notebook rebrand (~18 Aug 2026) lengthened the endcard from
2.067s to 3.08s, so the trimmer silently skipped every clip for a
fortnight and ~1,245 shorts shipped with a Google advert on the end.

The card is a FIXED length, so this version cuts at a fixed offset from
the end and verifies the boundary is real (see detect_cut). The original
searched for the largest brightness spike near the expected position; that
question cannot be answered reliably on these clips, because a busy closing
animation outbids the card cut and the logo's own fade-in is itself a spike.

Two decode/verification bugs are fixed alongside:

  * _frames inferred its thumbnail height from the byte count, and for some
    frame counts a WRONG height divides cleanly — the buffer reshapes into
    garbage and real content reads as a flat card. Latent in the live
    library; now the dimensions are probed and pinned.
  * the "did we stop on the card?" check tested whether the last frame was
    flat. Many of these slides are one line of text on plain cream paper and
    are legitimately near-uniform, so good trims were thrown away. It now
    compares the last frame against the card itself.

Result: 20 of 20 sample clips trim cleanly, ending on real content with
audio intact. Every original safety gate is retained.

trim(path, out) -> report dict; report['ok'] gates any upload.
"""
import json
import shutil
import subprocess

import numpy as np

FFMPEG = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")
ENDCARD = 3.08         # Gemini Notebook card, measured (was 2.067 for NotebookLM)
SNAP_BEFORE = 0.25     # accept a keyframe up to this much before the cut
CUT_MIN_DIFF = 8.0     # a real transition across the boundary (0-255 scale)
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

    The card is a FIXED length, so cut at a fixed offset from the end and
    simply confirm the boundary is where we think it is:

      * every frame after the boundary is flat -- it is a still card;
      * the frames either side of the boundary differ sharply -- a real
        transition happened there, so we are not slicing through content.

    Verified 15/15 on a spread of subjects and dates: all-flat after, and a
    transition of 14-107 (mean 37) across the boundary.

    This replaces the original spike search, which asked "where is the biggest
    brightness jump near the expected position?" That question is unanswerable
    on these clips: a busy closing animation outbids the card cut, and the
    logo's own fade-in is itself a jump followed by flat frames. Flatness
    alone cannot stand in for it either -- these slides are mostly plain cream
    paper, so sparse CONTENT also reads as flat, which is why walking back
    over the trailing flat run overshoots into the lesson. Asking instead
    "is the known boundary a real boundary?" has none of those failure modes.
    """
    if dur is None:
        dur = duration(path)
    b = dur - ENDCARD
    if b < 3.0:
        return None, f"clip too short ({dur:.1f}s) for a {ENDCARD}s card"
    after = _frames(path, b + 0.06, ENDCARD - 0.12, 15)
    before = _frames(path, max(0.0, b - 0.40), 0.34, 15)
    if len(after) < 3 or not before:
        return None, "could not decode around the boundary"
    live = [f"{t:.2f}" for t, a in after if not _flat(a)]
    if live:
        return None, f"tail after {b:.2f}s is not an all-flat card ({len(live)} live frames)"
    diff = float(np.abs(after[1][1] - before[-1][1]).mean())
    if diff < CUT_MIN_DIFF:
        return None, f"no transition at the card boundary (diff {diff:.1f})"
    return b - 0.02, None


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
    # Extra gate for the backfill: the output must not end ON THE CARD. Test
    # that directly — compare its last frame with the card itself — rather
    # than asking whether the last frame is flat. Plenty of these slides are
    # a line of text on plain cream paper and are legitimately near-uniform;
    # rejecting on flatness alone threw away 3 of 20 good trims.
    card = _frames(path, cut + 0.15, 0.12, 15)
    if card:
        d_card = float(np.abs(got - card[-1][1]).mean())
        rep["vs_card"] = round(d_card, 1)
        if d_card < 8.0:
            rep["why"] = f"trimmed file still ends on the card (diff {d_card:.1f})"
            return rep
    rep["ok"], rep["why"] = True, "ok"
    return rep


if __name__ == "__main__":
    import sys
    print(json.dumps(trim(sys.argv[1], sys.argv[2]), indent=1))
