"""Weekly-doodle candidates for the Guided door backdrop (Google-doodle style:
the art changes weekly with a notable event). Same lw style + composition rule
as _designlab_guided_backdrop.py. Week of 2026-06-29: Somme 110 / World Cup.
"""
import os, io, time
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
IMG_MODEL = "gemini-3-pro-image-preview"

STYLE = (" — drawn as a refined pen-and-ink illustration finished with a thin watercolour wash: "
         "confident black ink linework and fine hatching, thin translucent watercolour in muted colours "
         "laid over it, plenty of warm cream paper showing through, in the style of a vintage book-plate. "
         "Calm, atmospheric, editorial. No people, no recognisable faces. "
         "ABSOLUTELY NO text, words, letters or numbers. "
         "CRITICAL COMPOSITION RULE: all detail and ink density gathers in the LOWER-RIGHT of the image; "
         "the drawing dissolves into completely blank warm cream paper across the UPPER-LEFT THIRD — "
         "that region must be empty paper, as if the illustration was never finished there.")

WEEK = {
    # 1 July 1916 -> 110 years. Indirect and tasteful: poppies + a distant memorial arch.
    "weekly-somme110": ("A gentle meadow of scattered wild poppies rippling across soft chalk downland, "
                        "with a great weathered stone memorial arch standing hazy and small on the far "
                        "horizon under a quiet dawn sky, the reds of the poppies the only strong colour"),
    # FIFA World Cup 2026 knockout rounds, happening this week.
    "weekly-worldcup": ("An empty sunlit football goal seen from a low angle on a freshly mown pitch, "
                        "a single ball resting near the penalty spot casting a long evening shadow, "
                        "faint mown stripes leading to a small flag-topped stand far on the horizon"),
}

def extract(r):
    for c in (r.candidates or []):
        cont = getattr(c, "content", None)
        for p in (getattr(cont, "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def render(prompt):
    for attempt in range(4):
        for cfg in (types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio="3:2")),
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

for name, scene in WEEK.items():
    path = os.path.join(OUT, name + ".png")
    if os.path.exists(path):
        print(f"skip {name}.png (exists)", flush=True); continue
    img, err = render(scene + STYLE)
    if img:
        img.save(path); print(f"ok  {name}.png  {img.size}", flush=True)
    else:
        print(f"FAILED {name}: {err}", flush=True)
