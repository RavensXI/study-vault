"""Paint the 19 lessons the /desk demo links to (Sam's 'next lesson' targets).
ALL PROMPT-ONLY — no source image is ever sent to the model (2 sources are
CC BY-SA, most are unverified, so every one gets the safe treatment the
business plan requires for BY-SA). Keyed by the lesson's stored hero URL so
skin-switcher's manifest swap picks them up. MERGES into _lw_manifest.json
(the old pilot script overwrites — do not reuse it for top-ups).
Also writes _lw_captions_demo.json {heroUrl: caption} for the switcher.
"""
import os, io, json, time, hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from google.genai import types
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LW = os.path.join(ROOT, "design-lab", "assets", "lw")
SC = r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad"
LESSONS = json.load(open(os.path.join(SC, "demo_lessons.json"), encoding="utf-8"))
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3-pro-image-preview"

STYLE = ("A REFINED study, partway to finished: clean confident pen-and-ink linework "
         "with a first thin watercolour wash, still mostly warm uncoloured paper — as if "
         "the picture is coming into focus. Wide landscape composition. "
         "FULL-BLEED artwork filling the entire frame edge to edge: do NOT show the "
         "sketchbook, page edges, spiral binding, desk, easel, hands, brushes, paints "
         "or any surroundings — the image IS the drawing itself, nothing around it. "
         "ABSOLUTELY NO text, words, letters or numbers. The scene: ")

# (sub, unit, n) -> [scene prompt, caption]
SCENES = {
 ("history-aqa","germany-democracy-dictatorship",5): [
   "a crowded 1920s Berlin street rally outside the Reichstag — flat caps and overcoats, blank banners "
   "held high, a tram and iron lamp posts, restless energy",
   "A street rally in Weimar Berlin · ink & wash illustration"],
 ("history-aqa","conflict-tension-first-world-war",3): [
   "dreadnought battleships in line at a naval review, grey hulls and big guns, coal smoke trailing "
   "across a cold sea, small launches alongside",
   "Dreadnoughts at review — the Anglo-German naval race · ink & wash illustration"],
 ("history-aqa","britain-health-people",2): [
   "a medieval monastery infirmary — a monk tending a patient on a low cot, shelves of labelled-less herb "
   "jars, arched stone windows, a physic garden glimpsed outside",
   "The monastery infirmary — medieval care of the sick · ink & wash illustration"],
 ("history-aqa","elizabethan-england",2): [
   "a candlelit Tudor council chamber — a long oak table with quills, sealed letters and maps, carved "
   "high-backed chairs, panelled walls, one chair grander than the rest",
   "The Privy Council chamber — where Elizabeth's ministers worked · ink & wash illustration"],
 ("english-literature-aqa","macbeth",5): [
   "a spiral stone castle stair at night, a single guttering candle on a step beside a fallen dagger, "
   "long trembling shadows up the curved wall",
   "A dagger on the castle stair · ink & wash illustration"],
 ("english-literature-aqa","a-christmas-carol",4): [
   "a small Victorian family Christmas dinner — a modest goose on a crowded little table, patched "
   "clothes, a tiny crutch propped by the hearth, warm firelight",
   "The Cratchits' Christmas dinner · ink & wash illustration"],
 ("english-literature-aqa","a-christmas-carol",6): [
   "a bright Victorian street on Christmas morning seen from an open sash window, a boy below hauling "
   "an enormous turkey, church spire and ringing-bell sky, snow on the sills",
   "Christmas morning from Scrooge's window · ink & wash illustration"],
 ("english-literature-aqa","power-and-conflict",4): [
   "a renaissance palace gallery — a tall portrait frame on the wall with its curtain half-drawn across "
   "an indistinct painted figure, marble floor, a bronze statue further along",
   "The curtained portrait — 'My Last Duchess' · ink & wash illustration"],
 ("science-aqa","biology-paper-1",5): [
   "a clinician's desk still life — stethoscope coiled beside a blood-pressure cuff and an anatomical "
   "model of a human heart, daylight from a surgery window",
   "Tools for measuring health · ink & wash illustration"],
 ("science-aqa","chemistry-paper-1",3): [
   "ball-and-stick molecular models and a giant ionic lattice model on a laboratory bench, scattered "
   "salt crystals, a bunsen burner unlit behind",
   "Models of chemical bonding on the lab bench · ink & wash illustration"],
 ("science-aqa","physics-paper-1",2): [
   "a wooden rollercoaster's highest crest with a car pausing at the top, the track sweeping down into "
   "a valley and rising again, fairground below",
   "Stored energy at the top of the ride · ink & wash illustration"],
 ("geography-aqa","paper-1",6): [
   "palm trees bent almost flat in a hurricane, storm surge flooding a tropical coastal street, "
   "shuttered houses and driven rain",
   "A tropical storm makes landfall · ink & wash illustration"],
 ("geography-aqa","paper-2",5): [
   "rows of terraced rooftops and chimneys stepping down a hillside toward a modern UK city skyline "
   "with cranes, seen in soft morning light",
   "Terraces to towers — a growing UK city · ink & wash illustration"],
 ("computer-science","computer-systems",4): [
   "an opened desktop computer as a close still life — RAM sticks standing in their slots on the "
   "motherboard, a screwdriver resting on the case edge",
   "Primary storage on the motherboard · ink & wash illustration"],
 ("computer-science","computer-systems",3): [
   "a kitchen counter with a microwave and washing machine, and in front of them a small bare "
   "circuit board with a single chip — the tiny computer inside the machines",
   "The tiny computers hidden inside everyday machines · ink & wash illustration"],
 ("computer-science","computational-thinking",3): [
   "a long wooden library card-catalogue with one drawer pulled out and a single card lifted "
   "mid-search, reading lamps glowing down the hall",
   "Searching the catalogue · ink & wash illustration"],
 ("religious-studies-ocr","christianity-beliefs-and-teachings",3): [
   "three crosses on a hill at dawn with an empty rock-cut tomb in the hillside below, its stone "
   "rolled aside, light breaking over the horizon",
   "The cross and the empty tomb · ink & wash illustration"],
 ("religious-studies-ocr","islam-beliefs-and-teachings",2): [
   "a mosque interior — a tiled mihrab with intricate geometric patterns, hanging brass lamps, "
   "soft light across the carpeted floor, no people",
   "The mihrab — turning towards Allah · ink & wash illustration"],
 ("religious-studies-ocr","theme-relationships-and-families",1): [
   "two wedding rings resting on a closed book beside a small bouquet on a linen-covered table, "
   "soft window light",
   "Rings, vows and family · ink & wash illustration"],
}

def norm(u): return (u or "").split("?")[0].strip()
def key(u): return hashlib.sha1(norm(u).encode("utf-8")).hexdigest()[:12]

def extract(r):
    for c in (r.candidates or []):
        for p in (getattr(getattr(c, "content", None), "parts", None) or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None

def gen(prompt):
    for attempt in range(4):
        for cfg in (types.GenerateContentConfig(response_modalities=["IMAGE"],
                        image_config=types.ImageConfig(aspect_ratio="16:9")),
                    types.GenerateContentConfig(response_modalities=["IMAGE"])):
            try:
                r = client.models.generate_content(model=MODEL, contents=[prompt], config=cfg)
                d = extract(r)
                if d:
                    return Image.open(io.BytesIO(d)).convert("RGB"), None
            except Exception as e:
                msg = str(e)
                if any(k in msg for k in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                    time.sleep(5 * (attempt + 1)); break
                return None, msg[:90]
    return None, "refused/empty"

def work(les):
    k = (les["sub"], les["unit"], les["n"])
    scene = SCENES.get(k)
    if not scene:
        return k, None, "no scene"
    out = os.path.join(LW, key(les["hero"]) + ".png")
    if os.path.exists(out):
        return k, les, "cached"
    img, err = gen(STYLE + scene[0])
    if img:
        img.save(out); return k, les, "ok"
    return k, None, err

results = {}
with ThreadPoolExecutor(max_workers=2) as ex:
    futs = [ex.submit(work, l) for l in LESSONS]
    for i, f in enumerate(as_completed(futs)):
        k, les, msg = f.result()
        results[k] = les
        print(f"[{i+1}/{len(LESSONS)}] {'OK ' if les else 'FAIL'} {msg:14s} {k[0][:12]}/{k[1][:30]}/{k[2]}", flush=True)

# MERGE into the manifest + write the caption sidecar
mpath = os.path.join(ROOT, "design-lab", "_lw_manifest.json")
manifest = json.load(open(mpath, encoding="utf-8"))
caps = {}
for k, les in results.items():
    if not les: continue
    n = norm(les["hero"])
    manifest[n] = "/design-lab/assets/lw/" + key(les["hero"]) + ".png"
    caps[n] = SCENES[k][1]
json.dump(manifest, open(mpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
cpath = os.path.join(ROOT, "design-lab", "_lw_captions_demo.json")
old = json.load(open(cpath, encoding="utf-8")) if os.path.exists(cpath) else {}
old.update(caps)
json.dump(old, open(cpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ok = sum(1 for v in results.values() if v)
print(f"\npainted {ok}/{len(LESSONS)} | manifest now {len(manifest)} entries | captions {len(old)}")
