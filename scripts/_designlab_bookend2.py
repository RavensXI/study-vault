"""Pass 2 shelf furniture: a SOLID, perfectly-upright StudyVault bookend (heavy enough
to actually stop books) + a lamp for the right side whose head points LEFT to light the
books. Line-and-wash to match the painted spines, cut to alpha.
Outputs design-lab/assets/lw/shelf/{bookend2_*,lamp_*}.png
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
         "same hand-painted style as a cloth hardback book spine. Plain flat pure-white background, "
         "the object filling the frame, nothing else, no cast shadow on the ground.")
STRAIGHT = ("Perfectly upright and symmetrical, seen EXACTLY straight-on from the front, flat "
            "orthographic view, no perspective, no tilt, no rotation. ")

JOBS = {
  # --- solid bookends: read as heavy, could really stop a row of books ---
  "bookend2_brass": (STRAIGHT + "A SOLID heavy polished-brass bookend: a thick rectangular block "
     "with softly chamfered edges and a small stepped plinth at the base, substantial mass, clearly "
     "heavy metal. A raised embossed PADLOCK crest centred on the face. Aged warm brass with soft "
     "highlights. About the height of a hardback book. " + STYLE, "3:4"),
  "bookend2_marble": (STRAIGHT + "A SOLID heavy bookend carved from a single block of pale grey "
     "veined marble, a chunky upright rectangular block with a bevelled top and a stout base, obvious "
     "weight and thickness. A small aged-brass PADLOCK medallion inset in the centre of the face. "
     "About the height of a hardback book. " + STYLE, "3:4"),
  "bookend2_iron": (STRAIGHT + "A SOLID heavy cast-iron bookend, a chunky upright wedge/block of dark "
     "blackened iron with rounded corners and a heavy base, clearly dense and heavy. A raised PADLOCK "
     "motif cast into the centre of the face, faint warm highlights on the dark metal. About the height "
     "of a hardback book. " + STYLE, "3:4"),
  # --- lamps for the RIGHT side, head pointing LEFT to light the books ---
  "lamp_angle": ("A classic adjustable brass desk lamp (anglepoise style) standing on its round base, "
     "the jointed arm reaching UP and bending OVER so the conical shade/head points to the LEFT and "
     "slightly down, casting a warm pool of light to the left. Aged brass, warm glow at the shade mouth. "
     "Seen from the side, upright base, the whole lamp about one and a half book-heights tall. " + STYLE, "3:4"),
  "lamp_banker": ("A classic brass banker's lamp with a domed green glass shade on a slim brass column and "
     "round base, the green shade tilted so its opening faces LEFT to throw warm light to the left. Aged "
     "brass fittings, soft warm glow under the shade. Seen from the side, upright, about one and a quarter "
     "book-heights tall. " + STYLE, "3:4"),
  "lamp_task": ("A slim brass library task lamp: a round weighted base, a straight column, and a small "
     "cylindrical brass shade on a swan-neck bend at the top angled to point LEFT and down, warm light "
     "spilling to the left. Aged brass. Seen from the side, upright, about one and a half book-heights "
     "tall. " + STYLE, "3:4"),
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
