"""Weekly-doodle art generator (Google-doodle style backdrops for the dashboard's
Guided door). Reads design-lab/_weekly_doodles.json — {monday: {art, cap, scene}} —
and generates any entry whose art file doesn't exist yet, using the locked
line-and-wash style plus the backdrop composition rule (blank cream upper-left
where the plan text sits, detail gathering lower-right).

Usage: python scripts/_designlab_weekly_doodle.py [--only YYYY-MM-DD]
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
         "CRITICAL COMPOSITION RULE: all detail and ink density gathers in the LOWER-RIGHT of the image; "
         "the drawing dissolves into completely blank warm cream paper across the UPPER-LEFT THIRD — "
         "that region must be empty paper, as if the illustration was never finished there.")

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
        for cfg in (types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio="3:2")),
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
    cal = json.load(open(CAL, encoding="utf-8"))
    todo = [(k, v) for k, v in sorted(cal.items())
            if (not only or k == only) and not os.path.exists(os.path.join(OUT, v["art"]))]
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
