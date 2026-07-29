# -*- coding: utf-8 -*-
"""Repair psychology-ocr + psychology-edexcel heroes (July 2026 incident).

The original scripts assigned cross-subject index matches sight-unseen, with
topic-derived captions that rarely described the actual image, and no dedupe.
This regenerates ALL heroes for both subjects through lib/hero_pipeline.py:
vision-gated, grounded captions, unique per subject, stored under each
subject's own R2 folder. psychology-aqa heroes act as a same-family reuse
pool (same topics), vision-gated like everything else.

Resumable: state in the scratchpad; done lessons are skipped on re-run.
    python scripts/_heroes_psychology_repair.py            # both subjects
    python scripts/_heroes_psychology_repair.py --one      # first pending lesson only
"""
import io
import json
import os
import sys

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.supabase_client import get_client
from lib.hero_pipeline import HeroFinder

SUBJECTS = [
    ("psychology-ocr", "OCR GCSE Psychology"),
    ("psychology-edexcel", "Edexcel GCSE Psychology"),
]
REUSE_SOURCE = "psychology-aqa"
STATE_PATH = os.path.join(
    r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault",
    r"b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad", "_hero_repair_state.json")


def load_state():
    if os.path.exists(STATE_PATH):
        with io.open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"done": {}, "failed": []}


def save_state(state):
    with io.open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=1, ensure_ascii=False)


def fetch_lessons(sb, subject_slug):
    subj = sb.table("subjects").select("id").eq("slug", subject_slug).execute()
    subject_id = subj.data[0]["id"]
    units = sb.table("units").select("id,slug,name").eq("subject_id", subject_id).execute()
    out = []
    for u in units.data:
        rows = (sb.table("lessons")
                .select("id,lesson_number,title,description,hero_image_url")
                .eq("unit_id", u["id"]).order("lesson_number").execute())
        for l in rows.data:
            out.append({"unit_slug": u["slug"], "unit_name": u["name"], **l})
    out.sort(key=lambda l: (l["unit_slug"], l["lesson_number"]))
    return out


def build_reuse_pool(sb):
    pool = []
    for l in fetch_lessons(sb, REUSE_SOURCE):
        url = l.get("hero_image_url") or ""
        # only same-family images that live in psychology-aqa's own R2 folder —
        # its offsite hotlinks and cross-subject strays don't get propagated
        if "/psychology-aqa/" in url:
            row = sb.table("lessons").select("hero_image_caption").eq("id", l["id"]).execute()
            pool.append({"url": url, "title": l["title"],
                         "caption": (row.data[0] or {}).get("hero_image_caption", "")})
    return pool


def main():
    one_only = "--one" in sys.argv
    sb = get_client()
    finder = HeroFinder()
    state = load_state()
    finder.used.update(u for rec in state["done"].values() for u in rec.get("used", []))

    reuse_pool = build_reuse_pool(sb)
    print(f"Reuse pool from {REUSE_SOURCE}: {len(reuse_pool)} images")

    # Unsplash's search API allows ~50 calls/hour: run in rounds, sleeping
    # between them, until every lesson is done or a round makes no progress
    # twice in a row.
    import time as _time
    stalled = 0
    while True:
        before = len(state["done"])
        run_round(sb, finder, state, reuse_pool, one_only)
        if one_only:
            return
        total = sum(len(fetch_lessons(sb, slug)) for slug, _ in SUBJECTS)
        if len(state["done"]) >= total:
            break
        stalled = stalled + 1 if len(state["done"]) == before else 0
        if stalled >= 2:
            print("no progress across two rounds — stopping for inspection")
            break
        print(f"\n{len(state['done'])}/{total} done — sleeping 20 min for the "
              f"Unsplash search window to reset...")
        _time.sleep(20 * 60)

    done_n = len(state["done"])
    print(f"\nDone: {done_n} lessons | failed: {state['failed'] or 'none'}")
    print(f"vision calls: {finder.vision_calls}")


def run_round(sb, finder, state, reuse_pool, one_only):
    state["failed"] = []
    for subject_slug, board_label in SUBJECTS:
        lessons = fetch_lessons(sb, subject_slug)
        print(f"\n===== {subject_slug}: {len(lessons)} lessons =====")
        for l in lessons:
            key = f"{subject_slug}/{l['unit_slug']}/L{l['lesson_number']:02d}"
            if key in state["done"]:
                continue
            print(f"\n--- {key}  \"{l['title']}\"")
            print(f"    old: {(l.get('hero_image_url') or 'NONE')[:90]}")

            result = finder.find(
                subject_slug=subject_slug, subject_name="Psychology",
                unit_slug=l["unit_slug"], unit_name=l["unit_name"],
                lesson_number=l["lesson_number"], title=l["title"],
                description=l.get("description") or "", reuse_pool=reuse_pool)

            if not result:
                print("    [FAIL] no acceptable image found")
                state["failed"].append(key)
                save_state(state)
                continue

            alt = f"{l['title']} — {l['unit_name']} for {board_label}"
            sb.table("lessons").update({
                "hero_image_url": result["url"],
                "hero_image_caption": result["caption"],
                "hero_image_alt": alt,
                "hero_image_position": "center center",
            }).eq("id", l["id"]).execute()

            state["done"][key] = {
                "url": result["url"], "source": result["source"],
                "caption": result["caption"], "old": l.get("hero_image_url"),
                "used": sorted(finder.used),
            }
            # keep only the newest 'used' snapshot to bound file size
            for k in list(state["done"]):
                if k != key and "used" in state["done"][k]:
                    del state["done"][k]["used"]
            save_state(state)
            print(f"    [OK] {result['source']}: {result['caption'][:90]}")

            if one_only:
                print("\n--one: stopping after the first lesson.")
                print(f"vision calls so far: {finder.vision_calls}")
                return


if __name__ == "__main__":
    main()
