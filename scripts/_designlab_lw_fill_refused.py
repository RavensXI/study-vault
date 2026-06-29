"""Fill the BLANKS from the line-and-wash pilot: for every lesson whose hero was
refused by Pro (recognisable person / sensitive content) or has no remote source,
auto-generate an ORIGINAL line-and-wash hero FROM SCRATCH (text-to-image, so no
real photo to refuse):
  1. a Gemini text model writes a person-free, tasteful, topical scene from the
     lesson title;
  2. Gemini Pro renders that scene in the line-and-wash style.
Keyed by the lesson's stored hero URL so skin-switcher swaps it in just like the
img2img ones. Updates _lw_manifest.json, records _lw_generated.json, and rebuilds
_lw_pilot_index.json with a per-lesson source (photo / generated).
"""
import os, io, json, time, hashlib
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LW = os.path.join(ROOT, "design-lab", "assets", "lw")
DATA = json.load(open(os.path.join(ROOT, "scratch_history_pilot.json"), encoding="utf-8"))
MANI_PATH = os.path.join(ROOT, "design-lab", "_lw_manifest.json")
manifest = json.load(open(MANI_PATH, encoding="utf-8"))
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
TEXT_MODEL = "gemini-2.5-flash"
IMG_MODEL = "gemini-3-pro-image-preview"

NAMES = {
    "international-relations-1918-1975": "International Relations 1918-1975",
    "germany-people-state-1925-1955": "Germany 1925-1955: The People and the State",
    "migration-to-britain-1000-2010": "Migration to Britain c.1000-c.2010",
    "usa-people-state-1919-1948": "The USA 1919-1948: The People and the State",
}

def norm(u): return (u or "").split("?")[0].strip()
def key(u): return hashlib.sha1(norm(u).encode("utf-8")).hexdigest()[:12]

SCENE_SYS = (
    "You are choosing cover art for a GCSE History lesson.\n"
    "Lesson title: \"{title}\"\nUnit: {unit} (GCSE History).\n"
    "Describe in ONE vivid sentence a single representative SCENE, PLACE, BUILDING, OBJECT or SYMBOLIC "
    "STILL-LIFE that captures this lesson's topic for an illustrated hero image.\n"
    "Strict rules:\n"
    "- NO recognisable real people, named individuals, portraits, faces, or crowds with visible faces. "
    "Use places, architecture, landscapes, objects, documents, silhouettes, or views from behind/above.\n"
    "- Tasteful and age-appropriate. Do NOT depict violence, hateful symbols, swastikas, Klan robes or racist "
    "imagery — evoke difficult topics respectfully and INDIRECTLY (e.g. an empty segregated waiting room, "
    "a shuttered storefront at dusk, a quiet memorial).\n"
    "- Concrete, clearly depictable and period-accurate. No text or signage that must be readable.\n"
    "Reply with ONLY the scene description sentence."
)

def img_prompt(scene):
    return (scene + " — drawn as a refined pen-and-ink illustration finished with a thin watercolour wash: "
            "confident black ink linework and fine hatching, thin translucent watercolour in muted period colours "
            "laid over it, plenty of warm cream paper showing through, in the style of a vintage book-plate. "
            "Calm, atmospheric, editorial. No recognisable faces. ABSOLUTELY NO text, words, letters or numbers.")

def scene_for(title, unit):
    for _ in range(3):
        try:
            r = client.models.generate_content(model=TEXT_MODEL, contents=[SCENE_SYS.format(title=title, unit=unit)])
            t = (getattr(r, "text", "") or "").strip().strip('"')
            if t:
                return t.split("\n")[0]
        except Exception as e:
            time.sleep(4); print("    scene err", str(e)[:80], flush=True)
    return None

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
                if any(k in msg for k in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                    time.sleep(5 * (attempt + 1)); break
                return None, msg[:90]
    return None, "refused/empty"

# find blanks
blanks = []
for unit, rows in DATA.items():
    for r in rows:
        n = norm(r.get("hero_image_url"))
        if n not in manifest:
            blanks.append((unit, r.get("lesson_number"), r.get("title"), n))

print(f"{len(blanks)} blanks to fill from scratch…", flush=True)
generated = json.load(open(os.path.join(ROOT, "design-lab", "_lw_generated.json"), encoding="utf-8")) if os.path.exists(os.path.join(ROOT, "design-lab", "_lw_generated.json")) else []
genset = set(generated)
for unit, num, title, n in blanks:
    out = os.path.join(LW, key(n) + ".png")
    scene = scene_for(title, NAMES.get(unit, unit))
    if not scene:
        print(f"  [L{num}] {title[:40]}: NO SCENE", flush=True); continue
    print(f"  [L{num}] {title[:40]}\n      scene: {scene}", flush=True)
    img, err = render(img_prompt(scene))
    if img:
        img.save(out); manifest[n] = "/design-lab/assets/lw/" + key(n) + ".png"; genset.add(n)
        print("      -> ok", flush=True)
    else:
        print(f"      -> FAILED ({err})", flush=True)

json.dump(manifest, open(MANI_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(sorted(genset), open(os.path.join(ROOT, "design-lab", "_lw_generated.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# rebuild index with source field
idx = []
for unit, rows in DATA.items():
    for r in rows:
        n = norm(r.get("hero_image_url"))
        lw = manifest.get(n)
        src = "generated" if n in genset else ("photo" if lw else "none")
        idx.append({"unit": unit, "unitName": NAMES.get(unit, unit), "number": r.get("lesson_number"),
                    "title": r.get("title"), "laddered": bool(lw), "lw": lw, "source": src})
json.dump(idx, open(os.path.join(ROOT, "design-lab", "_lw_pilot_index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
lad = sum(1 for x in idx if x["laddered"])
print(f"\nnow {lad}/{len(idx)} laddered ({len(genset)} generated from scratch)", flush=True)
