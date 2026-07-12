"""Lower-shelf props for the extended landing page (Tom, 12 Jul): the open
display book, the practice jotter, and the schools cupboard. Same pipeline as
the bric-a-brac (lamp img2img style anchor, corner-median cut, hole fill).

Run: python scripts/_designlab_shelf_lower.py            # all, 2 candidates each
     python scripts/_designlab_shelf_lower.py export openbook 2   # pick one
"""
import io, os, sys, time
from google import genai
from google.genai import types
from PIL import Image
import numpy as np
from scipy.ndimage import binary_dilation, binary_fill_holes, label as cclabel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw", "shelf")
RAW = os.path.join(ROOT, "design-lab", "assets", "lw", "_raw_lower")
os.makedirs(RAW, exist_ok=True)
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3-pro-image-preview"

def on_white(path):
    im = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", im.size, (252, 249, 243, 255))
    bg.alpha_composite(im)
    return bg.convert("RGB")

LAMP = on_white(os.path.join(OUT, "lamp.webp"))

STYLE = ("English line-and-wash watercolour illustration in EXACTLY the style of the attached "
         "brass lamp: confident warm sepia ink outlines, controlled transparent watercolour "
         "washes, believable material colour, plain pale warm paper background and NOTHING else "
         "in frame. The object is drawn STRAIGHT-ON at eye level (no three-quarter perspective) "
         "and casts NO shadow. Exactly ONE object, filling most of the frame. ")

OBJECTS = {
    "openbook": ("A hardback book propped open on a small dark wooden display stand, its open "
                 "pages FACING the viewer like a museum display. The two visible pages carry "
                 "soft, indistinct lines suggesting handwritten study notes and one small ink "
                 "diagram — NO legible words or letters. Cream pages, warm tan leather binding "
                 "just visible at the spine and corners.", "4:3"),
    "jotter":   ("A slim school exercise book standing upright and seen square-on: a plain "
                 "deep-teal soft cover with a small BLANK cream paper label near the top, "
                 "slightly dog-eared corner, and a yellow wooden pencil leaning against its "
                 "side.", "3:4"),
    "cupboard": ("The lower cupboard section of an old oak bookcase: two panelled cabinet "
                 "doors side by side, each with a small round brass knob, and one small BLANK "
                 "rectangular brass plate centred on the top rail above the doors. Aged warm "
                 "oak with honest grain, completely plain — no lettering anywhere.", "4:3"),
}

def extract(r):
    for c in (r.candidates or []):
        for p in (getattr(getattr(c, "content", None), "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data

def gen(prompt, aspect):
    for attempt in range(5):
        try:
            r = client.models.generate_content(model=MODEL, contents=[LAMP, STYLE + prompt],
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
    dist = np.sqrt(((a-bg)**2).sum(axis=2))
    alpha = np.where(obj, np.clip((dist-8)/26, 0, 1)*255, 0)
    # solid interior: anything inside the object mask but pale (pages) stays opaque
    core = binary_fill_holes(dist > 34)
    alpha = np.where(obj & core, np.maximum(alpha, 255*np.clip((dist-8)/26,0,1)), alpha)
    alpha = np.where(obj & ~ (dist>8), 255, alpha)   # enclosed pale interior = paper of the OBJECT
    out = np.dstack([a, np.clip(alpha,0,255)]).astype(np.uint8)
    img = Image.fromarray(out, "RGBA")
    bbox = Image.fromarray(out[:,:,3]).getbbox()
    return img.crop(bbox) if bbox else img

if len(sys.argv) > 3 and sys.argv[1] == "export":
    key, n = sys.argv[2], sys.argv[3]
    img = Image.open(os.path.join(RAW, f"{key}_{n}_cut.png"))
    img.save(os.path.join(OUT, f"prop_{key}.png"))
    img.save(os.path.join(OUT, f"prop_{key}.webp"), quality=92)
    print("exported", key, n)
    sys.exit(0)

keys = sys.argv[1:] or list(OBJECTS)
tiles = []
for key in keys:
    prompt, aspect = OBJECTS[key]
    for i in (1, 2):
        raw = gen(prompt, aspect)
        raw.save(os.path.join(RAW, f"{key}_{i}_raw.png"))
        c = cut(raw)
        c.save(os.path.join(RAW, f"{key}_{i}_cut.png"))
        tiles.append((f"{key}{i}", c))
        print("made", key, i, c.size)

sheet_tiles = []
for name, img in tiles:
    t = img.copy(); t.thumbnail((420, 330))
    tile = Image.new("RGB", (440, 350), (196, 174, 148))
    tile.paste(t, ((440-t.width)//2, (350-t.height)//2), t)
    sheet_tiles.append(tile)
cols = 2
rows = (len(sheet_tiles)+1)//2
sheet = Image.new("RGB", (440*cols+30, 350*rows+20), (60,50,40))
for i, tile in enumerate(sheet_tiles):
    sheet.paste(tile, (10+(i%cols)*450, 10+(i//cols)*360))
sheet.save(os.path.join(os.path.expanduser("~"), "Downloads", "lower_props_sheet.png"))
print("sheet -> Downloads/lower_props_sheet.png")
