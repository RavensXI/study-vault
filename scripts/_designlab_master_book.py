"""Option 2: ONE master book, recoloured. Generate a few grayscale line-and-wash
book candidates (spine view). Grayscale so the SAME painting serves as both the
'unpainted/pencil' state AND, tinted per subject, the painted state — the fill
just reveals the tint up from the bottom. Cut to alpha; light-normalised so
multiply-tint stays vivid. Outputs design-lab/assets/lw/shelf/master{N}.png
"""
import io, os, time
from google import genai
from google.genai import types
from PIL import Image
import numpy as np
from scipy.ndimage import binary_dilation, binary_fill_holes, gaussian_filter, label as cclabel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw", "shelf")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3-pro-image-preview"

BASE = ("REFINED line-and-wash study in GRAYSCALE ONLY (no colour, warm neutral grays): "
        "one closed cloth-bound hardback book standing upright, viewed square-on from the "
        "SPINE side so the spine faces the viewer, tall with gently rounded corners and a "
        "soft rolled head-cap at the top. Clean confident pen-and-ink linework with soft "
        "grey watercolour shading — a little darker down each side edge, lighter through "
        "the centre, on cold-press paper. Filling most of the frame height, isolated on "
        "plain pale warm paper, nothing else. ABSOLUTELY NO text, letters, numbers or titles.")
VARIANTS = {
  "master1": BASE + " Three subtle raised horizontal binding bands across the spine.",
  "master2": BASE + " Five raised horizontal binding bands and a small blank rectangular "
             "label panel in the upper third (empty, no text).",
  "master3": BASE + " A smooth spine with a single faint groove near the top and bottom, "
             "no bands, softly worn corners.",
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
                    image_config=types.ImageConfig(aspect_ratio="9:16")))
            d = extract(r)
            if d: return Image.open(io.BytesIO(d)).convert("RGB")
        except Exception as e:
            if any(k in str(e) for k in ("503", "429", "UNAVAILABLE")):
                time.sleep(5 * (attempt + 1)); continue
            raise
    raise RuntimeError("gen failed")

def cut(im):
    a = np.array(im).astype(np.float64)
    corners = np.concatenate([a[:14, :14].reshape(-1, 3), a[:14, -14:].reshape(-1, 3),
                              a[-14:, :14].reshape(-1, 3), a[-14:, -14:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    obj = np.sqrt(((a - bg) ** 2).sum(axis=2)) > 24
    obj = binary_fill_holes(binary_dilation(obj, iterations=2))
    lab, n = cclabel(obj)
    if n > 1:
        sz = np.bincount(lab.ravel()); sz[0] = 0
        obj = lab == sz.argmax()
    alpha = gaussian_filter(obj.astype(np.float64), 1.1)
    # to grayscale, light-normalised so multiply-tint stays vivid (ink stays dark)
    g = np.array(im.convert("L")).astype(np.float64)
    g = (g - g.min()) / max(1, g.max() - g.min())
    g = 0.30 + g * 0.70                       # ink ~0.30, cloth ~0.8-1.0
    gg = (g * 255).astype(np.uint8)
    ys, xs = np.where(alpha > 0.5)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgba = np.dstack([gg, gg, gg, (alpha * 255).astype(np.uint8)])[y0:y1, x0:x1]
    return Image.fromarray(rgba, "RGBA")

for name, prompt in VARIANTS.items():
    p = os.path.join(OUT, name + ".png")
    if os.path.exists(p): print("have", name); continue
    cut(gen(prompt)).save(p)
    print("made", name, flush=True)
print("done ->", OUT)
