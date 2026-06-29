"""Fix hero units whose sketch/refined stage failed during the rollout (transient 503s)
and were left as the OLD bespoke backdrop. For each hero unit, re-derive any stage
that is missing or older than the saved hero (-land-photo.png), straight from that
hero, with retries. Also removes the now-unused -land-blueprint.png.
"""
import json, os, io, glob, time
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
state = json.load(open(os.path.join(ROOT, "scratch_rollout_state.json"), encoding="utf-8"))
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

KEEP = ("Keep the SAME composition and layout — every element in the SAME place as the input image. "
        "ABSOLUTELY NO text, words, letters or numbers.")
STAGES = {  # suffix -> prompt
 "land-refined.png": ("Redraw this exact image as a REFINED study, partway to finished: clean confident pen-and-ink "
             "linework tracing the forms with a first thin watercolour wash of the same colours, still mostly warm "
             "uncoloured paper — as if the picture is coming into focus. " + KEEP),
 "land.png": ("Redraw this exact image as a loose PENCIL SKETCH: rough, light, unfinished graphite linework on warm "
             "paper, no colour, a quick first study — as if barely in focus yet. " + KEEP),
}

def extract(r):
    for c in (r.candidates or []):
        for p in (c.content.parts or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def transform(hero, prompt, aspect):
    for attempt in range(4):
        for cfg in (types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio=aspect)),
                    types.GenerateContentConfig(response_modalities=["IMAGE"])):
            try:
                r = client.models.generate_content(model="gemini-3-pro-image-preview", contents=[prompt, hero], config=cfg)
                d = extract(r)
                if d:
                    return Image.open(io.BytesIO(d)).convert("RGB")
            except Exception as e:
                msg = str(e)
                if any(k in msg for k in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                    time.sleep(6 * (attempt + 1)); break
                print("     err", msg[:110], flush=True)
    return None

fixed = ok = 0
for key, st in state.items():
    if st != "ok":
        continue
    skey, slug = key.split("/")
    base = os.path.join(ASSETS, f"path-bg-u-{skey}-{slug}")
    photo = base + "-land-photo.png"
    if not os.path.exists(photo):
        print(f"[{key}] no hero photo, skip", flush=True); continue
    pmt = os.path.getmtime(photo)
    bp = base + "-land-blueprint.png"
    if os.path.exists(bp):
        os.remove(bp)
    hero = None
    for suf, prompt in STAGES.items():
        f = base + "-" + suf
        if os.path.exists(f) and os.path.getmtime(f) >= pmt - 1:
            ok += 1; continue   # already a fresh hero-derived stage
        if hero is None:
            hero = Image.open(photo).convert("RGB")
            ar = hero.width / hero.height
            aspect = "3:2" if abs(ar - 1.5) < 0.18 else ("16:9" if ar > 1.6 else ("4:3" if ar > 1.2 else "1:1"))
        print(f"[{key}] re-deriving {suf}…", flush=True)
        img = transform(hero, prompt, aspect)
        if img:
            img.save(f); fixed += 1; print(f"   ok", flush=True)
        else:
            print(f"   FAILED", flush=True)
print(f"\ndone — re-derived {fixed} stale stages, {ok} already fresh", flush=True)
