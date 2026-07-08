"""A glow-less brass desk lamp — the SWITCHED-OFF fixture only, so the scene's
light can be done entirely in CSS. Line-and-wash, cut to alpha.
Outputs design-lab/assets/lw/shelf/lampoff_*.png
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

STYLE = ("Refined pen-and-ink linework with soft watercolour washes on cold-press paper, the "
         "same hand-painted style as a cloth book spine. Plain flat PURE-WHITE background, nothing "
         "else at all — no cast shadow, no light, no glow anywhere in the image.")
OFF = ("IMPORTANT: the lamp is SWITCHED OFF. There is NO light, NO glow, NO warm wash, NO "
       "illumination and NO bright bulb — the inside of the shade is dark and shadowed. Do not "
       "paint any light spilling from the shade. ")

JOBS = {
  "lampoff_a": (OFF + "A classic adjustable brass desk lamp (anglepoise style) standing on its round "
     "weighted base, the jointed arm reaching UP and bending OVER so the conical shade points to the "
     "LEFT and slightly down. Aged brass, dark empty shade interior. Seen from the side, upright base, "
     "about one and a half book-heights tall. " + STYLE, "3:4"),
  "lampoff_b": (OFF + "A compact brass desk lamp: a round weighted base, a short curved brass arm, and a "
     "conical brass shade at the top angled to point LEFT and down. Aged brass, the shade interior dark "
     "and unlit. Seen from the side, upright, a little taller than a hardback book. " + STYLE, "3:4"),
}

def extract(r):
    for c in (r.candidates or []):
        for p in (getattr(getattr(c, "content", None), "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen(prompt, ar):
    for attempt in range(4):
        try:
            r = client.models.generate_content(model=MODEL, contents=[prompt],
                config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio=ar)))
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
    obj = np.sqrt(((a - bg) ** 2).sum(axis=2)) > 30
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

for name, (prompt, ar) in JOBS.items():
    p = os.path.join(OUT, name + ".png")
    if os.path.exists(p): print("have", name); continue
    cut(gen(prompt, ar)).save(p)
    print("made", name, flush=True)
print("done ->", OUT)
