# -*- coding: utf-8 -*-
"""Platform-wide hero VISION audit — grades every hero against its lesson.

Read-only: no DB writes, no uploads. One Haiku vision call per hero:
  GRADE   A (clearly on-topic) / B (generic-acceptable) / C (wrong image)
  CAPTION OK / WRONG — does the stored caption honestly describe the image?
  SHOWS   one factual sentence of what the image actually shows

Output: JSONL ledger in the scratchpad, resumable by lesson id.
    python scripts/_hero_vision_audit.py [--limit N]
"""
import base64
import io
import json
import os
import re
import sys
import threading
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import anthropic

MODEL = "claude-haiku-4-5-20251001"
WORKERS = 3
SKIP_SUBJECTS = set()
SCRATCH = os.path.join(
    r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault",
    r"b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")
LEDGER = os.path.join(SCRATCH, "_hero_vision_audit.jsonl")

SB_URL = os.environ["SUPABASE_URL"]
SB_KEY = os.environ["SUPABASE_SERVICE_KEY"]

PROMPT = """You are auditing the hero (header) image of a GCSE revision lesson (students aged 15-16).

LESSON: {title}
ABOUT: {description}
SUBJECT: {subject_name}
STORED CAPTION: {caption}

Look at the image. Reply in EXACTLY this format:

GRADE: A or B or C
CAPTION: OK or WRONG
SHOWS: one factual sentence (max 18 words) describing what the image actually shows.

Grading the image: A = clearly illustrates this lesson's topic. B = acceptable but generic (related mood/setting, not specific). C = wrong — unrelated subject matter, text-heavy screenshot, software UI, watermark, logo, or misleading for this topic.
Grading the caption: OK if the stored caption honestly describes what is visible in THIS image (minor wording latitude allowed). WRONG if it describes things that are not in the image."""


def sq(path):
    r = urllib.request.Request(SB_URL + "/rest/v1/" + path,
                               headers={"apikey": SB_KEY, "Authorization": "Bearer " + SB_KEY})
    return json.load(urllib.request.urlopen(r))


def fetch_jobs():
    subs = {s["id"]: s for s in sq("subjects?select=id,slug,name,school_id&limit=500")}
    units = sq("units?select=id,subject_id,slug,name&limit=2000")
    unit_by_id = {u["id"]: u for u in units}
    jobs, off = [], 0
    while True:
        page = sq("lessons?select=id,unit_id,lesson_number,title,description,"
                  f"hero_image_url,hero_image_caption&order=id&limit=1000&offset={off}")
        for l in page:
            u = unit_by_id.get(l["unit_id"])
            if not u:
                continue
            s = subs.get(u["subject_id"])
            if not s or s["slug"] in SKIP_SUBJECTS:
                continue
            if not l.get("hero_image_url"):
                continue
            jobs.append({
                "lesson_id": l["id"], "subject": s["slug"], "subject_name": s["name"],
                "school": bool(s["school_id"]), "unit": u["slug"], "unit_name": u["name"],
                "n": l["lesson_number"], "title": l["title"],
                "description": l.get("description") or "",
                "url": l["hero_image_url"], "caption": l.get("hero_image_caption") or "",
            })
        if len(page) < 1000:
            break
        off += 1000
    return jobs


def fetch_image(url):
    # Wikimedia's robot policy requires a descriptive UA with contact details
    ua = ("StudyVaultHeroAudit/1.0 (https://www.studyvault.co.uk; "
          "studyvault.info@gmail.com)")
    # legacy Unity R2 keys contain literal spaces — encode like a browser would
    url = urllib.parse.quote(url, safe=":/?&=%")
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=45) as resp:
        data = resp.read()
    if len(data) < 5000:
        raise ValueError(f"too small ({len(data)}b)")
    if len(data) > 4_500_000:  # api limit ~5MB base64 — shrink via PIL
        from PIL import Image
        im = Image.open(io.BytesIO(data)).convert("RGB")
        im.thumbnail((1400, 1400))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=80)
        data = buf.getvalue()
    return data


_write_lock = threading.Lock()
_count = {"done": 0}


def audit_one(client, job, total):
    rec = dict(job)
    try:
        img = fetch_image(job["url"])
        media = "image/png" if img[:4] == b"\x89PNG" else "image/jpeg"
        if media == "image/png":  # normalise: some R2 objects are PNG-in-.jpg
            from PIL import Image
            im = Image.open(io.BytesIO(img)).convert("RGB")
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=85)
            img, media = buf.getvalue(), "image/jpeg"
        msg = client.messages.create(
            model=MODEL, max_tokens=200,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media,
                                             "data": base64.b64encode(img).decode()}},
                {"type": "text", "text": PROMPT.format(
                    title=job["title"], description=job["description"][:400],
                    subject_name=job["subject_name"], caption=job["caption"] or "(none)")}]}])
        text = msg.content[0].text
        rec["grade"] = (re.search(r"GRADE:\s*([ABC])", text) or [None, "?"])[1]
        rec["caption_ok"] = bool(re.search(r"CAPTION:\s*OK", text))
        m = re.search(r"SHOWS:\s*(.+)", text)
        rec["shows"] = m.group(1).strip() if m else ""
    except Exception as e:
        rec["grade"] = "FETCH_FAIL"
        rec["error"] = str(e)[:200]
    with _write_lock:
        with io.open(LEDGER, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        _count["done"] += 1
        if _count["done"] % 50 == 0:
            print(f"  {_count['done']}/{total}")
    return rec


def main():
    limit = 0
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    done_ids = set()
    if os.path.exists(LEDGER):
        with io.open(LEDGER, encoding="utf-8") as f:
            for line in f:
                try:
                    done_ids.add(json.loads(line)["lesson_id"])
                except (json.JSONDecodeError, KeyError):
                    pass

    jobs = [j for j in fetch_jobs() if j["lesson_id"] not in done_ids]
    if limit:
        jobs = jobs[:limit]
    print(f"heroes to audit: {len(jobs)} (already done: {len(done_ids)})")

    client = anthropic.Anthropic()
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        list(ex.map(lambda j: audit_one(client, j, len(jobs)), jobs))

    print("audit complete")


if __name__ == "__main__":
    main()
