"""Desk v4 radio plate: vintage wireless in the scene's style with a BLANK
tuning window (the live LCD marquee gets mapped into it) and two clear round
knobs (live station / skip-song controls sit on them). Cream background,
flood-fill cut like the book. Writes desk4-radio-{a,b}.png + -cut.png.
"""
import os, io, time
from google.genai import types
from PIL import Image
from _designlab_desk4_book import client, IMG_MODEL, extract, cut, OUT

PROMPT = (
    "In exactly the style of the attached reference image (hand-drawn pen-and-ink with soft "
    "watercolour wash, warm muted colours), draw ONE object on a plain warm cream paper "
    "background: a small 1950s wooden valve wireless radio, seen from a seated three-quarter "
    "view slightly above, angled a few degrees so its right side recedes gently. Rounded wooden "
    "cabinet, woven fabric speaker grille across the upper front. On the lower front fascia: "
    "ONE wide rectangular glass tuning window spanning most of the fascia width, drawn as a "
    "PLAIN EMPTY very dark green-black glass panel with a thin bezel — nothing printed inside "
    "it — and TWO round dark bakelite knobs, one at each end of the fascia below the window, "
    "clearly separated from it, each with a small pointer notch. A braided cloth power cord "
    "trails off to the left. Soft watercolour shadow beneath the set falling to its lower left. "
    "The radio fills most of the frame. ABSOLUTELY NO text, letters, numbers or dial markings."
)

scene = open(os.path.join(OUT, "desk4-scene-a.png"), "rb").read()
for tag in ("a", "b"):
    raw = os.path.join(OUT, f"desk4-radio-{tag}.png")
    if not os.path.exists(raw):
        img = None
        for attempt in range(4):
            try:
                r = client.models.generate_content(model=IMG_MODEL,
                    contents=[PROMPT, types.Part.from_bytes(data=scene, mime_type="image/png")],
                    config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                        image_config=types.ImageConfig(aspect_ratio="4:3", image_size="2K")))
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
    w, h = cut(raw, os.path.join(OUT, f"desk4-radio-{tag}-cut.png"))
    print(f"ok   {tag}  cut {w}x{h}", flush=True)
print("done")
