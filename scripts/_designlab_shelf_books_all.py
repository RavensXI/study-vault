"""Paint the REST of the free-tier library: one titled, cloth-coloured book per
GCSE subject family (the 9 originals exist; this adds the other 25). Same
method as bookshelf v3: img2img from the grayscale master (shape) + a finished
book (gilt-lettering style), title baked into the art, cut to alpha, defringed,
exported at the same 650px height as the originals (png + webp).

Run:            python scripts/_designlab_shelf_books_all.py
Re-run safety:  skips any book whose .png already exists (delete to regen).
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

MASTER = Image.open(os.path.join(OUT, "master2.png")).convert("RGB")
EXAMPLE = Image.open(os.path.join(OUT, "book_history.png")).convert("RGB")

# key -> (spine title, cloth description, hex)
ROSTER = {
    "triple":      ("TRIPLE SCIENCE",        "deep pine-green cloth",       "#3d5c50"),
    "french":      ("FRENCH",                "cornflower-blue cloth",       "#5c72a4"),
    "german":      ("GERMAN",                "deep burgundy cloth",         "#7c4a52"),
    "business":    ("BUSINESS",              "dark navy cloth",             "#3f5570"),
    "econ":        ("ECONOMICS",             "bottle-green cloth",          "#35594e"),
    "psych":       ("PSYCHOLOGY",            "dusty rose cloth",            "#9c6b74"),
    "socio":       ("SOCIOLOGY",             "muted mauve cloth",           "#85688f"),
    "stats":       ("STATISTICS",            "steel-cyan cloth",            "#557a8a"),
    "pe":          ("PHYSICAL EDUCATION",    "muted vermilion-red cloth",   "#a34a3a"),
    "citizenship": ("CITIZENSHIP",           "blue-violet cloth",           "#5d5f8d"),
    "astro":       ("ASTRONOMY",             "midnight-blue cloth",         "#3c4a6b"),
    "geology":     ("GEOLOGY",               "warm stone-grey cloth",       "#6e6459"),
    "classics":    ("CLASSICAL CIVILISATION","pale olive-gold cloth",       "#9a8a5a"),
    "dt":          ("DESIGN & TECHNOLOGY",   "workshop-ochre cloth",        "#8a713b"),
    "eng":         ("ENGINEERING",           "gunmetal-grey cloth",         "#5a6068"),
    "electronics": ("ELECTRONICS",           "burnished copper-brown cloth (title in ONE single column, no wrapping)","#8f5b31"),
    "it":          ("I.T.",                  "cool blue-grey cloth",        "#4f6d7d"),
    "media":       ("MEDIA STUDIES",         "plum-mauve cloth",            "#6b4f63"),
    "film":        ("FILM STUDIES",          "charcoal cloth",              "#4a4a52"),
    "drama":       ("DRAMA",                 "deep crimson cloth",          "#8d3f4c"),
    "music":       ("MUSIC",                 "petrol-teal cloth",           "#446272"),
    "mtech":       ("MUSIC TECHNOLOGY",      "indigo cloth",                "#4c5480"),
    "food":        ("FOOD & NUTRITION",      "warm saffron cloth",          "#a8842f"),
    "hosp":        ("HOSPITALITY & CATERING","muted aubergine cloth",       "#67424e"),
    "hsc":         ("HEALTH & SOCIAL CARE",  "soft teal cloth",             "#4e7d78"),
}

def extract(r):
    for c in (r.candidates or []):
        for p in (getattr(getattr(c, "content", None), "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def prompt_for(title, desc, hexc):
    spelled = " ".join(list(title.replace(" ", "␣")))  # visible word gaps for the spelling line
    return (
        "The FIRST attached image is a grayscale line-and-wash master painting of a cloth hardback "
        "book seen square-on from its SPINE. The SECOND attached image is a finished example of the "
        "same book, recoloured with a cloth colour and given a gold gilt spine title. "
        f"Produce the SAME book again, identical shape, bands and brown leather label panel, but with: "
        f"(1) the cloth painted {desc} (close to {hexc}), keeping the line-and-wash watercolour feel; "
        f"(2) the spine title '{title}' in EXACTLY the same vertical gold gilt serif capitals as the "
        "second image, running top-to-bottom down the spine, fitted to the spine (wrap onto a second "
        "column of lettering if long, like a real bound book). "
        f"The title must be spelled EXACTLY, letter by letter: {spelled} — no other words. "
        "Exactly ONE single book in the frame, standing alone — no second book behind it, beside it, "
        "or lying flat. Plain pale warm paper background, the book filling most of the frame height, "
        "nothing else in frame."
    )

def gen(prompt):
    for attempt in range(5):
        try:
            r = client.models.generate_content(
                model=MODEL, contents=[prompt, MASTER, EXAMPLE],
                config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="9:16")))
            d = extract(r)
            if d: return Image.open(io.BytesIO(d)).convert("RGB")
        except Exception as e:
            if any(k in str(e) for k in ("503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED")):
                time.sleep(6 * (attempt + 1)); continue
            raise
    raise RuntimeError("gen failed")

def cut(im):
    """bookend2-style alpha cut with pale-fringe removal (the halo fix)."""
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

def export(rgba, key):
    h = 650
    w = max(1, round(rgba.width * h / rgba.height))
    small = rgba.resize((w, h), Image.LANCZOS)
    small.save(os.path.join(OUT, f"book_{key}.png"))
    small.save(os.path.join(OUT, f"book_{key}.webp"), quality=82, method=6)

only = sys.argv[1:]   # optionally regen specific keys
for key, (title, desc, hexc) in ROSTER.items():
    if only and key not in only: continue
    p = os.path.join(OUT, f"book_{key}.png")
    if os.path.exists(p) and not only:
        print("have", key); continue
    im = gen(prompt_for(title, desc, hexc))
    export(cut(im), key)
    print("made", key, "->", title, flush=True)
print("done ->", OUT)
