# -*- coding: utf-8 -*-
"""Rewrite every free-tier hero caption to the concise two-part standard
(Tom, 30 Jul — docs/PIPELINE.md Phase 4):

    [what it shows, 3-6 words] — [link to the lesson, 4-8 words] (credit)

One Haiku vision call per hero: it sees the image AND the lesson, writes
both clauses grounded (first clause strictly visible-truth), the credit is
rescued from the existing caption, British English enforced. School-bespoke
rows untouched. Resumable JSONL ledger; --apply writes, default dry-runs
the first screenful.

    python scripts/_hero_caption_two_part.py --trial 8    # sample, no writes
    python scripts/_hero_caption_two_part.py --apply      # full run, writes
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.hero_pipeline import briticise
import anthropic

MODEL = "claude-haiku-4-5-20251001"
WORKERS = 3
SCRATCH = os.path.join(
    r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault",
    r"b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")
LEDGER = os.path.join(SCRATCH, "_caption_two_part.jsonl")

SB_URL = os.environ["SUPABASE_URL"]
SB_KEY = os.environ["SUPABASE_SERVICE_KEY"]

PROMPT = """You write the caption for the hero image of a GCSE revision lesson (students aged 15-16).

LESSON: {title}
ABOUT: {description}
SUBJECT: {subject_name}

Look at the image. Write ONE caption in EXACTLY this shape:
[what it shows, 3-6 words] — [its link to this lesson, 4-8 words]

Rules: under 12 words total. First clause = strictly what is visible, no speculation. Second clause may reference the lesson topic — it is what makes the image make sense here. No "representing", "illustrating", "showing", "symbolising", "demonstrating", "demonstrates". No full stop. Do not include any credit — that is appended separately.
Example: An empty courtroom — where sentencing decisions are made

Reply with ONLY the caption text."""


def sq(path):
    r = urllib.request.Request(SB_URL + "/rest/v1/" + path,
                               headers={"apikey": SB_KEY, "Authorization": "Bearer " + SB_KEY})
    return json.load(urllib.request.urlopen(r))


def sb_patch(lesson_id, caption):
    body = json.dumps({"hero_image_caption": caption}).encode()
    r = urllib.request.Request(
        SB_URL + "/rest/v1/lessons?id=eq." + lesson_id, data=body, method="PATCH",
        headers={"apikey": SB_KEY, "Authorization": "Bearer " + SB_KEY,
                 "Content-Type": "application/json"})
    urllib.request.urlopen(r)


def extract_credit(caption):
    """Rescue attribution in ANY style the platform has used, normalised."""
    c = caption or ""
    m = re.search(r"\(([^()]*(?:Unsplash|Pexels|Pixabay|Wikimedia|Photo|Image|Geograph|©)[^()]*)\)\s*$", c)
    if m:
        return m.group(1)
    m = re.search(r"(?:Photo|Image)(?:\s+by|:)\s+([^/()—-]+?)\s*(?:on|/)\s*(Unsplash|Pexels|Pixabay)", c)
    if m:
        word = "Image" if m.group(2) == "Pixabay" else "Photo"
        return f"{word}: {m.group(1).strip()} / {m.group(2)}"
    for src in ("Unsplash", "Pexels", "Pixabay", "Geograph"):
        if src in c:
            return src
    if re.search(r"Wikimedia|wikipedia", c, re.I):
        return "Wikimedia Commons"
    return ""


def fetch_jobs():
    subs = {s["id"]: s for s in sq("subjects?select=id,slug,name,school_id&limit=500")}
    units = sq("units?select=id,subject_id,slug,name&limit=2000")
    ubid = {u["id"]: u for u in units}
    jobs, off = [], 0
    while True:
        page = sq("lessons?select=id,unit_id,lesson_number,title,description,"
                  f"hero_image_url,hero_image_caption&order=id&limit=1000&offset={off}")
        for l in page:
            u = ubid.get(l["unit_id"])
            s = subs.get(u["subject_id"]) if u else None
            if not s or s["school_id"] or not l.get("hero_image_url"):
                continue
            jobs.append({"lesson_id": l["id"], "subject": s["slug"],
                         "subject_name": s["name"], "unit": u["slug"],
                         "n": l["lesson_number"], "title": l["title"],
                         "description": l.get("description") or "",
                         "url": l["hero_image_url"],
                         "old": l.get("hero_image_caption") or ""})
        if len(page) < 1000:
            break
        off += 1000
    su = os.environ.get("CAPTION_SUBJECT")
    un = os.environ.get("CAPTION_UNIT")
    if su:
        jobs = [j for j in jobs if j["subject"] == su]
    if un:
        jobs = [j for j in jobs if j["unit"] == un]
    return jobs


def fetch_image(url):
    url = urllib.parse.quote(url, safe=":/?&=%")
    req = urllib.request.Request(url, headers={"User-Agent": "StudyVaultHeroBot/1.0"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return resp.read()


_lock = threading.Lock()
_count = {"n": 0}


def caption_one(client, job, total, apply):
    try:
        img = fetch_image(job["url"])
        msg = client.messages.create(
            model=MODEL, max_tokens=100,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                             "data": base64.b64encode(img).decode()}},
                {"type": "text", "text": PROMPT.format(
                    title=job["title"], description=job["description"][:300],
                    subject_name=job["subject_name"])}]}])
        text = briticise(msg.content[0].text.strip().strip('"').rstrip("."))
        if not (3 <= len(text.split()) <= 16 and "—" in text):
            raise ValueError(f"malformed caption: {text[:60]}")
        credit = extract_credit(job["old"])
        new = f"{text} ({credit})" if credit else text
        if apply:
            sb_patch(job["lesson_id"], new)
        rec = {**{k: job[k] for k in ("lesson_id", "subject", "unit", "n")},
               "old": job["old"], "new": new, "applied": apply}
    except Exception as e:
        rec = {**{k: job[k] for k in ("lesson_id", "subject", "unit", "n")},
               "error": str(e)[:160]}
    with _lock:
        with io.open(LEDGER, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        _count["n"] += 1
        if _count["n"] % 100 == 0:
            print(f"  {_count['n']}/{total}", flush=True)
    return rec


def main():
    apply = "--apply" in sys.argv
    trial = int(sys.argv[sys.argv.index("--trial") + 1]) if "--trial" in sys.argv else 0

    done = set()
    if os.path.exists(LEDGER) and not trial:
        with io.open(LEDGER, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    if r.get("applied"):
                        done.add(r["lesson_id"])
                except json.JSONDecodeError:
                    pass

    jobs = [j for j in fetch_jobs() if j["lesson_id"] not in done]
    if trial:
        jobs = jobs[::max(1, len(jobs) // trial)][:trial]
    print(f"captions to write: {len(jobs)} (already done {len(done)}) | apply={apply}")

    client = anthropic.Anthropic()
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        results = list(ex.map(lambda j: caption_one(client, j, len(jobs), apply), jobs))

    ok = [r for r in results if "new" in r]
    err = [r for r in results if "error" in r]
    print(f"done: {len(ok)} ok, {len(err)} errors")
    if trial:
        for r in ok:
            print(f"\n[{r['subject']}/{r['unit']} L{r['n']}]")
            print(f"  OLD: {r['old'][:100]}")
            print(f"  NEW: {r['new'][:100]}")


if __name__ == "__main__":
    main()
