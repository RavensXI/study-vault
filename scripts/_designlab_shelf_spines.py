"""Paint the classic dashboard's bookshelf: nine subject spines (cloth colour
+ small motif, line-and-wash, prompt-only, NO text), one shelf plank, one
amber bookmark ribbon. Each spine is cut to alpha (paper background removed)
so the dashboard can stack sketch/colour copies for the ink-fill effect.
Outputs design-lab/assets/lw/shelf/{slug}.png (+ plank.png, ribbon.png).
"""
import io, os, time
from google import genai
from google.genai import types
from PIL import Image
import numpy as np
from scipy.ndimage import binary_dilation, binary_fill_holes, gaussian_filter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw", "shelf")
os.makedirs(OUT, exist_ok=True)
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3-pro-image-preview"

STYLE = ("REFINED line-and-wash study: clean confident pen-and-ink linework with thin "
         "watercolour washes. ONE closed cloth-bound hardback book standing upright, seen "
         "exactly from its SPINE side so the spine faces the viewer square-on: a tall "
         "chunky rounded spine, its width about one fifth of its height, filling most of "
         "the frame height, isolated on plain pale warm paper, nothing else in frame. "
         "ABSOLUTELY NO text, letters, numbers or titles anywhere.")

SPINES = {
  "maths":   ("slate blue-grey cloth ({}), a small drawn pair of compasses emblem near the head of the spine", "#4e5f66"),
  "lang":    ("dusty steel-blue cloth ({}), a small quill pen emblem near the head of the spine", "#5b7285"),
  "lit":     ("muted plum cloth ({}), a small theatre-masks emblem near the head of the spine", "#7d5a78"),
  "science": ("sage green cloth ({}), a small conical flask emblem near the head of the spine", "#4e6e5d"),
  "history": ("warm russet-brown cloth ({}), a small laurel wreath emblem near the head of the spine", "#8a5a44"),
  "geog":    ("moss green cloth ({}), a small globe emblem near the head of the spine", "#6d7a4e"),
  "spanish": ("terracotta cloth ({}), a small fan emblem near the head of the spine", "#a2643f"),
  "cs":      ("cool graphite-blue cloth ({}), a small circuit-node emblem near the head of the spine", "#54606e"),
  "rs":      ("muted violet cloth ({}), a small dove emblem near the head of the spine", "#6f5b91"),
}
EXTRAS = {
  "plank":  "REFINED line-and-wash study: a long horizontal wooden bookshelf plank seen straight-on, warm honey-brown wood with subtle grain, thin watercolour wash, isolated on plain pale warm paper, nothing else. ABSOLUTELY NO text.",
  "ribbon": "REFINED line-and-wash study: a single small amber-orange silk bookmark ribbon hanging straight down with a neat angled cut tail, isolated on plain pale warm paper, nothing else in frame. ABSOLUTELY NO text.",
}

def extract(r):
    for c in (r.candidates or []):
        for p in (getattr(getattr(c, "content", None), "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen(prompt, aspect):
    for attempt in range(4):
        for cfg in (types.GenerateContentConfig(response_modalities=["IMAGE"],
                        image_config=types.ImageConfig(aspect_ratio=aspect)),
                    types.GenerateContentConfig(response_modalities=["IMAGE"])):
            try:
                r = client.models.generate_content(model=MODEL, contents=[prompt], config=cfg)
                d = extract(r)
                if d: return Image.open(io.BytesIO(d)).convert("RGB")
            except Exception as e:
                if any(k in str(e) for k in ("503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED")):
                    time.sleep(5 * (attempt + 1)); break
                raise
    raise RuntimeError("gen failed")

def cut_alpha(im, feather=1.2):
    """Remove the near-uniform paper background: distance from median corner
    colour -> alpha, holes filled so pale cloth interiors survive."""
    a = np.array(im).astype(np.float64)
    corners = np.concatenate([a[:12, :12].reshape(-1, 3), a[:12, -12:].reshape(-1, 3),
                              a[-12:, :12].reshape(-1, 3), a[-12:, -12:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    dist = np.sqrt(((a - bg) ** 2).sum(axis=2))
    obj = dist > 26
    obj = binary_fill_holes(binary_dilation(obj, iterations=2))
    # keep only the largest connected piece (drops detached paper patches)
    from scipy.ndimage import label as cclabel
    lab, n = cclabel(obj)
    if n > 1:
        sizes = np.bincount(lab.ravel()); sizes[0] = 0
        obj = lab == sizes.argmax()
    alpha = gaussian_filter(obj.astype(np.float64), feather)
    ys, xs = np.where(alpha > 0.5)
    if len(ys) == 0: raise RuntimeError("empty cut")
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgba = np.dstack([a, alpha[..., None] * 255]).astype(np.uint8)
    return Image.fromarray(rgba[y0:y1, x0:x1], "RGBA")

for slug, (desc, hexc) in SPINES.items():
    p = os.path.join(OUT, slug + ".png")
    if os.path.exists(p): print("have", slug); continue
    im = gen(STYLE + " The spine is " + desc.format("similar to " + hexc) + ".", "1:1")
    cut_alpha(im).save(p)
    print("made", slug, flush=True)
for name, prompt in EXTRAS.items():
    p = os.path.join(OUT, name + ".png")
    if os.path.exists(p): print("have", name); continue
    im = gen(prompt, "16:9" if name == "plank" else "1:1")
    cut_alpha(im).save(p)
    print("made", name, flush=True)
print("done ->", OUT)
