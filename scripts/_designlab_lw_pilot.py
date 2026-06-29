"""PILOT: line-and-wash (Pro) every hero in SAM's History (history-ocr, 4 units).
Downloads each lesson hero, redraws it with gemini-3-pro-image-preview, and writes:
  design-lab/assets/lw/<hash>.png            the refined heroes
  design-lab/_lw_manifest.json               { normalizedHeroUrl: "/design-lab/assets/lw/<hash>.png" }
                                             (skin-switcher reads this to swap heroes locally)
  design-lab/_lw_pilot_index.json            [ {unit,unitName,number,title,laddered} ] for the index page
People-heavy subject → expect Pro to REFUSE recognisable-person portraits; those
are recorded as not-laddered (lesson keeps its photo). Re-runnable: skips heroes
already rendered.
"""
import os, io, json, time, hashlib, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LW = os.path.join(ROOT, "design-lab", "assets", "lw")
os.makedirs(LW, exist_ok=True)
DATA = json.load(open(os.path.join(ROOT, "scratch_history_pilot.json"), encoding="utf-8"))
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3-pro-image-preview"

UNIT_NAMES = {
    "international-relations-1918-1975": "International Relations 1918–1975",
    "germany-people-state-1925-1955": "Germany 1925–1955: The People and the State",
    "migration-to-britain-1000-2010": "Migration to Britain c.1000–c.2010",
    "usa-people-state-1919-1948": "The USA 1919–1948: The People and the State",
}

KEEP = ("Keep the SAME composition and layout — every element in the SAME place as the input image. "
        "ABSOLUTELY NO text, words, letters or numbers.")
PROMPT = ("Redraw this exact image as a REFINED study, partway to finished: clean confident pen-and-ink "
          "linework tracing the forms with a first thin watercolour wash of the same colours, still mostly warm "
          "uncoloured paper — as if the picture is coming into focus. " + KEEP)

def norm(u):
    return (u or "").split("?")[0].strip()

def key(u):
    return hashlib.sha1(norm(u).encode("utf-8")).hexdigest()[:12]

UA = "StudyVault/1.0 (+https://www.studyvault.co.uk; studyvault.info@gmail.com) Python-urllib"
def dl(url):
    if "wikimedia.org" in url or "wikipedia.org" in url:
        time.sleep(1.3)   # Wikimedia asks for polite, throttled access (429 otherwise)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=45).read())).convert("RGB")
    if im.width > 1280:
        im = im.resize((1280, round(im.height * 1280 / im.width)))
    return im

def aspect_of(im):
    ar = im.width / im.height
    return "3:2" if abs(ar - 1.5) < 0.18 else ("16:9" if ar > 1.6 else ("4:3" if ar > 1.2 else "1:1"))

def extract(r):
    for c in (r.candidates or []):
        cont = getattr(c, "content", None)
        for p in (getattr(cont, "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def ladder(hero, aspect):
    for attempt in range(4):
        for cfg in (types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio=aspect)),
                    types.GenerateContentConfig(response_modalities=["IMAGE"])):
            try:
                r = client.models.generate_content(model=MODEL, contents=[PROMPT, hero], config=cfg)
                d = extract(r)
                if d:
                    return Image.open(io.BytesIO(d)).convert("RGB"), None
            except Exception as e:
                msg = str(e)
                if any(k in msg for k in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                    time.sleep(5 * (attempt + 1)); break
                return None, msg[:90]
    return None, "refused/empty"

# unique heroes across the 4 units
uniq = {}
for unit, rows in DATA.items():
    for r in rows:
        u = r.get("hero_image_url")
        if u and not u.startswith("/"):
            uniq.setdefault(norm(u), u)

def work(nurl, full):
    out = os.path.join(LW, key(nurl) + ".png")
    if os.path.exists(out):
        return nurl, True, "cached"
    try:
        hero = dl(full)
    except Exception as e:
        return nurl, False, "dl:" + str(e)[:60]
    img, err = ladder(hero, aspect_of(hero))
    if img:
        img.save(out); return nurl, True, "ok"
    return nurl, False, err

print(f"{len(uniq)} unique heroes to ladder (Pro)…", flush=True)
status = {}
with ThreadPoolExecutor(max_workers=2) as ex:
    futs = {ex.submit(work, n, f): n for n, f in uniq.items()}
    done = 0
    for fut in as_completed(futs):
        nurl, ok, msg = fut.result(); status[nurl] = ok; done += 1
        print(f"  [{done}/{len(uniq)}] {'OK ' if ok else 'SKIP'} {msg}  {nurl.split('/')[-1][:42]}", flush=True)

# manifest: only laddered heroes get a swap entry
manifest = {n: "/design-lab/assets/lw/" + key(n) + ".png" for n, ok in status.items() if ok}
json.dump(manifest, open(os.path.join(ROOT, "design-lab", "_lw_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# index for the pilot page
index = []
for unit, rows in DATA.items():
    for r in rows:
        n = norm(r.get("hero_image_url"))
        index.append({"unit": unit, "unitName": UNIT_NAMES.get(unit, unit),
                      "number": r.get("lesson_number"), "title": r.get("title"),
                      "laddered": bool(manifest.get(n))})
json.dump(index, open(os.path.join(ROOT, "design-lab", "_lw_pilot_index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

lad = sum(1 for v in status.values() if v)
print(f"\nladdered {lad}/{len(uniq)} | refused/failed {len(uniq)-lad}", flush=True)
print("wrote _lw_manifest.json + _lw_pilot_index.json", flush=True)
