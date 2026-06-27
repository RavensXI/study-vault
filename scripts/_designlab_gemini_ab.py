"""A/B: run our backdrop pipeline through Google Gemini (Nano Banana Pro) instead
of OpenAI, on the same unit (Biology Paper 1), so we can compare quality —
especially the img2img ladder (does Gemini hold the composition?).
Writes design-lab/assets/_gem-sketch.png and _gem-photo.png
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _designlab_unit_backdrops import MOTIFS, ACCENT, sketch_prompt
from _designlab_aligned_ladder import prompts as ladder_prompts
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
# argv: [model] [suffix]   e.g.  gemini-2.5-flash-image flash
MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemini-3-pro-image-preview"   # Nano Banana Pro
SUFFIX = sys.argv[2] if len(sys.argv) > 2 else "gem"
SUBJECT, UNIT = "science-aqa", "biology-paper-1"
hexc, word = ACCENT[SUBJECT]
motifs = MOTIFS[f"{SUBJECT}/{UNIT}"]

def extract_image(resp):
    for cand in (resp.candidates or []):
        for part in (cand.content.parts or []):
            d = getattr(part, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen(client, contents, label, out):
    cfg_variants = [
        types.GenerateContentConfig(response_modalities=["IMAGE"],
                                    image_config=types.ImageConfig(aspect_ratio="2:3")),
        types.GenerateContentConfig(response_modalities=["IMAGE"]),
        None,
    ]
    for cfg in cfg_variants:
        try:
            print(f"[{label}] generating…", flush=True)
            kw = {"model": MODEL, "contents": contents}
            if cfg is not None:
                kw["config"] = cfg
            resp = client.models.generate_content(**kw)
            img = extract_image(resp)
            if not img:
                print(f"[{label}] no image part (text: {getattr(resp,'text','')[:120]})", flush=True)
                continue
            with open(out, "wb") as f:
                f.write(img)
            print(f"[{label}] saved ({os.path.getsize(out)//1024} KB)", flush=True)
            return out
        except Exception as e:
            print(f"[{label}] cfg failed: {str(e)[:160]}", flush=True)
    return None

def main():
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    print(f"=== model: {MODEL} (suffix _{SUFFIX}) ===", flush=True)
    sp = sketch_prompt(motifs, word, hexc) + " Vertical portrait, 2:3 aspect ratio."
    sketch_out = os.path.join(ASSETS, f"_{SUFFIX}-sketch.png")
    gen(client, sp, "sketch", sketch_out)
    if os.path.exists(sketch_out):
        pp = ladder_prompts(motifs, word, hexc)["photo"]
        src = Image.open(sketch_out)
        gen(client, [pp, src], "photo (img2img)", os.path.join(ASSETS, f"_{SUFFIX}-photo.png"))
    print("done")

if __name__ == "__main__":
    main()
