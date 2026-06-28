"""From the chosen 'complete' tapestry (_tap-D), derive the aligned REFINED and
SKETCH stages (same composition, lower fidelity) so we can see the 3-stage ladder.
Outputs _tap-D-refined.png and _tap-D-sketch.png next to _tap-D.png.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
SRC = os.path.join(ASSETS, "_tap-D.png")

KEEP = ("Keep the SAME composition — every element in the SAME position and size as the input image. "
        "ABSOLUTELY NO text, words, letters or numbers.")
STAGES = {
 "refined": ("Redraw this exact image as a REFINED line-illustration stage: confident clean single-weight contour "
             "linework in deep sage-ink on warm paper, only the faintest hint of flat colour, mostly uncoloured — "
             "the 'inked but not yet fully coloured' stage just before the finished print. " + KEEP),
 "sketch":  ("Redraw this exact image as a loose hand-drawn PENCIL SKETCH: rough, light, unfinished graphite "
             "linework on warm paper, no colour, the look of a quick first study. " + KEEP),
}

def extract(r):
    for c in (r.candidates or []):
        for p in (c.content.parts or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

src = Image.open(SRC)
cfg = types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio="21:9"))
for stage, prompt in STAGES.items():
    try:
        r = client.models.generate_content(model="gemini-3-pro-image-preview", contents=[prompt, src], config=cfg)
        data = extract(r)
        if data:
            out = os.path.join(ASSETS, f"_tap-D-{stage}.png")
            open(out, "wb").write(data); print(f"{stage}: saved", flush=True)
        else:
            print(f"{stage}: no image", flush=True)
    except Exception as e:
        print(f"{stage}: err {str(e)[:140]}", flush=True)
