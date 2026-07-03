"""Progress-staged subject emblems for the desk notebook: each subject gets a
3-stage ALIGNED ladder of the same composition —
  s1 faint pencil construction sketch -> s2 ink linework -> s3 full line-and-wash.
Alignment: generate s3 (text->image), then img2img DOWN (s3 -> s2 -> s1) so the
composition is identical and the picture visibly 'finishes' as the student does.
Writes design-lab/_subject_ladders.json incrementally: {slug: [s1,s2,s3]}.
"""
import os, io, json, time
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "assets", "lw", "ladders")
MANIFEST = os.path.join(ROOT, "design-lab", "_subject_ladders.json")
os.makedirs(OUT, exist_ok=True)
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
IMG_MODEL = "gemini-3-pro-image-preview"

WASH = (" — drawn as a refined pen-and-ink illustration finished with thin watercolour washes in muted "
        "colours, plenty of warm cream paper showing through, vintage book-plate style. Calm, editorial. "
        "No people, no faces. ABSOLUTELY NO text, letters or numbers.")

EMBLEMS = {
 "maths":      "A drafting compass standing open on paper beside a wooden ruler and protractor, a large hand-drawn logarithmic spiral curving beneath them",
 "lang":       "A vintage typewriter with blank round keys, a curling sheet of blank paper rising from the platen, a small stack of envelopes beside it",
 "lit":        "A candlelit stack of clothbound novels with ribbon bookmarks, wax pooled at the candle's base, a pair of reading glasses resting on top",
 "science":    "A brass microscope beside a wooden rack of test tubes and a scatter of glass slides, one slide catching the light",
 "history":    "A ruined hilltop castle keep seen across a valley, a winding path climbing toward it through hedgerows",
 "geog":       "A river valley seen from above, the river meandering in wide loops past small fields toward a distant coast",
 "spanish":    "A horseshoe archway with intricate geometric tilework opening onto a sunlit courtyard with a small fountain",
 "cs":         "A retro computer terminal with a blank dark screen on a desk beside a reel-to-reel tape unit and a punched card",
 "rs":         "A tall arched stained-glass window with abstract geometric panes, light falling through onto a stone floor",
}

DOWN_INK = ("Redraw this exact image, keeping the composition identical, as UNFINISHED pen-and-ink linework: "
            "confident black ink outlines and hatching only, NO watercolour wash, no colour at all, plain warm "
            "cream paper background. The same picture, before the paint. No text.")
DOWN_PENCIL = ("Redraw this exact image, keeping the composition identical, as a FAINT UNFINISHED pencil "
               "construction sketch: light graphite guidelines, rough gesture lines, some construction geometry "
               "still visible, large areas of the paper still empty, as if the artist has only just begun. "
               "No ink, no colour. No text.")

def extract(r):
    for c in (r.candidates or []):
        for p in (getattr(getattr(c, "content", None), "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen(contents):
    for attempt in range(4):
        try:
            r = client.models.generate_content(model=IMG_MODEL, contents=contents,
                config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="3:2")))
            d = extract(r)
            if d:
                return Image.open(io.BytesIO(d)).convert("RGB")
        except Exception as e:
            msg = str(e)
            if any(k in msg for k in ("502", "503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                time.sleep(6 * (attempt + 1)); continue
            print("  err:", msg[:80], flush=True)
    return None

manifest = json.load(open(MANIFEST, encoding="utf-8")) if os.path.exists(MANIFEST) else {}
for slug, scene in EMBLEMS.items():
    if slug in manifest:
        print("skip", slug, flush=True); continue
    paths = [os.path.join(OUT, f"{slug}-s{i}.png") for i in (1, 2, 3)]
    s3 = gen([scene + WASH])
    if not s3: print("FAIL s3", slug, flush=True); continue
    s3.save(paths[2])
    s2 = gen([DOWN_INK, types.Part.from_bytes(data=open(paths[2],'rb').read(), mime_type="image/png")])
    if not s2: print("FAIL s2", slug, flush=True); continue
    s2.save(paths[1])
    s1 = gen([DOWN_PENCIL, types.Part.from_bytes(data=open(paths[1],'rb').read(), mime_type="image/png")])
    if not s1: print("FAIL s1", slug, flush=True); continue
    s1.save(paths[0])
    manifest[slug] = [f"assets/lw/ladders/{slug}-s{i}.png" for i in (1, 2, 3)]
    json.dump(manifest, open(MANIFEST, "w", encoding="utf-8"), indent=1)
    print("ok  ", slug, flush=True)
print(f"done: {len(manifest)}/9 ladders", flush=True)
