# -*- coding: utf-8 -*-
"""Machine audit of all 165 drill questions.

I cannot hear the excerpts, so I cannot confirm that "the answer is plagal" is
musically true — that stays an ear-check for Tom. What I CAN do is catch the
faults that need no ears: an index pointing at the wrong option, duplicate or
overlapping options, an explanation that names a different answer from the key,
a question with no explanation, or a passage_id that does not exist.
"""
import sys, json, re, difflib
sys.path.insert(0, r"C:\Users\tshau\Documents\Study Vault\scripts")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client
sb = get_client()

UNITS = ["western-classical-1650-1910", "aos-listening", "listening-skills", "score-reading"]
strip = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()

findings = []
total = 0
for slug in UNITS:
    u = [x for x in sb.table("units").select("id,slug").execute().data if x["slug"] == slug][0]
    for l in sb.table("lessons").select("lesson_number,title,practice_data") \
            .eq("unit_id", u["id"]).order("lesson_number").execute().data:
        pd = l["practice_data"] or {}
        pids = set(p.get("id") for p in (pd.get("passages") or []))
        bank = pd.get("problem_bank") or {}
        for tier in ("bronze", "silver", "gold"):
            for qi, q in enumerate(bank.get(tier) or [], 1):
                total += 1
                where = "%s L%-2d %-6s Q%d" % (slug[:26], l["lesson_number"], tier, qi)
                qt = strip(q.get("question"))
                opts = q.get("options") or []
                sols = q.get("solutions")
                expl = strip(q.get("explanation"))

                if q.get("passage_id") and q["passage_id"] not in pids:
                    findings.append((where, "passage_id not in this lesson: %s" % q["passage_id"]))

                if q.get("input_type") == "multiple_choice":
                    if not isinstance(sols, list) or len(sols) != 1:
                        findings.append((where, "expected exactly one solution index, got %r" % (sols,)))
                    else:
                        s = sols[0]
                        if not isinstance(s, int) or s < 0 or s >= len(opts):
                            findings.append((where, "solution index %r out of range for %d options" % (s, len(opts))))
                        else:
                            key = strip(opts[s])
                            # explanation should not assert a DIFFERENT option
                            if expl:
                                others = [strip(o) for j, o in enumerate(opts) if j != s]
                                el = expl.lower()
                                named = [o for o in others if len(o) > 12 and o.lower() in el]
                                if named and key.lower() not in el:
                                    findings.append((where, "explanation names a non-key option (%r) and never the key (%r)"
                                                     % (named[0][:50], key[:50])))
                    low = [strip(o).lower() for o in opts]
                    if len(set(low)) != len(low):
                        findings.append((where, "duplicate options"))
                    for i in range(len(low)):
                        for j in range(i + 1, len(low)):
                            if low[i] and low[j] and difflib.SequenceMatcher(None, low[i], low[j]).ratio() > 0.90:
                                findings.append((where, "near-identical options: %r / %r" % (low[i][:45], low[j][:45])))
                    if len(opts) < 3:
                        findings.append((where, "only %d options" % len(opts)))

                if not expl:
                    findings.append((where, "no explanation — student gets no feedback when wrong"))
                if not qt:
                    findings.append((where, "empty question text"))

print("questions audited:", total)
print("findings:", len(findings))
print()
for w, f in findings:
    print("  %-34s %s" % (w, f))
