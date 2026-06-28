"""Cohesion from STYLE, not from plumbing. Same unified flat screen-print style +
palette as D, but each subject is its OWN distinct illustration — no veins / tubes /
tendrils joining unrelated objects. Find the right balance of distinct-vs-composed.
Outputs design-lab/assets/_tap2-{E,F,G}.png  (Biology Paper 1)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

SUBJECTS = ("microscope, an animal cell, a heart, a leaf cross-section, lungs, white blood cells, a DNA double helix, "
            "a green plant, a small ecosystem")
STYLE = ("ONE unified flat modern SCREEN-PRINT illustration style and a single limited palette of sage green, warm "
         "cream and deep ink — even line weight, flat shapes, the same treatment for everything.")
NOJOIN = ("Each subject is its OWN distinct, clearly-readable illustration. They are unified ONLY by the shared flat "
          "style and palette — absolutely NO veins, tubes, arteries, tendrils, vines, roots, wires or flowing lines "
          "running between different objects; do NOT merge, plumb or fuse separate objects into one another; no "
          "background scenery linking them. Warm off-white paper. NO text, letters, numbers or labels.")

PROMPTS = {
 "E": (f"A wide horizontal banner of GCSE Biology subjects: {SUBJECTS}. {STYLE} A calm, balanced arrangement with "
       f"comfortable breathing space around each subject. {NOJOIN}"),
 "F": (f"A wide horizontal banner of GCSE Biology subjects: {SUBJECTS}. {STYLE} Composed close together like a "
       f"well-designed poster, the shapes gently tessellating and slightly overlapping at their edges, but every "
       f"object stays a distinct recognisable thing. {NOJOIN}"),
 "G": (f"A wide horizontal banner: an evenly-spaced clean SPECIMEN-PLATE poster of distinct GCSE Biology subjects: "
       f"{SUBJECTS}. {STYLE} Generous warm-paper margins, each subject crisp and clearly separated like a tidy "
       f"printed chart. {NOJOIN}"),
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
            out = os.path.join(ASSETS, f"_tap2-{k}.png")
            open(out, "wb").write(data); print(f"{k}: saved {Image.open(out).size}", flush=True)
        else:
            print(f"{k}: no image", flush=True)
    except Exception as e:
        print(f"{k}: err {str(e)[:140]}", flush=True)
