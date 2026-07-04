"""Desk4 wristwatch plate — lying flat on the desk as if taken off, blank
dial (live hands + revision-timer arc are overlaid in dash-desk4.html).
"""
import os, io, time
from google.genai import types
from PIL import Image
from _designlab_desk4_book import client, IMG_MODEL, extract, cut, OUT

PROMPT = (
    "In exactly the style of the attached reference image (hand-drawn pen-and-ink with soft "
    "watercolour wash, warm muted colours), draw ONE object on a plain warm cream paper "
    "background: a wristwatch lying flat on a desk, seen from ALMOST DIRECTLY ABOVE, VERY "
    "NEARLY SQUARE TO THE FRAME — rotated no more than two or three degrees. The watch has "
    "been taken off and set down casually: a warm tan leather strap, unbuckled, lying in a "
    "gentle loose curve. Round steel case. The dial is PLAIN pale cream and COMPLETELY BLANK: "
    "thin ink tick marks around the rim of the dial are allowed, but ABSOLUTELY NO hands, NO "
    "numbers, NO letters, NO text anywhere. Thin ink outlines, soft watercolour shadow "
    "beneath. The watch fills most of the frame."
)

if __name__ == "__main__":
    scene = open(os.path.join(OUT, "desk4-scene-a.png"), "rb").read()
    for tag in ("a", "b"):
        raw = os.path.join(OUT, f"desk4-watch-{tag}.png")
        img = None
        if not os.path.exists(raw):
            for attempt in range(4):
                try:
                    r = client.models.generate_content(model=IMG_MODEL,
                        contents=[PROMPT, types.Part.from_bytes(data=scene, mime_type="image/png")],
                        config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                            image_config=types.ImageConfig(aspect_ratio="1:1", image_size="2K")))
                    d = extract(r)
                    if d:
                        img = Image.open(io.BytesIO(d)).convert("RGB"); break
                except Exception as e:
                    msg = str(e)
                    if any(k in msg for k in ("502", "503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                        time.sleep(6 * (attempt + 1)); continue
                    print("  err:", msg[:110], flush=True)
            if img is None:
                print("FAIL", tag, flush=True); continue
            img.save(raw)
        w, h = cut(raw, os.path.join(OUT, f"desk4-watch-{tag}-cut.png"))
        print(f"ok   {tag}  cut {w}x{h}", flush=True)
    print("done")
