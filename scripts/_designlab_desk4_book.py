"""Desk v4 notebook plate: an open notebook drawn at a gentle desk angle in
the scene's style, pages blank (live HTML text gets homography-mapped onto
them), no tabs (tabs stay live HTML). Generated on plain cream paper, then
flood-fill cut to a transparent plate like the other desk objects.
Writes design-lab/assets/lw/desk4-book-{a,b}.png (raw) and -cut.png.
"""
import os, io, time
import numpy as np
from google import genai
from google.genai import types
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw")
SCENE = os.path.join(OUT, "desk4-scene-a.png")
MOCK = r"C:\Users\tshau\Downloads\Gemini_Generated_Image_iaw6cbiaw6cbiaw6.jpg"

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
IMG_MODEL = "gemini-3-pro-image-preview"

PROMPT = (
    "In exactly the style of the attached reference images (hand-drawn pen-and-ink with soft "
    "watercolour wash, warm muted colours), draw ONE object on a plain warm cream paper "
    "background: an open A5 hardback notebook seen from a seated three-quarter view, as if "
    "lying on a desk in front of the viewer, rotated three or four degrees anticlockwise, with "
    "GENTLE perspective — only slightly foreshortened, the spread still close to rectangular. "
    "Thick cream pages, soft curvature where they rise over the spine, a stack of page edges "
    "visible along the bottom and right fore-edge, dark cloth cover just visible at the rim, an "
    "elastic strap hanging off the lower cover, and a soft watercolour shadow beneath it on the "
    "paper. Both pages COMPLETELY BLANK cream paper — no ruled lines, no text, no tabs, no "
    "bookmarks, no pen. The notebook fills most of the frame. ABSOLUTELY NO text or letters."
)

def extract(r):
    for c in (r.candidates or []):
        for p in (getattr(getattr(c, "content", None), "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def cut(src_path, out_path, thr=30.0, band=6):
    im = Image.open(src_path).convert("RGB")
    w, h = im.size
    cx, cy = int(w * .03), int(h * .03)
    im = im.crop((cx, cy, w - cx, h - cy))
    a = np.asarray(im).astype(np.float32)
    H, W = a.shape[:2]
    ring = np.concatenate([a[:12].reshape(-1,3), a[-12:].reshape(-1,3),
                           a[:, :12].reshape(-1,3), a[:, -12:].reshape(-1,3)])
    paper = np.median(ring, axis=0)
    dist = np.sqrt(((a - paper) ** 2).sum(axis=2))
    lab, n = ndimage.label(dist < thr)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:,0], lab[:,-1]]))
    mask = ~np.isin(lab, border[border != 0])
    lab2, n2 = ndimage.label(mask)
    sizes = ndimage.sum(mask, lab2, range(1, n2+1))
    keep = np.zeros(n2+1, bool); keep[1:] = sizes >= 200
    mask = keep[lab2]
    interior = ndimage.binary_erosion(mask, iterations=band)
    soft = np.clip(dist / thr, 0, 1)
    alpha = np.where(interior, 1.0, np.where(mask, soft*(3-2*soft), 0.0))
    alpha = ndimage.gaussian_filter(alpha, 1.0) * mask
    a8 = (np.clip(alpha,0,1)*255).astype(np.uint8)
    ys, xs = np.where(a8 > 8)
    p = 8
    y0,y1,x0,x1 = max(ys.min()-p,0), min(ys.max()+p,H), max(xs.min()-p,0), min(xs.max()+p,W)
    rgba = np.dstack([a.astype(np.uint8), a8])[y0:y1, x0:x1]
    Image.fromarray(rgba, "RGBA").save(out_path)
    return rgba.shape[1], rgba.shape[0]

scene = open(SCENE, "rb").read()
mock = open(MOCK, "rb").read()
for tag in ("a", "b"):
    raw = os.path.join(OUT, f"desk4-book-{tag}.png")
    if not os.path.exists(raw):
        img = None
        for attempt in range(4):
            try:
                r = client.models.generate_content(model=IMG_MODEL,
                    contents=[PROMPT,
                              types.Part.from_bytes(data=scene, mime_type="image/png"),
                              types.Part.from_bytes(data=mock, mime_type="image/jpeg")],
                    config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                        image_config=types.ImageConfig(aspect_ratio="1:1", image_size="2K")))
                d = extract(r)
                if d:
                    img = Image.open(io.BytesIO(d)).convert("RGB"); break
            except Exception as e:
                msg = str(e)
                if any(k in msg for k in ("502","503","UNAVAILABLE","429","RESOURCE_EXHAUSTED")):
                    time.sleep(6*(attempt+1)); continue
                print("  err:", msg[:110], flush=True)
        if img is None:
            print("FAIL", tag, flush=True); continue
        img.save(raw)
    w, h = cut(raw, os.path.join(OUT, f"desk4-book-{tag}-cut.png"))
    print(f"ok   {tag}  cut {w}x{h}", flush=True)
print("done")
