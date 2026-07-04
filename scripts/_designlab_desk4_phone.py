"""Desk v4 phone plate: smartphone drawn in the scene's style with a BLANK
dark screen (live shorts-poster screen gets homography-mapped into the glass).
Cream background, flood-fill cut. Writes desk4-phone-{a,b}.png + -cut.png.
"""
import os, io, time
from google.genai import types
from PIL import Image
from _designlab_desk4_book import client, IMG_MODEL, extract, cut, OUT

PROMPT = (
    "In exactly the style of the attached reference image (hand-drawn pen-and-ink with soft "
    "watercolour wash, warm muted colours), draw ONE object on a plain warm cream paper "
    "background: a modern smartphone in a slim dark matte case, lying flat on the desk, seen "
    "from a seated three-quarter view slightly above, rotated about five degrees anticlockwise. "
    "Its screen is a PLAIN VERY DARK, almost black glass rectangle with soft rounded corners — "
    "completely blank, nothing on it, just a faint diagonal window reflection. Thin drawn "
    "bezel, a small camera dot at the top of the screen, and a soft watercolour shadow beneath "
    "the phone falling to its lower left. The phone fills most of the frame height. "
    "ABSOLUTELY NO text, icons, app grids, buttons or logos on the screen."
)

scene = open(os.path.join(OUT, "desk4-scene-a.png"), "rb").read()
for tag in ("a", "b"):
    raw = os.path.join(OUT, f"desk4-phone-{tag}.png")
    if not os.path.exists(raw):
        img = None
        for attempt in range(4):
            try:
                r = client.models.generate_content(model=IMG_MODEL,
                    contents=[PROMPT, types.Part.from_bytes(data=scene, mime_type="image/png")],
                    config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                        image_config=types.ImageConfig(aspect_ratio="3:4", image_size="2K")))
                d = extract(r)
                if d:
                    img = Image.open(io.BytesIO(d)).convert("RGB"); break
            except Exception as e:
                msg = str(e)
                if any(k in msg for k in ("502","503","UNAVAILABLE","429","RESOURCE_EXHAUSTED")):
                    time.sleep(6*(attempt+1)); continue
                print("  err:", msg[:110], flush=True)
        if img is None:
            print("FAIL", tag, flush=True); continue
        img.save(raw)
    w, h = cut(raw, os.path.join(OUT, f"desk4-phone-{tag}-cut.png"))
    print(f"ok   {tag}  cut {w}x{h}", flush=True)
print("done")
