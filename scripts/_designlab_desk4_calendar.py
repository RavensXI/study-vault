"""Desk4 calendar plate — a wire-bound desk flip calendar with a BLANK top
page; the weekly doodle + live month grid are homography-mapped onto the
painted page in dash-desk4.html (same treatment as the radio LCD / phone
screen / book pages).
"""
import os, io, time
from google.genai import types
from PIL import Image
from _designlab_desk4_book import client, IMG_MODEL, extract, cut, OUT

PROMPT = (
    "In exactly the style of the attached reference image (hand-drawn pen-and-ink with soft "
    "watercolour wash, warm muted colours), draw ONE object on a plain warm cream paper "
    "background: a small wire-bound desk flip calendar lying flat on a desk, seen from ALMOST "
    "DIRECTLY ABOVE, VERY NEARLY SQUARE TO THE FRAME — rotated no more than two or three "
    "degrees. Metal wire-o spiral binding runs along the TOP edge, passing through punched "
    "holes; a small stack of pages shows at the side and bottom edges; the corners are very "
    "slightly curled and softened, nothing sharp. The visible top page is COMPLETELY BLANK "
    "plain cream paper: ABSOLUTELY NO text, NO numbers, NO pictures, NO lines on the page. "
    "Thin ink outlines, soft watercolour shadow beneath. The calendar fills most of the frame, "
    "slightly taller than wide."
)

if __name__ == "__main__":
    scene = open(os.path.join(OUT, "desk4-scene-a.png"), "rb").read()
    for tag in ("a", "b"):
        raw = os.path.join(OUT, f"desk4-calendar-{tag}.png")
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
        w, h = cut(raw, os.path.join(OUT, f"desk4-calendar-{tag}-cut.png"))
        print(f"ok   {tag}  cut {w}x{h}", flush=True)
    print("done")
