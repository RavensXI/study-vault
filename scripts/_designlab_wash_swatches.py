"""Generate a few neutral, tintable watercolour-wash swatches for the SVG book
fill (option 1: texture-filled SVG). Grayscale-warm so they tint cleanly to any
subject colour via multiply/overlay. Outputs design-lab/assets/lw/shelf/wash{N}.png
"""
import io, os, time
from google import genai
from google.genai import types
from PIL import Image
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw", "shelf")
os.makedirs(OUT, exist_ok=True)
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3-pro-image-preview"

PROMPTS = {
  "wash1": ("A flat rectangular swatch of a single soft watercolour wash on cold-press "
            "paper, warm neutral gray, gentle tonal mottling and granulation, subtle "
            "paper grain, a few darker pooled edges, no objects, no text — just the "
            "painted paper surface filling the whole frame."),
  "wash2": ("A rectangular swatch of layered watercolour washes, warm pale gray, visible "
            "brush streaks running vertically, soft bleeds and back-runs, cold-press paper "
            "texture, no objects or text — just the painted surface edge to edge."),
  "wash3": ("A rectangular swatch of a granulating watercolour wash, neutral warm gray, "
            "heavy paper tooth, speckled pigment settling into the paper valleys, uneven "
            "tone, no objects or text — the painted paper surface filling the frame."),
}

def extract(r):
    for c in (r.candidates or []):
        for p in (getattr(getattr(c, "content", None), "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen(prompt):
    for attempt in range(4):
        try:
            r = client.models.generate_content(model=MODEL, contents=[prompt],
                config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="1:1")))
            d = extract(r)
            if d: return Image.open(io.BytesIO(d)).convert("RGB")
        except Exception as e:
            if any(k in str(e) for k in ("503", "429", "UNAVAILABLE")):
                time.sleep(5 * (attempt + 1)); continue
            raise
    raise RuntimeError("gen failed")

for name, prompt in PROMPTS.items():
    p = os.path.join(OUT, name + ".png")
    if os.path.exists(p): print("have", name); continue
    im = gen(prompt)
    # normalise to a clean tintable luminance swatch: stretch to a soft mid-high range
    a = np.array(im.convert("L")).astype(np.float64)
    a = (a - a.min()) / max(1, a.max() - a.min())
    a = 0.62 + a * 0.38                     # keep it light so multiply-tint stays vivid
    g = (a * 255).astype(np.uint8)
    Image.fromarray(np.dstack([g, g, g]), "RGB").resize((360, 360)).save(p)
    print("made", name, flush=True)
print("done ->", OUT)
