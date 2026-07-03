"""Desk v4 background: OUR OWN composition in the style of Tom's approved mock
(passed as a style reference only — not copied). An empty desk with painted
non-interactive stationery and deliberate clear zones where the interactive
objects (notebook / radio / postcard / phone / flashcards / stickies) will be
added one by one as live overlays.
Writes design-lab/assets/lw/desk4-scene-{a,b}.png
"""
import os, io, time
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw")
STYLE_REF = r"C:\Users\tshau\Downloads\Gemini_Generated_Image_iaw6cbiaw6cbiaw6.jpg"

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
IMG_MODEL = "gemini-3-pro-image-preview"

PROMPT = (
    "Using the attached image ONLY as a style, palette, lighting and camera-angle reference "
    "(hand-drawn pen-and-ink with soft watercolour wash; pale scrubbed wood desk seen from a "
    "seated three-quarter view; soft daylight from the upper left), paint a NEW empty desk scene:\n"
    "- The whole frame is the wooden desktop: pale warm wood with long wavy hand-drawn grain "
    "lines, a few darker knots, watercolour tone variation.\n"
    "- Character marks: a cluster of small ink splatters lower left, one faint tea-ring stain "
    "right of centre, a couple of pale watermark blotches, tiny paint flecks.\n"
    "- Painted stationery, drawn small and true to scale, ONLY in the mid-right column of the "
    "desk between the upper right and lower right corners: a long yellow HB pencil, a black "
    "fountain pen with a gold nib, a small pink eraser, a stub of a yellow pencil, a few curls "
    "of pencil-sharpener shavings.\n"
    "- A white ceramic mug crammed with pencils and pens, upper centre-right, drawn from "
    "slightly above so a little of the rim interior shows.\n"
    "- LEAVE COMPLETELY EMPTY (plain wood only): the upper left corner, a very large area "
    "across the centre and centre-left (two thirds of the frame), the upper right corner, and "
    "the whole lower right corner.\n"
    "- Nothing else on the desk. No notebook, no phone, no radio, no postcard, no sticky notes, "
    "no cards, no paper. ABSOLUTELY NO text, letters, numbers or logos."
)

def extract(r):
    for c in (r.candidates or []):
        for p in (getattr(getattr(c, "content", None), "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

ref = open(STYLE_REF, "rb").read()
for tag in ("a", "b"):
    out = os.path.join(OUT, f"desk4-scene-{tag}.png")
    if os.path.exists(out):
        print("skip", tag); continue
    img = None
    for attempt in range(4):
        try:
            r = client.models.generate_content(model=IMG_MODEL,
                contents=[PROMPT, types.Part.from_bytes(data=ref, mime_type="image/jpeg")],
                config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="16:9", image_size="2K")))
            d = extract(r)
            if d:
                img = Image.open(io.BytesIO(d)).convert("RGB"); break
        except Exception as e:
            msg = str(e)
            if "image_size" in msg or "INVALID_ARGUMENT" in msg:
                # retry without the size hint
                try:
                    r = client.models.generate_content(model=IMG_MODEL,
                        contents=[PROMPT, types.Part.from_bytes(data=ref, mime_type="image/jpeg")],
                        config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                            image_config=types.ImageConfig(aspect_ratio="16:9")))
                    d = extract(r)
                    if d:
                        img = Image.open(io.BytesIO(d)).convert("RGB"); break
                except Exception as e2:
                    msg = str(e2)
            if any(k in msg for k in ("502", "503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                time.sleep(6 * (attempt + 1)); continue
            print("  err:", msg[:110], flush=True)
    if img is None:
        print("FAIL", tag, flush=True); continue
    img.save(out)
    print("ok  ", tag, img.size, flush=True)
print("done")
