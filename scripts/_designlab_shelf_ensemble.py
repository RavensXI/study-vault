"""One painting, cut apart (the desk method): generate the ENTIRE shelf row
as a single line-and-wash artwork so all nine books share one perspective,
light and hand — then segment the plate into per-subject spine cutouts by
the paper-background valleys between books. Overwrites shelf/{slug}.png|webp
(same filenames -> dashboard code unchanged).
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

# left -> right on the shelf = SUBJECTS order; hues distinct enough to auto-match
ORDER = ["maths", "lang", "lit", "science", "history", "geog", "spanish", "cs", "rs"]
HEX = {"maths": (78, 95, 102), "lang": (91, 114, 133), "lit": (125, 90, 120),
       "science": (78, 110, 93), "history": (138, 90, 68), "geog": (109, 122, 78),
       "spanish": (162, 100, 63), "cs": (84, 96, 110), "rs": (111, 91, 145)}

PROMPT = ("REFINED line-and-wash study: clean confident pen-and-ink linework with thin "
          "watercolour washes on warm paper. A single straight-on row of NINE upright "
          "cloth-bound hardback books standing side by side with small clear gaps between "
          "them, all seen square-on from the spine side, all the same height, drawn "
          "together in one consistent perspective. Their cloth colours from left to right: "
          "slate blue-grey, dusty steel-blue, muted plum, sage green, warm russet-brown "
          "(this one thicker than the rest), moss green, terracotta, cool graphite-blue, "
          "muted violet. Plain pale warm paper background, no shelf, nothing else. "
          "ABSOLUTELY NO text, letters or numbers anywhere.")

def extract(r):
    for c in (r.candidates or []):
        for p in (getattr(getattr(c, "content", None), "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen():
    for attempt in range(4):
        try:
            r = client.models.generate_content(model=MODEL, contents=[PROMPT],
                config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="16:9")))
            d = extract(r)
            if d: return Image.open(io.BytesIO(d)).convert("RGB")
        except Exception as e:
            if any(k in str(e) for k in ("503", "429", "UNAVAILABLE")):
                time.sleep(5 * (attempt + 1)); continue
            raise
    raise RuntimeError("gen failed")

im = gen()
im.save(os.path.join(OUT, "_ensemble_master.png"))
a = np.array(im).astype(np.float64)
h, w, _ = a.shape
corners = np.concatenate([a[:14, :14].reshape(-1, 3), a[:14, -14:].reshape(-1, 3),
                          a[-14:, :14].reshape(-1, 3), a[-14:, -14:].reshape(-1, 3)])
bg = np.median(corners, axis=0)
dist = np.sqrt(((a - bg) ** 2).sum(axis=2))
obj = dist > 26
obj = binary_fill_holes(binary_dilation(obj, iterations=2))

# segment by columns: a column belongs to a book if enough object pixels
colmass = obj.sum(axis=0)
thresh = h * 0.15
on = colmass > thresh
# find runs
runs, x = [], 0
while x < w:
    if on[x]:
        x0 = x
        while x < w and on[x]: x += 1
        if x - x0 > w * 0.02: runs.append((x0, x))
    else:
        x += 1
print("books found:", len(runs))
assert len(runs) == 9, f"expected 9 books, got {len(runs)} — regenerate or adjust"

alpha_full = gaussian_filter(obj.astype(np.float64), 1.2)
sizes = []
for (x0, x1), slug in zip(runs, ORDER):
    seg_obj = obj[:, x0:x1]
    ys = np.where(seg_obj.any(axis=1))[0]
    y0, y1 = ys.min(), ys.max() + 1
    rgba = np.dstack([a[y0:y1, x0:x1], alpha_full[y0:y1, x0:x1, None] * 255]).astype(np.uint8)
    img = Image.fromarray(rgba, "RGBA")
    img.save(os.path.join(OUT, slug + ".png"))
    # colour sanity: dominant colour of lower half vs expected
    lower = a[y0 + (y1 - y0) // 2:y1, x0:x1][seg_obj[(y1 - y0) // 2:, :]]
    dom = lower.mean(axis=0)
    exp = np.array(HEX[slug], float)
    print(f"{slug:8s} w={x1-x0:4d} dom=({dom[0]:.0f},{dom[1]:.0f},{dom[2]:.0f}) exp={tuple(exp.astype(int))}")
    sizes.append((slug, x1 - x0, y1 - y0))
    # webp
    scale = 0.4
    img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.LANCZOS)\
       .save(os.path.join(OUT, slug + ".webp"), "WEBP", quality=88, alpha_quality=90, method=6)
print("segmented + saved 9 spines")
