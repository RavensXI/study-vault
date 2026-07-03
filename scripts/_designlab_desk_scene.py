"""Empty-desk background plate for dash-desk3, img2img from Tom's approved
Gemini mock. Removes the INTERACTIVE objects (notebook, phone, radio, postcard,
stickies, flashcards) so they can live as HTML overlays that pop; keeps the
desk wood, stains, splatters and loose stationery as painted background.
Writes design-lab/assets/lw/desk-scene-{a,b}.png (two candidates).
"""
import os, io, time
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw")
SRC = r"C:\Users\tshau\Downloads\Gemini_Generated_Image_iaw6cbiaw6cbiaw6.jpg"

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
IMG_MODEL = "gemini-3-pro-image-preview"

PROMPT = (
    "Recreate this exact desk scene in the same hand-drawn pen-and-ink with soft watercolour "
    "wash style, keeping the identical camera angle, the identical pale scrubbed-wood desk with "
    "its grain lines, the identical soft lighting from the upper left, and the same ink splatters, "
    "coffee stains and watermarks on the wood. "
    "REMOVE COMPLETELY: the open notebook, the mobile phone, the radio, the postcard, all sticky "
    "notes, all flashcards / index cards, and any labels or UI chrome. Where those objects were, "
    "show plain open desk wood with only subtle stains — leave those areas generously empty. "
    "KEEP, exactly where they are: the white mug holding pencils and pens, the long wooden pencil, "
    "the short yellow pencil stub, the black fountain pen, the pink eraser, and every stain and "
    "splatter on the wood. Add nothing new. "
    "ABSOLUTELY NO text, letters, numbers or logos anywhere."
)

def extract(r):
    for c in (r.candidates or []):
        for p in (getattr(getattr(c, "content", None), "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

src_bytes = open(SRC, "rb").read()
for tag in ("a", "b"):
    out = os.path.join(OUT, f"desk-scene-{tag}.png")
    if os.path.exists(out):
        print("skip", tag); continue
    img = None
    for attempt in range(4):
        try:
            r = client.models.generate_content(model=IMG_MODEL,
                contents=[PROMPT, types.Part.from_bytes(data=src_bytes, mime_type="image/jpeg")],
                config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="16:9")))
            d = extract(r)
            if d:
                img = Image.open(io.BytesIO(d)).convert("RGB"); break
        except Exception as e:
            msg = str(e)
            if any(k in msg for k in ("502", "503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                time.sleep(6 * (attempt + 1)); continue
            print("  err:", msg[:100], flush=True)
    if img is None:
        print("FAIL", tag, flush=True); continue
    img.save(out)
    print("ok  ", tag, img.size, flush=True)
print("done")
