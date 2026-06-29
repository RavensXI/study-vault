"""Roll the hero-banner treatment out to ALL of SAM's units: for each unit use its
real lesson-1 hero (falling back to the subject hero for practice-format units with
no lesson hero), ladder it (sketch + refined + complete), and write the files the
dashboard reads (path-bg-u-<skey>-<slug>-land{,-refined,-photo}.png). Also stamps the
QA'd hero crop (hero_image_position) into design-lab/_path_backdrops.json.

Resumable via scratch_rollout_state.json. Idempotent per source URL (a shared subject
hero is laddered once and copied). Run: python scripts/_designlab_hero_rollout.py
"""
import json, os, io, urllib.request
from supabase import create_client
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
MANIFEST = os.path.join(ROOT, "design-lab", "_path_backdrops.json")
STATE = os.path.join(ROOT, "scratch_rollout_state.json")
UNITS = json.load(open(os.path.join(ROOT, "scratch_sam_units.json"), encoding="utf-8"))
sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

KEEP = ("Keep the SAME composition and layout — every element in the SAME place as the input image. "
        "ABSOLUTELY NO text, words, letters or numbers.")
STAGES = {
 "refined": ("Redraw this exact image as a REFINED study, partway to finished: clean confident pen-and-ink linework "
             "tracing the forms with a first thin watercolour wash of the same colours, still mostly warm uncoloured "
             "paper — as if the picture is coming into focus. " + KEEP),
 "sketch":  ("Redraw this exact image as a loose PENCIL SKETCH: rough, light, unfinished graphite linework on warm "
             "paper, no colour, a quick first study — as if barely in focus yet. " + KEEP),
}

def dl(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (StudyVault design-lab)"})
    im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=45).read())).convert("RGB")
    if im.width > 1280:
        im = im.resize((1280, round(im.height * 1280 / im.width)))
    return im

def extract(r):
    for c in (r.candidates or []):
        for p in (c.content.parts or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def transform(hero, prompt, aspect):
    for cfg in (types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio=aspect)),
                types.GenerateContentConfig(response_modalities=["IMAGE"])):
        try:
            r = client.models.generate_content(model="gemini-3-pro-image-preview", contents=[prompt, hero], config=cfg)
            d = extract(r)
            if d:
                return Image.open(io.BytesIO(d)).convert("RGB")
        except Exception as e:
            print("     err", str(e)[:110], flush=True)
    return None

CACHE = {}   # source URL -> {complete, refined, sketch} PIL images
def ladder(url):
    if url in CACHE:
        return CACHE[url]
    hero = dl(url)
    ar = hero.width / hero.height
    aspect = "3:2" if abs(ar - 1.5) < 0.18 else ("16:9" if ar > 1.6 else ("4:3" if ar > 1.2 else "1:1"))
    out = {"complete": hero}
    for st, prompt in STAGES.items():
        out[st] = transform(hero, prompt, aspect)
    CACHE[url] = out
    return out

def l1_hero(skey, slug):
    l = sb.table("lessons").select("hero_image_url,hero_image_position,units!inner(slug,subjects!inner(slug,school_id))") \
        .eq("units.slug", slug).eq("units.subjects.slug", skey).is_("units.subjects.school_id", "null").eq("lesson_number", 1).execute().data
    if l:
        return l[0].get("hero_image_url"), (l[0].get("hero_image_position") or "center")
    return None, "center"

def subject_hero(skey):
    s = sb.table("subjects").select("image_url").eq("slug", skey).is_("school_id", "null").execute().data
    return (s[0].get("image_url") if s else None)

manifest = json.load(open(MANIFEST, encoding="utf-8"))
state = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
made = skipped = nohero = 0
for skey, sub in UNITS.items():
    subhero = subject_hero(skey)
    print(f"== {skey} (subject hero: {'yes' if subhero else 'no'}) ==", flush=True)
    for u in sub["units"]:
        slug = u["slug"]; key = f"{skey}/{slug}"
        if state.get(key) in ("ok", "nohero"):
            skipped += 1; continue
        url, pos = l1_hero(skey, slug)
        if not url or url.startswith("/"):
            url, pos = (subhero, "center") if subhero and not str(subhero).startswith("/") else (None, pos)
        if key in manifest:
            manifest[key]["position"] = pos
        if not url:
            state[key] = "nohero"; nohero += 1; print(f"   - {slug}: no hero (gradient)", flush=True); continue
        try:
            lad = ladder(url)
        except Exception as e:
            print(f"   ! {slug}: download/ladder failed: {str(e)[:90]}", flush=True); continue
        base = os.path.join(ASSETS, f"path-bg-u-{skey}-{slug}")
        lad["complete"].save(base + "-land-photo.png")
        if lad.get("refined"): lad["refined"].save(base + "-land-refined.png")
        if lad.get("sketch"):  lad["sketch"].save(base + "-land.png")
        state[key] = "ok"; made += 1
        print(f"   Y {slug}  pos:{pos}", flush=True)
        json.dump(state, open(STATE, "w"), indent=1)
        json.dump(manifest, open(MANIFEST, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
json.dump(state, open(STATE, "w"), indent=1)
json.dump(manifest, open(MANIFEST, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"\nrollout: made {made}, skipped {skipped}, no-hero {nohero}", flush=True)
