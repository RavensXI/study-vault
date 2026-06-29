"""Build the hero-showcase doc: for a spread of units, fetch the REAL hero + lessons
from Supabase, ladder the hero (sketch + refined + complete), and write a manifest
(design-lab/_hero_showcase.json) for hero-showcase.html to render lanes from.

Stage images land in design-lab/assets/showcase/<key>-{sketch,refined,complete}.png
Run: python scripts/_designlab_showcase_build.py
"""
import json, os, sys, io, urllib.request
from supabase import create_client
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOW = os.path.join(ROOT, "design-lab", "assets", "showcase")
os.makedirs(SHOW, exist_ok=True)
sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# (subject_slug, unit_slug, mastery 0..1)  — masteries vary so the doc shows all three default stages
TARGETS = [
    ("history-aqa", "germany-democracy-dictatorship", 1.0),
    ("business-edexcel", "building-a-business", 0.55),
    ("english-literature-aqa", "macbeth", 0.25),
    ("geography-aqa", "paper-1", 1.0),
    ("religious-studies-aqa", "christianity-beliefs", 0.45),
    ("psychology-aqa", "memory", 0.0),
]

KEEP = ("Keep the SAME composition and layout — every element in the SAME place as the input image. "
        "ABSOLUTELY NO text, words, letters or numbers.")
STAGES = {
 "refined": ("Redraw this exact image as a REFINED study, partway to finished: clean confident pen-and-ink linework "
             "tracing the forms with a first thin watercolour wash of the same colours, still mostly warm uncoloured "
             "paper — as if the picture is coming into focus. " + KEEP),
 "sketch":  ("Redraw this exact image as a loose PENCIL SKETCH: rough, light, unfinished graphite linework on warm "
             "paper, no colour, a quick first study — as if barely in focus yet. " + KEEP),
}

def fetch_hero(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (StudyVault design-lab)"})
    with urllib.request.urlopen(req, timeout=40) as r:
        data = r.read()
    im = Image.open(io.BytesIO(data)).convert("RGB")
    if im.width > 1280:
        im = im.resize((1280, round(im.height * 1280 / im.width)))
    im.save(dest, quality=88)
    return im

def extract(r):
    for c in (r.candidates or []):
        for p in (c.content.parts or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def transform(hero, prompt, out, aspect):
    for cfg in (types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio=aspect)),
                types.GenerateContentConfig(response_modalities=["IMAGE"])):
        try:
            r = client.models.generate_content(model="gemini-3-pro-image-preview", contents=[prompt, hero], config=cfg)
            d = extract(r)
            if d:
                open(out, "wb").write(d); return True
        except Exception as e:
            print("   err", str(e)[:120], flush=True)
    return False

manifest = []
for skey, uslug, m in TARGETS:
    sub = sb.table("subjects").select("id,name").eq("slug", skey).is_("school_id", "null").execute().data
    if not sub:
        print(f"[{skey}/{uslug}] no subject", flush=True); continue
    sid, sname = sub[0]["id"], sub[0]["name"]
    unit = sb.table("units").select("name,image_url").eq("subject_id", sid).eq("slug", uslug).execute().data
    if not unit or not unit[0].get("image_url"):
        print(f"[{skey}/{uslug}] no unit/hero", flush=True); continue
    uname, hero_url = unit[0]["name"], unit[0]["image_url"]
    if hero_url.startswith("/"):
        print(f"[{skey}/{uslug}] local hero, skip", flush=True); continue
    lessons = sb.table("lessons").select("lesson_number,title,units!inner(slug,subjects!inner(slug,school_id))") \
        .eq("units.slug", uslug).eq("units.subjects.slug", skey).is_("units.subjects.school_id", "null") \
        .eq("status", "live").order("lesson_number").limit(12).execute().data
    lessons = [{"no": l["lesson_number"], "t": l["title"]} for l in lessons][:10]
    if len(lessons) < 3:
        print(f"[{skey}/{uslug}] too few lessons ({len(lessons)})", flush=True); continue
    key = f"{skey}__{uslug}"
    print(f"[{key}] {sname} · {uname} — {len(lessons)} lessons, hero…", flush=True)
    try:
        hero = fetch_hero(hero_url, os.path.join(SHOW, f"{key}-complete.jpg"))
    except Exception as e:
        print(f"   hero download failed: {str(e)[:100]}", flush=True); continue
    ar = hero.width / hero.height
    aspect = "3:2" if abs(ar - 1.5) < 0.18 else ("16:9" if ar > 1.6 else ("4:3" if ar > 1.2 else "1:1"))
    stage_files = {"complete": f"assets/showcase/{key}-complete.jpg"}
    for st, prompt in STAGES.items():
        out = os.path.join(SHOW, f"{key}-{st}.png")
        if transform(hero, prompt, out, aspect):
            stage_files[st] = f"assets/showcase/{key}-{st}.png"; print(f"   {st} ok", flush=True)
        else:
            print(f"   {st} FAILED", flush=True)
    done = round(m * len(lessons))
    manifest.append({"key": key, "subject": sname, "unit": uname, "mastery": m, "done": done,
                     "lessons": lessons, "stages": stage_files})

out = os.path.join(ROOT, "design-lab", "_hero_showcase.json")
json.dump(manifest, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"\nmanifest: {len(manifest)} units -> {out}", flush=True)
