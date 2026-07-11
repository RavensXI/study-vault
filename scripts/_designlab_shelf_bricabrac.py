"""Bric-a-brac to replace the sacked L-bookends (Tom, 12 Jul): solid objects
books can visibly lean on. Same pipeline as the atmosphere props, with the
SAFE repair baked in (peel white slivers; open only true-paper enclosed holes;
never eat pale object regions in the lower half).

Run: python scripts/_designlab_shelf_bricabrac.py [keys...]
"""
import io, os, sys, time
from google import genai
from google.genai import types
from PIL import Image
import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion, binary_fill_holes, gaussian_filter, label as cclabel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw", "shelf")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3-pro-image-preview"
PAPER = np.array([250.0, 247.0, 240.0])

def on_white(path):
    im = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", im.size, (252, 249, 243, 255))
    bg.alpha_composite(im)
    return bg.convert("RGB")

LAMP = on_white(os.path.join(OUT, "lamp.webp"))

STYLE = ("English line-and-wash watercolour illustration in EXACTLY the style of the attached "
         "brass lamp: confident warm sepia ink outlines, controlled transparent watercolour "
         "washes, believable material colour, plain pale warm paper background and NOTHING else "
         "in frame. The object is drawn STRAIGHT-ON at eye level (no three-quarter perspective, "
         "no visible top surface) and casts NO shadow. Exactly ONE object, filling most of the frame. ")

OBJECTS = {
    "trophy":    ("A small brass two-handled trophy cup on a short dark wooden plinth base — a "
                  "modest school prize cup, polished but aged, completely plain with no "
                  "engraving and no lettering.", "3:4"),
    "pencilpot": ("A sturdy ceramic pot with a deep teal glaze holding a loose bunch of wooden "
                  "pencils of slightly different heights. Simple and solid, wider at the base "
                  "than a cup.", "3:4"),
    "owl":       ("A small carved dark-wood owl figurine with simple rounded forms, big carved "
                  "eyes, sitting upright — a bookish study ornament.", "3:4"),
    "handbell":  ("A small brass school hand bell resting mouth-down on its rim, with a dark "
                  "turned wooden handle pointing straight up.", "3:4"),
}

def extract(r):
    for c in (r.candidates or []):
        for p in (getattr(getattr(c, "content", None), "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen(contents, aspect):
    for attempt in range(5):
        try:
            r = client.models.generate_content(
                model=MODEL, contents=contents,
                config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio=aspect)))
            d = extract(r)
            if d: return Image.open(io.BytesIO(d)).convert("RGB")
        except Exception as e:
            if any(k in str(e) for k in ("503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED")):
                time.sleep(6 * (attempt + 1)); continue
            raise
    raise RuntimeError("gen failed")

def cut(im):
    a = np.array(im).astype(np.float64)
    corners = np.concatenate([a[:14,:14].reshape(-1,3), a[:14,-14:].reshape(-1,3),
                              a[-14:,:14].reshape(-1,3), a[-14:,-14:].reshape(-1,3)])
    bg = np.median(corners, axis=0)
    obj = np.sqrt(((a-bg)**2).sum(axis=2)) > 30
    obj = binary_fill_holes(binary_dilation(obj, iterations=2))
    lab, n = cclabel(obj)
    if n > 1:
        sz = np.bincount(lab.ravel()); sz[0] = 0
        obj = lab == sz.argmax()
    obj = binary_erosion(obj, iterations=2)
    obj = binary_fill_holes(obj)
    alpha = gaussian_filter(obj.astype(np.float64), 1.1)
    mn = a.min(axis=2)
    alpha[(alpha>0.05)&(alpha<0.95)&(mn>212)] = 0.0
    core = binary_erosion(alpha>0.5, iterations=1)
    alpha = np.clip(gaussian_filter(np.maximum(alpha, core.astype(np.float64)), 0.7), 0, 1)
    return a, alpha * 255

def safe_repair(rgb, alpha):
    """Peel white slivers from edges; open ONLY true-paper enclosed holes in the
    upper half (lower-half pale regions are object highlights, never holes)."""
    d = np.sqrt(((rgb - PAPER) ** 2).sum(axis=2))
    white = d < 34
    for _ in range(8):
        tr = alpha < 40
        touch = binary_dilation(tr) & white & (alpha >= 40)
        if not touch.any(): break
        alpha[touch] = 0
    H = alpha.shape[0]
    hole = (d < 16) & (alpha >= 40)
    lab, n = cclabel(hole)
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 80: continue
        ys, xs = np.where(m)
        if ys.mean() > H * 0.5: continue   # lower half = object body, keep
        alpha[m] = 0
    return alpha

def export(rgb, alpha, key, h=520):
    ys, xs = np.where(alpha > 128)
    y0,y1,x0,x1 = ys.min(), ys.max()+1, xs.min(), xs.max()+1
    rgba = np.dstack([rgb, alpha]).astype(np.uint8)[y0:y1, x0:x1]
    out = Image.fromarray(rgba, "RGBA")
    if out.height > h:
        out = out.resize((round(out.width*h/out.height), h), Image.LANCZOS)
    out.save(os.path.join(OUT, f"prop_{key}.png"))
    out.save(os.path.join(OUT, f"prop_{key}.webp"), quality=82, method=6)

only = sys.argv[1:]
for key, (body, aspect) in OBJECTS.items():
    if only and key not in only: continue
    if os.path.exists(os.path.join(OUT, f"prop_{key}.png")) and not only:
        print("have", key); continue
    im = gen([STYLE + body, LAMP], aspect)
    rgb, alpha = cut(im)
    alpha = safe_repair(rgb, alpha)
    export(rgb, alpha, key)
    print("made", key, flush=True)
print("done ->", OUT)
