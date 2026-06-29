"""Can a STRONGER prompt push Flash toward Pro quality? Re-run gemini-2.5-flash-image
on the same source heroes with a much more emphatic line-and-wash prompt that
targets Flash's two failure modes: (1) staying photographic on abstract textures,
(2) leaving text/document layout in. Saves -cmp-flashv2.png (non-destructive).
"""
import os, io, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.5-flash-image"

UNITS = [
    ("english-literature-aqa", "macbeth"),
    ("science-aqa", "biology-paper-1"),
    ("geography-edexcel-b", "uk-geographical-issues"),
    ("history-ocr", "usa-people-state-1919-1948"),
    ("history-ocr", "international-relations-1918-1975"),
]

# v2 — emphatic: hand-drawn ink illustration, NOT a photo; outline every form;
# kill photographic texture; never reproduce text/document layout.
PROMPT = (
    "Turn this photograph into a hand-drawn pen-and-ink illustration finished with a light watercolour wash — "
    "in the style of a vintage book-plate or a botanical / architectural study. "
    "Draw EVERY form, edge and contour with confident black pen-and-ink outlines and fine hatching for the shadows. "
    "Nothing may stay photographic: replace ALL photographic texture, grain and smooth gradients with visible "
    "hand-drawn linework — if you can't see an ink line, redraw it. "
    "Over the ink, lay thin translucent watercolour washes following the original colours, leaving plenty of warm "
    "cream paper showing through in the highlights — restrained colour, not a full repaint. "
    "Keep the EXACT same composition and layout: every element in the same position, same crop, as the photo. "
    "This is a DRAWING, not a photo. Do NOT reproduce any text, printed words, captions, page edges or document "
    "layout from the source — draw only the physical objects and forms, never any letters or numbers."
)

def aspect_of(im):
    ar = im.width / im.height
    return "3:2" if abs(ar - 1.5) < 0.18 else ("16:9" if ar > 1.6 else ("4:3" if ar > 1.2 else "1:1"))

def extract(r):
    for c in (r.candidates or []):
        cont = getattr(c, "content", None)
        for p in (getattr(cont, "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen(hero, aspect):
    for attempt in range(4):
        for cfg in (types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio=aspect)),
                    types.GenerateContentConfig(response_modalities=["IMAGE"])):
            try:
                r = client.models.generate_content(model=MODEL, contents=[PROMPT, hero], config=cfg)
                d = extract(r)
                if d:
                    return Image.open(io.BytesIO(d)).convert("RGB"), None
            except Exception as e:
                msg = str(e)
                if any(k in msg for k in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                    time.sleep(5 * (attempt + 1)); break
                return None, msg[:120]
    return None, "exhausted / empty"

def task(skey, slug):
    base = os.path.join(ASSETS, f"path-bg-u-{skey}-{slug}")
    hero = Image.open(base + "-land-photo.png").convert("RGB")
    img, err = gen(hero, aspect_of(hero))
    if img:
        img.save(base + "-cmp-flashv2.png"); return f"[{slug}] ok"
    return f"[{slug}] FAILED — {err}"

print(f"{len(UNITS)} Flash v2 renders…", flush=True)
with ThreadPoolExecutor(max_workers=3) as ex:
    futs = [ex.submit(task, *u) for u in UNITS]
    for f in as_completed(futs):
        print("  " + f.result(), flush=True)
print("done", flush=True)
