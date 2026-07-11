"""Round 2 of the landing atmosphere kit (Tom's notes, 11 Jul evening):
  - brass_plaque: blank engraved-style brass wall plaque (exam board names get
    overlaid as live text with an engraved CSS treatment — never baked in)
  - door_frame: slim walnut picture frame with brass lip holding aged cream
    paper, empty — used as border-image so the two door panels become objects
    OF the painted scene.

Run: python scripts/_designlab_shelf_atmosphere2.py [keys...]
"""
import io, os, sys, time
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw", "shelf")
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
         "in frame. Drawn STRAIGHT-ON, no perspective, no cast shadow. ")

ITEMS = {
    "brass_plaque": (
        STYLE + "A wide rectangular polished brass wall plaque with a softly bevelled edge and "
        "a small round screw head in each of the four corners. The plaque face is completely "
        "BLANK and smooth — absolutely no text, no lettering, no engraving marks, no decoration "
        "— just warm aged brass with a gentle horizontal sheen, slightly darker toward the "
        "bevelled edges. The plaque is much wider than tall and fills the frame.", "21:9"),
    "door_frame": (
        STYLE + "A slim rectangular picture frame of dark walnut wood with a very thin polished "
        "brass inner lip, holding a completely plain panel of aged warm cream paper. The frame "
        "borders are narrow and even on all four sides; the cream paper panel is completely "
        "empty — no picture, no text, no marks. The frame fills the frame of the image.", "4:5"),
}

def extract(r):
    for c in (r.candidates or []):
        for p in (getattr(getattr(c, "content", None), "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen(contents, aspect):
    for attempt in range(5):
        try:
            r = client.models.generate_content(
                model=MODEL, contents=contents,
                config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio=aspect)))
            d = extract(r)
            if d: return Image.open(io.BytesIO(d)).convert("RGB")
        except Exception as e:
            if any(k in str(e) for k in ("503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED")):
                time.sleep(6 * (attempt + 1)); continue
            raise
    raise RuntimeError("gen failed")

only = sys.argv[1:]
for key, (prompt, aspect) in ITEMS.items():
    p = os.path.join(OUT, f"{key}.png")
    if only and key not in only: continue
    if os.path.exists(p) and not only:
        print("have", key); continue
    im = gen([prompt, LAMP], aspect)
    if im.width > 1600:
        im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
    im.save(p)
    im.save(os.path.join(OUT, f"{key}.webp"), quality=84, method=6)
    print("made", key, flush=True)
print("done")
