"""PROTOTYPE: regenerate the 'refined' ink-and-wash stage so the watercolour wash
is anchored to the SUBJECT'S accent colour (thematic primary), instead of the
photo's own colours. Writes to -land-refined-accent.png (does NOT touch the live
-land-refined.png) so we can compare old vs accent side by side. Source = the
saved real hero (-land-photo.png).

Usage:
  python scripts/_designlab_accent_refined_proto.py                      # the 2 demo units
  python scripts/_designlab_accent_refined_proto.py religious-studies-aqa  # every unit of a subject
  python scripts/_designlab_accent_refined_proto.py <skey> <skey> ...      # several subjects
Accent + name are read from design-lab/_path_backdrops.json.
"""
import os, io, json, sys, time, colorsys
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
MANIFEST = os.path.join(ROOT, "design-lab", "_path_backdrops.json")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
manifest = json.load(open(MANIFEST, encoding="utf-8"))

KEEP = ("Keep the SAME composition and layout — every element in the SAME place as the input image. "
        "ABSOLUTELY NO text, words, letters or numbers.")

def colour_name(hexv):
    """Rough human descriptor from a hex accent — anchors the prompt alongside the hex."""
    h = hexv.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    hue, light, sat = colorsys.rgb_to_hls(r, g, b)
    deg = hue * 360
    if sat < 0.16:
        return ("deep grey" if light < 0.4 else "soft warm grey" if light < 0.7 else "pale grey")
    fam = ("red" if deg < 15 or deg >= 345 else "amber-brown" if deg < 45 else "gold" if deg < 65
           else "green" if deg < 160 else "teal" if deg < 200 else "blue" if deg < 255
           else "indigo" if deg < 280 else "purple" if deg < 320 else "magenta")
    qual = "deep" if light < 0.4 else "muted" if sat < 0.55 else "rich"
    return f"{qual} {fam}"

def jobs_from_subject(skey):
    out = []
    for key, e in manifest.items():
        if not key.startswith(skey + "/"):
            continue
        slug = key.split("/", 1)[1]
        if not os.path.exists(os.path.join(ASSETS, f"path-bg-u-{skey}-{slug}-land-photo.png")):
            continue
        acc = e.get("accent") or "#888888"
        out.append((skey, slug, acc, colour_name(acc)))
    return out

DEMO = [
    ("english-literature-aqa", "macbeth", "#7d3737", "deep brick-red / burgundy"),
    ("science-aqa", "biology-paper-1", "#368352", "muted emerald green"),
]

def prompt_for(name, hexv):
    return ("Redraw this exact image as a REFINED study, partway to finished: clean confident pen-and-ink "
            "linework tracing the forms with a thin watercolour wash, still mostly warm uncoloured paper, as "
            "if the picture is coming into focus. Make the DOMINANT colour of the wash a " + name +
            " (around hex " + hexv + ") — use this one colour thematically across the whole image so it reads "
            "as a single tonal family, tasteful and not oversaturated, with the paper showing through. " + KEEP)

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
                print("     err", msg[:120], flush=True)
    return None

args = sys.argv[1:]
JOBS = DEMO if not args else [j for sk in args for j in jobs_from_subject(sk)]
print(f"{len(JOBS)} unit(s) to render", flush=True)
made = 0
for skey, slug, hexv, name in JOBS:
    base = os.path.join(ASSETS, f"path-bg-u-{skey}-{slug}")
    photo = base + "-land-photo.png"
    if not os.path.exists(photo):
        print(f"[{skey}/{slug}] no hero photo, skip", flush=True); continue
    hero = Image.open(photo).convert("RGB")
    ar = hero.width / hero.height
    aspect = "3:2" if abs(ar - 1.5) < 0.18 else ("16:9" if ar > 1.6 else ("4:3" if ar > 1.2 else "1:1"))
    print(f"[{skey}/{slug}] accent {hexv} ({name}) …", flush=True)
    img = transform(hero, prompt_for(name, hexv), aspect)
    if img:
        img.save(base + "-land-refined-accent.png"); made += 1
        print("   ok", flush=True)
    else:
        print("   FAILED", flush=True)
print(f"done — {made}/{len(JOBS)} rendered", flush=True)
