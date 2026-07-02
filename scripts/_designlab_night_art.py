"""Overnight art for the five dashboard directions (2-3 Jul). Same lw language.
- panorama-a/b: ultra-wide landscape for the 'live in the landscape' direction
  (16:9, detail along the BOTTOM edge, vast calm sky above — UI floats in the sky)
- radio-set: a drawn wireless set object plate for the 'desk' direction
- desk-lamp: small spot vignette, same direction
"""
import os, io, time
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
IMG_MODEL = "gemini-3-pro-image-preview"

BASE = (" — drawn as a refined pen-and-ink illustration finished with a thin watercolour wash: "
        "confident black ink linework and fine hatching, thin translucent watercolour in muted colours "
        "laid over it, plenty of warm cream paper showing through, in the style of a vintage book-plate. "
        "Calm, atmospheric, editorial. No people, no recognisable faces. "
        "ABSOLUTELY NO text, words, letters or numbers.")

JOBS = {
    # UI floats in the sky: all landscape detail must hug the BOTTOM quarter
    "panorama-a": ("A vast panoramic English countryside vista: a winding footpath entering from the bottom-left "
                   "corner and wandering right through hedgerow fields, past a small copse and a stream, toward a "
                   "distant hilltop tower on the far right horizon; above the low horizon line, an enormous calm "
                   "cream sky with only the faintest wash of morning cloud. CRITICAL: all ink detail stays in the "
                   "BOTTOM QUARTER of the image; the upper three quarters are near-blank warm cream sky", "16:9"),
    "panorama-b": ("A sweeping panoramic downland landscape at dawn: gentle chalk hills rolling from left to right "
                   "along the very bottom of the frame, a winding track threading between them toward a tiny distant "
                   "village with a church spire at far right; a huge empty warm cream sky filling the upper three "
                   "quarters, one thin skein of birds high up. CRITICAL: all ink detail stays in the BOTTOM QUARTER; "
                   "the upper three quarters are near-blank warm cream sky", "16:9"),
    "radio-set": ("A single handsome 1950s wooden valve wireless radio set with a woven speaker grille and two round "
                  "bakelite dials, drawn as an isolated object plate centred on plain warm cream paper with a soft "
                  "drop shadow beneath it and nothing else around it", "1:1"),
    "desk-lamp": ("A small green-shaded brass banker's desk lamp switched on, drawn as an isolated object plate "
                  "centred on plain warm cream paper with a soft pool of light and nothing else around it", "1:1"),
}

def extract(r):
    for c in (r.candidates or []):
        cont = getattr(c, "content", None)
        for p in (getattr(cont, "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def render(prompt, ar):
    for attempt in range(4):
        for cfg in (types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio=ar)),
                    types.GenerateContentConfig(response_modalities=["IMAGE"])):
            try:
                r = client.models.generate_content(model=IMG_MODEL, contents=[prompt], config=cfg)
                d = extract(r)
                if d:
                    return Image.open(io.BytesIO(d)).convert("RGB"), None
            except Exception as e:
                msg = str(e)
                if any(k in msg for k in ("502", "503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                    time.sleep(5 * (attempt + 1)); break
                return None, msg[:90]
    return None, "refused/empty"

for name, (scene, ar) in JOBS.items():
    path = os.path.join(OUT, "night-" + name + ".png")
    if os.path.exists(path):
        print(f"skip {name} (exists)", flush=True); continue
    img, err = render(scene + BASE, ar)
    if img:
        img.save(path); print(f"ok  night-{name}.png  {img.size}", flush=True)
    else:
        print(f"FAIL {name}: {err}", flush=True)
