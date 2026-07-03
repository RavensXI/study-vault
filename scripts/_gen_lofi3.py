"""Generate a COMPOSED study track with Lyria 3 Pro ($0.08/full song on the
Gemini API — same GEMINI_API_KEY as the art pipeline). This replaced the
Lyria RealTime recorder (_gen_lofi.py): RealTime streams seamless-but-loopy
ambience; Lyria 3 writes an actual song with structure.

GOTCHA (learned 3 Jul 2026): genre-anchor phrases like "lo-fi hip hop"
trip Lyria's resembles-copyrighted-works filter (finishReason OTHER +
finishMessage). Describe the music ORIGINALLY — instruments, mood, arc —
instead of naming the genre.

Usage: python scripts/_gen_lofi3.py <outname> ["prompt..."]
"""
import os, sys, json, base64, urllib.request

NAME = sys.argv[1] if len(sys.argv) > 1 else "lofi-a"
PROMPT = sys.argv[2] if len(sys.argv) > 2 else (
    "A calm original instrumental for late-evening studying: soft electric piano chords, "
    "gentle brushed drums, warm upright bass, faint room ambience like rain on a window. "
    "Unhurried, around 72 beats per minute. It begins sparsely, gathers warmth in the middle "
    "as a muted guitar answers the piano, and settles to a soft close. Soothing and "
    "unobtrusive. No vocals.")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
req = urllib.request.Request(
    "https://generativelanguage.googleapis.com/v1beta/models/lyria-3-pro-preview:generateContent",
    data=json.dumps({"contents": [{"parts": [{"text": PROMPT}]}],
                     "generationConfig": {"responseModalities": ["AUDIO"]}}).encode(),
    headers={"x-goog-api-key": os.environ["GEMINI_API_KEY"], "Content-Type": "application/json"})
d = json.load(urllib.request.urlopen(req, timeout=280))
c = d.get("candidates", [{}])[0]
parts = (c.get("content") or {}).get("parts", [])
audio = [p for p in parts if "inlineData" in p]
if not audio:
    raise SystemExit(f"filtered/failed: {c.get('finishReason')} — {(c.get('finishMessage') or '')[:160]}")
blob = audio[0]["inlineData"]
raw = base64.b64decode(blob["data"])
ext = "wav" if "wav" in blob.get("mimeType", "") else "mp3"
out = os.path.join(ROOT, "design-lab", "assets", f"{NAME}.{ext}")
open(out, "wb").write(raw)
print(f"ok {out} ({blob.get('mimeType')}, {len(raw)//1024} KB)")
