"""Hand-sketched curved arrows for the landing page (Tom, 12 Jul): the SVG
wobble looked drawn-by-maths, so get real drawn ones from the same Gemini art
pipeline as the shelf props. Pure ink on paper -> ink-density alpha cut (no
background removal heuristics needed), natural pen texture kept.

Run: python scripts/_designlab_sketch_arrows.py            # generate candidates
     python scripts/_designlab_sketch_arrows.py export N   # export candidate N
"""
import io, os, sys, time
from google import genai
from google.genai import types
from PIL import Image
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw", "shelf")
RAW = os.path.join(ROOT, "design-lab", "assets", "lw", "_raw_arrows")
os.makedirs(RAW, exist_ok=True)
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3-pro-image-preview"

BASE = ("A single hand-drawn curved arrow, sketched quickly and confidently with a "
        "fine warm sepia-brown ink pen, like a teacher's annotation in a book margin. "
        "It begins at the TOP RIGHT of the frame, swoops down and leftward in one "
        "smooth confident curve, and ends at the MIDDLE LEFT with a small hand-drawn "
        "open arrowhead pointing up-and-left. Natural line-weight variation from pen "
        "pressure. Plain pale warm paper background and NOTHING else in the frame: "
        "no shadow, no text, exactly one arrow. ")

VARIANTS = [
    ("a", BASE),
    ("b", BASE + "The line is drawn with a relaxed, slightly loose sketchy energy, "
                 "with a hint of a second quick pass near the tail."),
]

def extract(r):
    for c in (r.candidates or []):
        for p in (getattr(getattr(c, "content", None), "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen(prompt):
    for attempt in range(5):
        try:
            r = client.models.generate_content(
                model=MODEL, contents=prompt,
                config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="16:9")))
            d = extract(r)
            if d: return Image.open(io.BytesIO(d)).convert("RGB")
        except Exception as e:
            if any(k in str(e) for k in ("503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED")):
                time.sleep(6 * (attempt + 1)); continue
            raise
    raise RuntimeError("gen failed")

def ink_cut(im):
    """Paper -> transparent via ink density; keeps pen texture and colour."""
    a = np.array(im).astype(np.float64)
    lum = a.mean(axis=2)
    paper = np.percentile(lum, 92)          # paper tone (bulk of the frame)
    ink = np.percentile(lum, 2)             # darkest ink
    alpha = np.clip((paper - 6 - lum) / max(paper - ink, 1), 0, 1)
    out = np.dstack([a, alpha * 255]).astype(np.uint8)
    img = Image.fromarray(out, "RGBA")
    bbox = Image.fromarray((alpha * 255).astype(np.uint8)).getbbox()
    return img.crop(bbox) if bbox else img

def contact_sheet(cands):
    """QA sheet on the wallpaper-ish midtone."""
    tiles = []
    for name, img in cands:
        t = img.copy(); t.thumbnail((560, 300))
        tile = Image.new("RGB", (580, 320), (238, 228, 210))
        tile.paste(t, ((580 - t.width) // 2, (320 - t.height) // 2), t)
        tiles.append((name, tile))
    sheet = Image.new("RGB", (580 * 2 + 30, 320 * ((len(tiles) + 1) // 2) + 20), (60, 50, 40))
    for i, (name, tile) in enumerate(tiles):
        sheet.paste(tile, (10 + (i % 2) * 590, 10 + (i // 2) * 330))
    p = os.path.join(os.path.expanduser("~"), "Downloads", "arrow_candidates.png")
    sheet.save(p); print("sheet ->", p)

if len(sys.argv) > 2 and sys.argv[1] == "export":
    n = sys.argv[2]
    img = Image.open(os.path.join(RAW, f"arrow_{n}_cut.png"))
    img.save(os.path.join(OUT, "arrow_sketch.png"))
    img.save(os.path.join(OUT, "arrow_sketch.webp"), quality=92)
    print("exported candidate", n, "->", OUT)
    sys.exit(0)

cands = []
for key, prompt in VARIANTS:
    for i in (1, 2):
        name = f"{key}{i}"
        raw = gen(prompt)
        raw.save(os.path.join(RAW, f"arrow_{name}_raw.png"))
        cut = ink_cut(raw)
        cut.save(os.path.join(RAW, f"arrow_{name}_cut.png"))
        cands.append((name, cut))
        print("made", name, cut.size)
contact_sheet(cands)
