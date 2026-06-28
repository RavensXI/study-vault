"""Find a COHESIVE 'tapestry of ideas' style for a unit's art band — one unified
artwork, single style + palette, ideas interwoven — NOT a collage of cut-out
objects. Text-to-image (no source photo to copy isolated objects from).

Outputs design-lab/assets/_tap-{A,B,C,D}.png  (Biology Paper 1)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

IDEAS = ("cells and microscopy, body organisation and the digestive system, the heart and circulation, "
         "the lungs and breathing, infection and white blood cells, photosynthesis, plants and ecology")
NO = "Warm off-white paper. Absolutely NO text, letters, numbers, captions or labels anywhere."
CON = ("Render it as ONE single integrated artwork in ONE consistent style and ONE palette — every element "
       "drawn the same way and woven together so the whole reads as a single piece. Do NOT make separate "
       "cut-out objects floating on blank paper; do NOT mix realistic photos with drawings; NOT a collage.")

PROMPTS = {
 "A": (f"A cohesive hand-painted MURAL for GCSE Biology: {IDEAS} — all interwoven and flowing into one another "
       f"through shared organic forms (vines, veins, membranes, roots) so the ideas blend across one continuous "
       f"scene. Detailed pen-and-ink line with soft watercolour washes, a single calm sage-green and warm-ochre "
       f"palette. {CON} {NO}"),
 "B": (f"A vintage scientific WALL-CHART tapestry for GCSE Biology in one unified antique engraving / lithograph "
       f"style and a single muted green palette: {IDEAS}, all connected by decorative flourishes, tendrils and "
       f"flowing lines into one ornate continuous naturalist panel. {CON} {NO}"),
 "C": (f"An ART-NOUVEAU decorative TAPESTRY of GCSE Biology ideas: {IDEAS}, stylised and interlaced with sinuous "
       f"flowing lines and botanical borders in the manner of a woven William-Morris panel, one flat unified palette "
       f"of sage green, cream and soft gold, everything connected edge to edge like fabric. {CON} {NO}"),
 "D": (f"One continuous SCREEN-PRINT illustration banding GCSE Biology together: {IDEAS}, drawn in a single bold "
       f"modern editorial line-illustration style with a limited 3-colour palette (sage green, warm cream, deep "
       f"ink), elements overlapping and connected by flowing contour lines into one seamless composition. {CON} {NO}"),
}

def extract(r):
    for c in (r.candidates or []):
        for p in (c.content.parts or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

cfg = types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio="21:9"))
for k, prompt in PROMPTS.items():
    try:
        r = client.models.generate_content(model="gemini-3-pro-image-preview", contents=[prompt], config=cfg)
        data = extract(r)
        if data:
            out = os.path.join(ASSETS, f"_tap-{k}.png")
            open(out, "wb").write(data)
            print(f"{k}: saved {Image.open(out).size}", flush=True)
        else:
            print(f"{k}: no image", flush=True)
    except Exception as e:
        print(f"{k}: err {str(e)[:140]}", flush=True)
