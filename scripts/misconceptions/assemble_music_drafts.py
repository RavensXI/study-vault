# -*- coding: utf-8 -*-
"""Assemble the four _music_draft_{unit}.json previews into one readable desk
file for Tom. Joins each draft entry against the live problem so the question
and the wrong option appear in full. DESK ONLY — nothing written to the DB.
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

UNITS = ["western-classical-1650-1910", "score-reading", "listening-skills",
         "aos-listening"]
OUT = os.path.join(HERE, "..", "music-practice",
                   "MC_MISCONCEPTION_DRAFTS_2026-08-15.md")


def txt(x):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", str(x or ""))).strip()


sb = get_client()
subj = [s for s in sb.table("subjects").select("id,slug").execute().data
        if s["slug"] == "music-aqa"][0]["id"]
unit_ids = {u["slug"]: u["id"] for u in sb.table("units").select("id,slug")
            .eq("subject_id", subj).execute().data}

md = io.StringIO()
md.write("# Music MC misconception drafts — desk copy (15 Aug 2026)\n\n")
md.write("Per-distractor diagnoses for every multiple-choice problem in the "
         "four music practice units, in the same format already live for "
         "English Language and MFL (wrong answer picked → named error pattern "
         "→ teacher table). **Drafted only — your ear gates music, so nothing "
         "is in the database.** Approve and I apply with the same script the "
         "other subjects used (backups first).\n\n")

grand = 0
for uslug in UNITS:
    path = os.path.join(HERE, "_music_draft_%s.json" % uslug)
    drafts = json.load(io.open(path, encoding="utf-8"))
    rows = sb.table("lessons").select("id,lesson_number,practice_data") \
        .eq("unit_id", unit_ids[uslug]).execute().data
    lessons = {l["id"]: l["practice_data"] for l in rows}     # draft key = UUID
    num = {l["id"]: l["lesson_number"] for l in rows}
    md.write("\n## %s (%d problems drafted)\n" % (uslug, len(drafts)))
    for d in sorted(drafts, key=lambda x: (num.get(x["lesson"], 99), x["tier"], x["idx"])):
        d["lesson_label"] = num.get(d["lesson"], "?")
        pd = lessons.get(d["lesson"])
        try:
            p = pd["problem_bank"][d["tier"]][d["idx"]]
        except (KeyError, IndexError, TypeError):
            md.write("\n### L%s %s[%s] — ⚠ problem not found (bank may have "
                     "changed since drafting)\n" % (d["lesson_label"], d["tier"], d["idx"]))
            continue
        opts = p.get("options") or []
        correct = p.get("solutions", [None])[0]
        md.write("\n**L%s %s[%s]** — %s\n" % (d["lesson_label"], d["tier"], d["idx"],
                                              txt(p.get("question"))[:200]))
        if isinstance(correct, int) and correct < len(opts):
            md.write("- ✓ correct: %s\n" % txt(opts[correct])[:120])
        for e in d["entries"]:
            i = e.get("expect")
            opt = txt(opts[i])[:120] if isinstance(i, int) and i < len(opts) else "?"
            md.write("- ✗ \"%s\" → `%s` — %s\n" % (opt, e.get("id"), txt(e.get("message"))))
        grand += 1
md.write("\n---\n%d problems drafted in total.\n" % grand)
io.open(OUT, "w", encoding="utf-8").write(md.getvalue())
print("assembled %d problems -> %s" % (grand, OUT))
