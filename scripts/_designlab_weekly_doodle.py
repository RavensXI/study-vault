"""Weekly-doodle art generator for the desk calendar's art strip (the wide
banner above the month grid on dash-desk4). Reads design-lab/_weekly_doodles.json
— {monday: {art, cap, scene}} — and generates any entry whose art file doesn't
exist yet, in the locked line-and-wash style. Composition is a full-width
panoramic vignette (the strip cover-crops a horizontal band, so interest must
span the whole width — the old blank-corner rule was for the retired Guided
door backdrop and left the strip half empty).

Usage: python scripts/_designlab_weekly_doodle.py [--only YYYY-MM-DD]
                                                  [--force] [--from YYYY-MM-DD]
--force regenerates even when the art file already exists (use with --from/--only).
"""
import os, io, sys, json, time
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw")
CAL = os.path.join(ROOT, "design-lab", "_weekly_doodles.json")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
IMG_MODEL = "gemini-3-pro-image-preview"

STYLE = (" — drawn as a refined pen-and-ink illustration finished with a thin watercolour wash: "
         "confident black ink linework and fine hatching, thin translucent watercolour in muted colours "
         "laid over it, plenty of warm cream paper showing through, in the style of a vintage book-plate. "
         "Calm, atmospheric, editorial. No people, no recognisable faces. "
         "ABSOLUTELY NO text, words, letters or numbers. "
         "CRITICAL COMPOSITION RULE: a wide panoramic vignette — the scene stretches across the "
         "FULL width of the frame, with its interest and ink detail spread along the horizontal "
         "middle band (the frame is later cropped to a wide strip, so nothing important near the "
         "very top or bottom edge). The drawing must reach both the left and right sides; edges may "
         "soften gently into the cream paper, but NO large empty regions of blank paper.")

def extract(r):
    for c in (r.candidates or []):
        cont = getattr(c, "content", None)
        for p in (getattr(cont, "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def render(prompt):
    for attempt in range(4):
        for cfg in (types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio="16:9")),
                    types.GenerateContentConfig(response_modalities=["IMAGE"])):
            try:
                r = client.models.generate_content(model=IMG_MODEL, contents=[prompt], config=cfg)
                d = extract(r)
                if d:
                    return Image.open(io.BytesIO(d)).convert("RGB"), None
            except Exception as e:
                msg = str(e)
                if any(k in msg for k in ("502", "503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                    time.sleep(5 * (attempt + 1)); break
                return None, msg[:90]
    return None, "refused/empty"

def main():
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    since = sys.argv[sys.argv.index("--from") + 1] if "--from" in sys.argv else None
    force = "--force" in sys.argv
    cal = json.load(open(CAL, encoding="utf-8"))
    todo = [(k, v) for k, v in sorted(cal.items())
            if (not only or k == only) and (not since or k >= since)
            and (force or not os.path.exists(os.path.join(OUT, v["art"])))]
    print(f"{len(todo)} doodles to generate ({len(cal)} in calendar)", flush=True)
    fails = 0
    for k, v in todo:
        img, err = render(v["scene"] + STYLE)
        if img:
            img.save(os.path.join(OUT, v["art"]))
            print(f"ok    {k}  {v['art']}  ({v['cap']})", flush=True)
        else:
            fails += 1
            print(f"FAIL  {k}  {v['art']}: {err}", flush=True)
    print(f"done: {len(todo) - fails} generated, {fails} failed", flush=True)

if __name__ == "__main__":
    main()
