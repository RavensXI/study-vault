# -*- coding: utf-8 -*-
"""Regenerate platform heroes from the worklist, through lib/hero_pipeline.

Sharded BY SUBJECT so shards can run in parallel with no dedupe races:
    python scripts/_hero_regen_run.py --shard 0 --of 3
    python scripts/_hero_regen_run.py --shard 0 --of 3 --one   # trial
Each shard pre-seeds the finder's used-set with every hero URL the subject
is KEEPING, so a regenerated lesson can never duplicate a kept image.
Resumable per shard; rounds sleep 15 min if sources run dry mid-shard.
"""
import io
import json
import os
import sys
import time

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

SCRATCH = os.path.join(
    r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault",
    r"b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")
WORKLIST = os.path.join(SCRATCH, "_hero_regen_worklist.json")


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def norm(url):
    return (url or "").split("?")[0]


def main():
    shard, of = int(arg("--shard", "0")), int(arg("--of", "1"))
    one_only = "--one" in sys.argv
    state_path = os.path.join(SCRATCH, f"_hero_regen_state_{shard}.json")
    state = {"done": {}, "failed": []}
    if os.path.exists(state_path):
        state = json.load(io.open(state_path, encoding="utf-8"))

    rows = json.load(io.open(WORKLIST, encoding="utf-8"))
    subjects = sorted({r["subject"] for r in rows})
    mine = {s for i, s in enumerate(subjects) if i % of == shard}
    rows = [r for r in rows if r["subject"] in mine]
    print(f"shard {shard}/{of}: {len(mine)} subjects, {len(rows)} lessons "
          f"({len(state['done'])} already done)")

    sb = get_client()
    finder = HeroFinder()

    # pre-seed used with every hero URL the shard's subjects are KEEPING
    regen_ids = {r["lesson_id"] for r in rows}
    for s in mine:
        subj = sb.table("subjects").select("id").eq("slug", s).execute().data[0]
        units = sb.table("units").select("id").eq("subject_id", subj["id"]).execute()
        for u in units.data:
            for l in (sb.table("lessons").select("id,hero_image_url")
                      .eq("unit_id", u["id"]).execute()).data:
                if l["id"] not in regen_ids and l.get("hero_image_url"):
                    finder.used.add(norm(l["hero_image_url"]))
    print(f"pre-seeded {len(finder.used)} kept image ids")

    stalled = 0
    while True:
        state["failed"] = []
        progressed = False
        for r in rows:
            if r["lesson_id"] in state["done"]:
                continue
            key = f"{r['subject']}/{r['unit']}/L{r['n']:02d}"
            print(f"\n--- {key} [{r['reason']}] \"{r['title'][:55]}\"")
            result = finder.find(
                subject_slug=r["subject"], subject_name=r["subject_name"],
                unit_slug=r["unit"], unit_name=r["unit_name"],
                lesson_number=r["n"], title=r["title"],
                description=r.get("description") or "")
            if not result:
                print("    [FAIL] no acceptable image")
                state["failed"].append(key)
                continue
            patch = {"hero_image_url": result["url"],
                     "hero_image_caption": result["caption"],
                     "hero_image_position": "center center"}
            old_alt = ""
            row = sb.table("lessons").select("hero_image_alt") \
                .eq("id", r["lesson_id"]).execute()
            if row.data:
                old_alt = row.data[0].get("hero_image_alt") or ""
            if not old_alt:
                patch["hero_image_alt"] = f"{r['title']} — {r['unit_name']}, {r['subject_name']}"
            sb.table("lessons").update(patch).eq("id", r["lesson_id"]).execute()
            state["done"][r["lesson_id"]] = {
                "key": key, "url": result["url"], "source": result["source"],
                "caption": result["caption"], "old": r["url"], "reason": r["reason"]}
            json.dump(state, io.open(state_path, "w", encoding="utf-8"),
                      indent=1, ensure_ascii=False)
            progressed = True
            print(f"    [OK] {result['source']}: {result['caption'][:85]}")
            if one_only:
                print("\n--one: stopping.")
                return
        if len(state["done"]) >= len(rows):
            break
        stalled = 0 if progressed else stalled + 1
        if stalled >= 2:
            print("no progress across two rounds — stopping for inspection")
            break
        print(f"\n{len(state['done'])}/{len(rows)} — sleeping 15 min for quotas...")
        time.sleep(15 * 60)

    print(f"\nshard {shard} done: {len(state['done'])}/{len(rows)} | "
          f"failed: {state['failed'] or 'none'} | vision calls {finder.vision_calls}")


if __name__ == "__main__":
    main()
