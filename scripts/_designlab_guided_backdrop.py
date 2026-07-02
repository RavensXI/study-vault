"""Generate bespoke line-and-wash BACKDROP art for the dashboard's Guided door.
Unlike lesson heroes (composed to be looked AT), these are composed to sit BEHIND
text: detail anchored lower-right, upper-left fading to near-blank cream paper.
Three motif candidates -> design-lab/assets/lw/guided-{a,b,c}.png
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

CANDIDATES = {
    "guided-a": ("A narrow footpath winding up from the foreground through soft rolling hills, past a couple "
                 "of small hedgerow trees, toward a small hilltop landmark tower on the far horizon in light morning haze"),
    "guided-b": ("A winding country lane with a weathered wooden fingerpost at a fork, gentle patchwork fields "
                 "beyond, and a distant village church spire on the horizon at dawn"),
    "guided-c": ("A single hot-air balloon drifting low over gentle patchwork fields toward distant soft hills, "
                 "its long shadow trailing on the fields below"),
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
                if any(k in msg for k in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                    time.sleep(5 * (attempt + 1)); break
                return None, msg[:90]
    return None, "refused/empty"

for name, scene in CANDIDATES.items():
    img, err = render(scene + STYLE)
    if img:
        path = os.path.join(OUT, name + ".png")
        img.save(path)
        print(f"ok  {name}.png  {img.size}", flush=True)
    else:
        print(f"FAILED {name}: {err}", flush=True)
