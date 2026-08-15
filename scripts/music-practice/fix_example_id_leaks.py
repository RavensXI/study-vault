# -*- coding: utf-8 -*-
"""Sweep the authored worked examples for passage-id leaks in visible prose
(Tom, 16 Aug: aos-listening L1 says 'Play the excerpt for
p-aos2_rock_live_band before reading on'). The validator checked the ref was
real but not that the TEXT kept it out of the student's sight.

An intro mentioning any of its lesson's passage ids is normalised to a clean
line; a step mentioning one gets the id replaced with 'the excerpt'.
Reports every change; --apply writes (per-lesson prior state re-saved to the
existing tier-examples backup family).
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_example_id_leaks_2026-08-16.json")
UNITS = ["listening-skills", "aos-listening", "western-classical-1650-1910",
         "score-reading"]
CLEAN_INTRO = "<p>Play the excerpt below before reading on, then follow the steps.</p>"


def main():
    sb = get_client()
    subj = [s for s in sb.table("subjects").select("id,slug").execute().data
            if s["slug"] == "music-aqa"][0]["id"]
    units = {u["slug"]: u["id"] for u in sb.table("units").select("id,slug,subject_id")
             .execute().data if u["subject_id"] == subj}

    backup, writes, leaks = {}, [], 0
    for uslug in UNITS:
        rows = sb.table("lessons").select("id,lesson_number,practice_data") \
            .eq("unit_id", units[uslug]).order("lesson_number").execute().data
        for l in rows:
            pd = l["practice_data"]
            ids = [p["id"] for p in pd.get("passages") or []]
            touched = False
            for w in pd.get("worked_examples") or []:
                # the intro is the question's text BEFORE any embedded figure
                cut = len(w["question"])
                for marker in ("<figure", "<div class=\"sv-ap"):
                    k = w["question"].find(marker)
                    if k != -1:
                        cut = min(cut, k)
                intro, rest = w["question"][:cut], w["question"][cut:]
                if any(pid in intro for pid in ids):
                    leaks += 1
                    touched = True
                    print("%s L%d %s INTRO: %r" % (uslug, l["lesson_number"],
                                                   w["difficulty"],
                                                   re.sub(r"<[^>]+>", "", intro)[:90]))
                    w["question"] = CLEAN_INTRO + rest
                for st in w.get("steps") or []:
                    hit = [pid for pid in ids if pid in st.get("content", "")]
                    for pid in hit:
                        leaks += 1
                        touched = True
                        print("%s L%d %s STEP [%s]: id %s -> 'the excerpt'"
                              % (uslug, l["lesson_number"], w["difficulty"],
                                 st.get("label"), pid))
                        st["content"] = st["content"].replace(pid, "the excerpt")
            if touched:
                backup["%s/%d" % (uslug, l["lesson_number"])] = {"id": l["id"]}
                writes.append((l["id"], pd))

    print("\nleaks found: %d in %d lesson(s)" % (leaks, len(writes)))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if writes and not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, pd in writes:
        sb.table("lessons").update({"practice_data": pd}).eq("id", lid).execute()
    print("applied.")


if __name__ == "__main__":
    main()
