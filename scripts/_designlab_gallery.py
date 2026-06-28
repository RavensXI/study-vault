"""Style-exploration gallery: the SAME Biology Paper 1 content rendered in 8 very
different art directions, stacked into one labelled image so Tom can point at the
one that's closest. Output: design-lab/assets/_gallery.png
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

BIO = ("GCSE Biology: cells and a microscope, the human body's organs (heart, lungs, digestive system), "
       "microbes and white blood cells, DNA, plants and an ecosystem")
NO = "Warm off-white paper, gentle sage-green palette. NO text, letters, numbers or labels."

DIRECTIONS = [
 ("1. Flat scene / cross-section world",
  f"ONE cohesive illustrated SCENE — a cross-section of a living world read left to right: a tree and sky, a plant "
  f"with roots in the soil, a human figure with organs shown in place, and a round magnified inset of cells and "
  f"microbes — all belonging to one believable scene. Flat modern illustration. {BIO}. No floating disconnected "
  f"icons, no tubes joining unrelated objects. {NO}"),
 ("2. Painterly gouache scene",
  f"ONE soft PAINTERLY GOUACHE illustrated scene of {BIO}, textured brushwork, the subjects nestled together in one "
  f"warm composed picture, not separate icons, not joined by tubes. {NO}"),
 ("3. Mid-century textbook",
  f"A charming VINTAGE 1950s-60s science textbook illustration of {BIO}: flat muted retro colours, simplified "
  f"friendly shapes, composed together as one tasteful plate. {NO}"),
 ("4. Risograph print",
  f"A RISOGRAPH print of {BIO}: grainy, two or three overlapping spot colours (sage green and warm ochre), slightly "
  f"mis-registered, arty and cohesive poster. {NO}"),
 ("5. Antique ink naturalist plate",
  f"A single antique PEN-AND-INK naturalist plate of {BIO}: fine cross-hatching, the specimens composed together "
  f"harmoniously on one engraved sheet. {NO}"),
 ("6. Continuous fine line",
  f"A CONTINUOUS single-weight FINE LINE drawing of {BIO} in one deep-sage colour on warm paper — each subject "
  f"distinct but drawn in one calm continuous hand, minimal and elegant. {NO}"),
 ("7. Cut-paper collage",
  f"A CUT-PAPER COLLAGE illustration of {BIO}: torn and layered coloured-paper shapes with soft drop shadows, "
  f"Matisse-like, warm muted palette, one cohesive composition. {NO}"),
 ("8. Isometric mini-world",
  f"A small ISOMETRIC illustrated diorama of {BIO} — a tidy 3/4-view mini-world with a body, plants, a microscope "
  f"and cells, soft sage/cream palette, one cohesive little scene. {NO}"),
]

def extract(r):
    for c in (r.candidates or []):
        for p in (c.content.parts or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

cfg = types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio="21:9"))
imgs = []
for label, prompt in DIRECTIONS:
    try:
        r = client.models.generate_content(model="gemini-3-pro-image-preview", contents=[prompt], config=cfg)
        data = extract(r)
        if data:
            p = os.path.join(ASSETS, f"_gal-{label.split('.')[0]}.png")
            open(p, "wb").write(data)
            imgs.append((label, Image.open(p).convert("RGB")))
            print(f"ok {label}", flush=True)
        else:
            print(f"no image {label}", flush=True)
    except Exception as e:
        print(f"err {label}: {str(e)[:120]}", flush=True)

# composite: vertical stack, each banner scaled to width W, label strip above
W, LBL = 1120, 30
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 20)
rows = []
for label, im in imgs:
    h = round(im.height * W / im.width)
    rows.append((label, im.resize((W, h))))
total_h = sum(LBL + r[1].height + 14 for r in rows) + 14
canvas = Image.new("RGB", (W + 24, total_h), (247, 246, 244))
d = ImageDraw.Draw(canvas)
y = 14
for label, im in rows:
    d.text((12, y + 4), label, fill=(40, 40, 38), font=font)
    canvas.paste(im, (12, y + LBL))
    y += LBL + im.height + 14
out = os.path.join(ASSETS, "_gallery.png")
canvas.save(out)
print("gallery saved", canvas.size, flush=True)
