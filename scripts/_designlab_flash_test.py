"""QUALITY TEST: line-and-wash refined, Flash vs Pro, on the same source heroes.
Generates -cmp-flash.png (gemini-2.5-flash-image) and -cmp-pro.png
(gemini-3-pro-image-preview) for a diverse set, from each unit's saved hero
(-land-photo.png). Non-destructive (own suffixes). Threaded with 503/429 retry.
"""
import os, io, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

UNITS = [
    ("english-literature-aqa", "macbeth"),                 # atmospheric scene
    ("science-aqa", "biology-paper-1"),                    # abstract micrograph
    ("geography-edexcel-b", "uk-geographical-issues"),     # landscape
    ("history-ocr", "usa-people-state-1919-1948"),         # documentary / figures
    ("english-literature-aqa", "an-inspector-calls"),      # single-person portrait (hard)
    ("history-ocr", "international-relations-1918-1975"),   # group photo / crowd (hard)
]
MODELS = [("gemini-2.5-flash-image", "flash"), ("gemini-3-pro-image-preview", "pro")]

KEEP = ("Keep the SAME composition and layout — every element in the SAME place as the input image. "
        "ABSOLUTELY NO text, words, letters or numbers.")
PROMPT = ("Redraw this exact image as a REFINED study, partway to finished: clean confident pen-and-ink "
          "linework tracing the forms with a first thin watercolour wash of the same colours, still mostly warm "
          "uncoloured paper — as if the picture is coming into focus. " + KEEP)

def aspect_of(im):
    ar = im.width / im.height
    return "3:2" if abs(ar - 1.5) < 0.18 else ("16:9" if ar > 1.6 else ("4:3" if ar > 1.2 else "1:1"))

def extract(r):
    for c in (r.candidates or []):
        for p in (c.content.parts or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen(model, hero, aspect):
    for attempt in range(4):
        for cfg in (types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio=aspect)),
                    types.GenerateContentConfig(response_modalities=["IMAGE"])):
            try:
                r = client.models.generate_content(model=model, contents=[PROMPT, hero], config=cfg)
                d = extract(r)
                if d:
                    return Image.open(io.BytesIO(d)).convert("RGB"), None
            except Exception as e:
                msg = str(e)
                if any(k in msg for k in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                    time.sleep(5 * (attempt + 1)); break
                return None, msg[:120]
    return None, "exhausted retries / empty"

def task(skey, slug, model, suffix):
    base = os.path.join(ASSETS, f"path-bg-u-{skey}-{slug}")
    photo = base + "-land-photo.png"
    if not os.path.exists(photo):
        return f"[{slug}/{suffix}] no source"
    hero = Image.open(photo).convert("RGB")
    img, err = gen(model, hero, aspect_of(hero))
    if img:
        img.save(base + f"-cmp-{suffix}.png")
        return f"[{slug}/{suffix}] ok"
    return f"[{slug}/{suffix}] FAILED — {err}"

jobs = [(s, u, m, sfx) for (s, u) in UNITS for (m, sfx) in MODELS]
print(f"{len(jobs)} renders ({len(UNITS)} units x {len(MODELS)} models)…", flush=True)
with ThreadPoolExecutor(max_workers=4) as ex:
    futs = [ex.submit(task, *j) for j in jobs]
    for f in as_completed(futs):
        print("  " + f.result(), flush=True)
print("done", flush=True)
