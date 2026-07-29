# -*- coding: utf-8 -*-
"""Line-and-wash model pilot (30 Jul 2026): current Flash vs Pro image tier,
on 30 REAL heroes straight from R2, using the LOCKED refined prompt from the
June pilot (scripts/_designlab_flash_test.py). Decides whether the platform
rollout costs ~£130 (Flash) or ~£260 (Pro).

Outputs to the scratchpad: {slug}-{unit}-L{n}-{orig|flash|pro}.png + a
compare page. Non-destructive; nothing touches Supabase or R2.
"""
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

from google import genai
from google.genai import types
from PIL import Image

SCRATCH = os.path.join(
    r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault",
    r"b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad", "_lw_pilot")
os.makedirs(SCRATCH, exist_ok=True)

SB_URL = os.environ["SUPABASE_URL"]
SB_KEY = os.environ["SUPABASE_SERVICE_KEY"]
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# (subject, unit, lesson_numbers) — a deliberate spread of image kinds:
# engravings, colour photos, lab shots, landscapes, portraits, crowds.
PICKS = [
    ("history-edexcel", "medicine-in-britain", [3, 5, 8]),
    ("history-aqa", "conflict-tension-inter-war", [2, 6]),
    ("science-aqa", "biology-paper-1", [1, 4, 7]),
    ("science-edexcel", "chemistry-paper-1", [1, 7]),
    ("geography-aqa", "paper-1", [2, 6, 10]),
    ("english-literature-aqa", "macbeth", [1, 5]),
    ("english-literature-edexcel", "jane-eyre", [1, 5]),
    ("psychology-ocr", "criminal-psychology", [1, 3]),
    ("psychology-edexcel", "perception", [1]),
    ("business-aqa", "business-real-world", [1, 4]),
    ("religious-studies-aqa", "islam-practices", [1, 3]),
    ("physical-education-aqa", "human-body-and-movement", [1, 5]),
    ("computer-science", "computer-systems", [1]),  # OCR board; free-tier slug has no suffix
    ("statistics-aqa", "planning-designing-enquiry", [1]),
    ("drama-aqa", "theatre-roles-stagecraft", [1]),
    ("food-preparation-and-nutrition-aqa", "food-nutrition-and-health", [1]),
]
MODELS = [
    ("gemini-3.1-flash-image-preview", "gemini-2.5-flash-image", "flash"),
    ("gemini-3-pro-image-preview", "gemini-3-pro-image", "pro"),
]

KEEP = ("Keep the SAME composition and layout — every element in the SAME place as the input image. "
        "ABSOLUTELY NO text, words, letters or numbers.")
PROMPT = ("Redraw this exact image as a REFINED study, partway to finished: clean confident pen-and-ink "
          "linework tracing the forms with a first thin watercolour wash of the same colours, still mostly warm "
          "uncoloured paper — as if the picture is coming into focus. " + KEEP)


def sq(path):
    r = urllib.request.Request(SB_URL + "/rest/v1/" + path,
                               headers={"apikey": SB_KEY, "Authorization": "Bearer " + SB_KEY})
    return json.load(urllib.request.urlopen(r))


def collect_jobs():
    jobs = []
    for subj, unit, nums in PICKS:
        srows = sq(f"subjects?slug=eq.{subj}&select=id&school_id=is.null")
        if not srows:
            print("no free-tier subject:", subj, "— skipped")
            continue
        sid = srows[0]["id"]
        urow = [u for u in sq(f"units?subject_id=eq.{sid}&select=id,slug") if u["slug"] == unit]
        if not urow:
            print("no unit:", subj, unit)
            continue
        for l in sq(f"lessons?unit_id=eq.{urow[0]['id']}&select=lesson_number,title,hero_image_url"
                    f"&lesson_number=in.({','.join(map(str, nums))})&order=lesson_number"):
            if l["hero_image_url"]:
                jobs.append({"subject": subj, "unit": unit, "n": l["lesson_number"],
                             "title": l["title"], "url": l["hero_image_url"]})
    return jobs


def fetch_hero(url, dest):
    if os.path.exists(dest):
        return Image.open(dest).convert("RGB")
    u = urllib.parse.quote(url, safe=":/?&=%")
    req = urllib.request.Request(u, headers={"User-Agent": "StudyVaultHeroBot/1.0"})
    data = urllib.request.urlopen(req, timeout=60).read()
    im = Image.open(io.BytesIO(data)).convert("RGB")
    im.save(dest)
    return im


def aspect_of(im):
    ar = im.width / im.height
    return "3:2" if abs(ar - 1.5) < 0.18 else ("16:9" if ar > 1.6 else ("4:3" if ar > 1.2 else "1:1"))


def extract(r):
    for c in (r.candidates or []):
        for p in (c.content.parts or []):
            d = getattr(p, "inline_data", None)
            if d and getattr(d, "data", None):
                return d.data
    return None


def gen(model_ids, hero, aspect):
    last = ""
    for model in model_ids:
        for attempt in range(4):
            for cfg in (types.GenerateContentConfig(response_modalities=["IMAGE"],
                                                    image_config=types.ImageConfig(aspect_ratio=aspect)),
                        types.GenerateContentConfig(response_modalities=["IMAGE"])):
                try:
                    r = client.models.generate_content(model=model, contents=[PROMPT, hero], config=cfg)
                    d = extract(r)
                    if d:
                        return Image.open(io.BytesIO(d)).convert("RGB"), model, None
                except Exception as e:
                    last = str(e)[:140]
                    if "NOT_FOUND" in last or "404" in last:
                        break  # unknown model id -> try the fallback id
                    if any(k in last for k in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                        time.sleep(5 * (attempt + 1))
                        break
                    return None, model, last
            else:
                continue
            if "NOT_FOUND" in last or "404" in last:
                break
    return None, model_ids[-1], last or "empty"


def task(job, primary, fallback, suffix):
    key = f"{job['subject']}-{job['unit']}-L{job['n']:02d}"
    out = os.path.join(SCRATCH, f"{key}-{suffix}.png")
    if os.path.exists(out):
        return f"[{key}/{suffix}] cached"
    hero = fetch_hero(job["url"], os.path.join(SCRATCH, f"{key}-orig.png"))
    img, used, err = gen([primary, fallback], hero, aspect_of(hero))
    if img:
        img.save(out)
        return f"[{key}/{suffix}] ok ({used})"
    return f"[{key}/{suffix}] FAILED — {err}"


def main():
    jobs = collect_jobs()
    print(f"pilot heroes: {len(jobs)} x {len(MODELS)} models")
    work = [(j, p, f, sfx) for j in jobs for (p, f, sfx) in MODELS]
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(task, *w) for w in work]
        for fu in as_completed(futs):
            print("  " + fu.result(), flush=True)
    json.dump(jobs, io.open(os.path.join(SCRATCH, "_jobs.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print("done")


if __name__ == "__main__":
    main()
