"""Generate a StudyVault bookend for the classic-dashboard shelf — line-and-wash,
matching the painted book spines, cut to alpha. A few candidates to pick from.
Outputs design-lab/assets/lw/shelf/bookend_{name}.png
"""
import io, os, time
from google import genai
from google.genai import types
from PIL import Image
import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion, binary_fill_holes, gaussian_filter, label as cclabel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw", "shelf")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3-pro-image-preview"

STYLE = ("Refined pen-and-ink linework with soft watercolour washes on cold-press paper, "
         "the same illustration style as a hand-painted cloth book spine. Plain flat white "
         "background, nothing else, no shadow on the ground.")
VARIANTS = {
  "brass": ("REFINED line-and-wash illustration of a single ornamental BRASS BOOKEND standing "
            "upright, seen straight-on from the front. An L-shaped aged-brass bookend: a tall "
            "slim vertical panel with a gently arched top, and a short foot at the base. Warm "
            "aged brass with soft patina and gentle highlights. A small embossed PADLOCK emblem "
            "centred in the upper third of the panel. Tall and narrow, about the height of a "
            "hardback book. " + STYLE),
  "walnut": ("REFINED line-and-wash illustration of a single ornamental WALNUT WOOD BOOKEND "
             "standing upright, seen straight-on from the front. An L-shaped dark walnut bookend: "
             "a tall slim vertical panel with a softly rounded top and a short foot at the base, "
             "warm wood grain and soft sheen. A small embossed brass PADLOCK emblem centred in "
             "the upper third. Tall and narrow, about the height of a hardback book. " + STYLE),
  "brass2": ("REFINED line-and-wash illustration of a single heavy BRASS BOOKEND standing upright, "
             "seen straight-on. A solid classical brass bookend shaped like a slim fluted pillar "
             "with a small decorative capital at the top and a stepped base, aged brass with soft "
             "patina. A small round PADLOCK medallion set into the pillar. Tall and narrow, about "
             "the height of a hardback book. " + STYLE),
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
                    image_config=types.ImageConfig(aspect_ratio="3:4")))
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
    obj = np.sqrt(((a - bg) ** 2).sum(axis=2)) > 32
    obj = binary_fill_holes(binary_dilation(obj, iterations=2))
    lab, n = cclabel(obj)
    if n > 1:
        sz = np.bincount(lab.ravel()); sz[0] = 0
        obj = lab == sz.argmax()
    obj = binary_erosion(obj, iterations=2)
    obj = binary_fill_holes(obj)
    alpha = gaussian_filter(obj.astype(np.float64), 1.1)
    mn = a.min(axis=2)
    fringe = (alpha > 0.05) & (alpha < 0.95) & (mn > 212)
    alpha[fringe] = 0.0
    core = binary_erosion(alpha > 0.5, iterations=1)
    alpha = np.clip(gaussian_filter(np.maximum(alpha, core.astype(np.float64)), 0.7), 0, 1)
    ys, xs = np.where(alpha > 0.5)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgba = np.dstack([a, alpha * 255]).astype(np.uint8)[y0:y1, x0:x1]
    return Image.fromarray(rgba, "RGBA")

for name, prompt in VARIANTS.items():
    p = os.path.join(OUT, "bookend_" + name + ".png")
    if os.path.exists(p): print("have", name); continue
    cut(gen(prompt)).save(p)
    print("made", name, flush=True)
print("done ->", OUT)
