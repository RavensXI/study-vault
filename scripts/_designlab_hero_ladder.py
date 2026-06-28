"""Ladder a unit's REAL hero image into the mastery stages: sketch + refined, aligned
to the hero (so the hero just 'comes into focus'). Saves into the lane's stage slots:
  hero      -> path-bg-u-<skey>-<slug>-land-photo.png   (complete)
  refined   -> ...-land-refined.png
  sketch    -> ...-land.png   (base)
Usage: python scripts/_designlab_hero_ladder.py <skey> <slug> <hero.jpg>
"""
import os, sys
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

SKEY, SLUG, HERO = sys.argv[1], sys.argv[2], sys.argv[3]
hero = Image.open(HERO).convert("RGB")
ar = hero.width / hero.height
ASPECT = "3:2" if abs(ar - 1.5) < 0.2 else ("16:9" if ar > 1.6 else "4:3")

KEEP = ("Keep the SAME composition and layout — every shape in the SAME place as the input image. "
        "ABSOLUTELY NO text, words, letters or numbers.")
STAGES = {
 "refined": ("Redraw this exact image as a REFINED study, partway to finished: clean confident pen-and-ink linework "
             "tracing the forms with a first thin watercolour wash of the same colours, still mostly warm uncoloured "
             "paper — as if the picture is coming into focus. " + KEEP),
 "sketch":  ("Redraw this exact image as a loose PENCIL SKETCH: rough, light, unfinished graphite linework on warm "
             "paper, no colour, a quick first study — as if barely in focus yet. " + KEEP),
}

def extract(r):
    for c in (r.candidates or []):
        for p in (c.content.parts or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def out_for(stage):
    suf = "land.png" if stage == "sketch" else f"land-{stage}.png"
    return os.path.join(ASSETS, f"path-bg-u-{SKEY}-{SLUG}-{suf}")

# complete = the hero itself
hero.save(out_for("photo")); print("complete = hero saved", flush=True)
for stage, prompt in STAGES.items():
    done = False
    for cfg in (types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio=ASPECT)),
                types.GenerateContentConfig(response_modalities=["IMAGE"])):
        try:
            r = client.models.generate_content(model="gemini-3-pro-image-preview", contents=[prompt, hero], config=cfg)
            d = extract(r)
            if d:
                open(out_for(stage), "wb").write(d); print(f"{stage} saved", flush=True); done = True; break
        except Exception as e:
            print(f"{stage} err {str(e)[:120]}", flush=True)
    if not done:
        print(f"{stage} FAILED", flush=True)
print("done")
