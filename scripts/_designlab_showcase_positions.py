"""Reuse Tom's QA'd hero crops: pull lesson-1 hero_image_position for each showcase
unit and add it to the manifest. Where the unit hero differs from the QA'd lesson-1
hero (i.e. the position wouldn't match), re-download the lesson-1 hero and re-ladder.
"""
import json, os, io, urllib.request
from supabase import create_client
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOW = os.path.join(ROOT, "design-lab", "assets", "showcase")
MAN = os.path.join(ROOT, "design-lab", "_hero_showcase.json")
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

def dl(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (StudyVault design-lab)"})
    im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=40).read())).convert("RGB")
    if im.width > 1280:
        im = im.resize((1280, round(im.height * 1280 / im.width)))
    im.save(dest, quality=88); return im

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

man = json.load(open(MAN, encoding="utf-8"))
for u in man:
    skey, uslug = u["key"].split("__")
    l = sb.table("lessons").select("hero_image_url,hero_image_position,units!inner(slug,image_url,subjects!inner(slug,school_id))") \
        .eq("units.slug", uslug).eq("units.subjects.slug", skey).is_("units.subjects.school_id", "null").eq("lesson_number", 1).execute().data
    if not l:
        print(f"{u['subject']}: no L1"); continue
    x = l[0]
    u["position"] = x.get("hero_image_position") or "center"
    l1hero, unithero = x.get("hero_image_url"), x["units"].get("image_url")
    if l1hero and l1hero != unithero:
        print(f"{u['subject']}: swapping to QA'd L1 hero + re-laddering…", flush=True)
        hero = dl(l1hero, os.path.join(SHOW, f"{u['key']}-complete.jpg"))
        ar = hero.width / hero.height
        aspect = "3:2" if abs(ar - 1.5) < 0.18 else ("16:9" if ar > 1.6 else ("4:3" if ar > 1.2 else "1:1"))
        for st, prompt in STAGES.items():
            transform(hero, prompt, os.path.join(SHOW, f"{u['key']}-{st}.png"), aspect)
        print(f"   done", flush=True)
    else:
        print(f"{u['subject']}: position '{u['position']}' (hero unchanged)", flush=True)

json.dump(man, open(MAN, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("manifest updated with positions")
