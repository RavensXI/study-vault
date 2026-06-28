"""Experiment: find the best 'long thin non-repeating banner' approach on ONE unit
(Combined Science · Biology Paper 1) before scaling to all.

Generates several candidates into design-lab/assets/_exp-*.png so we can compare:
  A) 21:9 panorama, img2img from the photo  (widest native single image)
  B) 21:9 panorama, sparser/continuous prompt (calmer, blends better when tiled)
  C) outpaint EXTEND: take A and grow it rightwards into a 2-segment long strip
     (true non-repeating length) — saved as the stitched _exp-extend.png

Run: python scripts/_designlab_land_experiment.py
Env: DL_GEMINI_MODEL (default gemini-3-pro-image-preview)
"""
import os, sys, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _designlab_unit_backdrops import ACCENT
from _designlab_aligned_ladder import motifs_for
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
MODEL = os.environ.get("DL_GEMINI_MODEL", "gemini-3-pro-image-preview")
SKEY, SLUG = "science-aqa", "biology-paper-1"
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def extract(resp):
    for cand in (resp.candidates or []):
        for part in (cand.content.parts or []):
            d = getattr(part, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen(contents, aspect, out):
    cfgs = [types.GenerateContentConfig(response_modalities=["IMAGE"],
                                        image_config=types.ImageConfig(aspect_ratio=aspect)),
            types.GenerateContentConfig(response_modalities=["IMAGE"])]
    for cfg in cfgs:
        try:
            resp = client.models.generate_content(model=MODEL, contents=contents, config=cfg)
            data = extract(resp)
            if data:
                open(out, "wb").write(data)
                im = Image.open(out)
                print(f"  saved {os.path.basename(out)} {im.size} ({os.path.getsize(out)//1024} KB)", flush=True)
                return out
        except Exception as e:
            print(f"  {aspect} err: {str(e)[:140]}", flush=True)
    return None

hexc, word = ACCENT[SKEY]
motifs = motifs_for(SKEY, SLUG)
photo = os.path.join(ASSETS, f"path-bg-u-{SKEY}-{SLUG}-photo.png")
src = Image.open(photo)

panorama = (
    f"Recompose as a WIDE ULTRA-PANORAMIC horizontal banner, a single continuous illustrated scene "
    f"reading left to right. Use the SAME subjects/motifs spread EVENLY along the full length: {motifs}; "
    f"render each as exactly what it is, do not reinterpret. Arrange motifs along the upper and lower edges; "
    f"keep a calm, open horizontal band through the vertical centre for a winding trail to run left-to-right. "
    f"Full colour, soft natural light, warm off-white paper, gentle {word} ({hexc}) tones. The far-left and "
    f"far-right edges should be calm and open. ABSOLUTELY NO text, words, letters or numbers."
)
sparse = (
    f"Wide ultra-panoramic horizontal banner, a calm continuous illustrated landscape reading left to right. "
    f"Feature these motifs as a FEW well-spaced focal points with generous open space between them: {motifs}; "
    f"render each exactly as what it is. Lots of quiet warm off-white paper, a gentle winding trail along the "
    f"horizontal centre, soft {word} ({hexc}) tones, airy and uncluttered. No text, no labels."
)

print("A) 21:9 panorama from photo")
A = gen([panorama, src], "21:9", os.path.join(ASSETS, "_exp-bio-p1-A-21x9.png"))
print("B) 21:9 sparse/continuous")
B = gen([sparse, src], "21:9", os.path.join(ASSETS, "_exp-bio-p1-B-sparse.png"))

# C) outpaint-extend A rightward into a longer strip, then stitch the two halves
if A:
    a_img = Image.open(A).convert("RGB")
    extend = (
        f"This is the LEFT portion of a wide illustrated banner. Continue the scene seamlessly to the RIGHT: "
        f"keep the same warm paper, the same {word} ({hexc}) palette and the same horizontal centre trail flowing "
        f"on, and add MORE different related motifs from this set along the top and bottom edges: {motifs}. "
        f"The left edge of your image must continue smoothly from this picture. No text."
    )
    print("C) extend A rightward")
    C = gen([extend, a_img], "21:9", os.path.join(ASSETS, "_exp-bio-p1-C-right.png"))
    if C:
        right = Image.open(C).convert("RGB")
        h = min(a_img.height, right.height)
        a2 = a_img.resize((round(a_img.width*h/a_img.height), h))
        r2 = right.resize((round(right.width*h/right.height), h))
        strip = Image.new("RGB", (a2.width + r2.width, h), "#f6f2ea")
        strip.paste(a2, (0, 0)); strip.paste(r2, (a2.width, 0))
        out = os.path.join(ASSETS, "_exp-bio-p1-extend.png")
        strip.save(out)
        print(f"  stitched {os.path.basename(out)} {strip.size} ({os.path.getsize(out)//1024} KB)", flush=True)
print("done")
