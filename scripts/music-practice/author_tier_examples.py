# -*- coding: utf-8 -*-
"""Per-tier worked examples for the music practice lessons (Tom, 16 Aug:
"dont bother with the interim, lets just fix it now").

The failed-tier interstitial re-teaches the wrong topic because each music
lesson carries ONE example while its tiers test different skills. This
authors bronze/silver/gold examples per lesson, each walking the DECISION
for a skill that tier actually tests, embedding an existing excerpt player
from the lesson — no outside sourcing, and every musical claim must come
from the lesson's own explanations (rule enforced in the prompt; outputs
validated and reviewed, then Tom's review pass covers them like the rest of
the pending content).

score-reading keeps its purpose-built bronze examples; it gains silver+gold.
Other units are replaced wholesale with the authored set of three.

Run: python author_tier_examples.py [--apply]   (~18 model calls, ~$1)
Backup: _backup_tier_examples_2026-08-16.json
"""
import io
import json
import os
import re
import sys

import anthropic

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_tier_examples_2026-08-16.json")
MODEL = "claude-sonnet-5"
UNITS = ["listening-skills", "aos-listening", "western-classical-1650-1910",
         "score-reading"]
TAGS = re.compile(r"<[^>]+>")


def plain(s):
    return re.sub(r"\s+", " ", TAGS.sub(" ", s or "")).strip()


SYSTEM = """You write worked examples for GCSE Music listening practice.

A worked example walks a student through HOW TO DECIDE — the reasoning a
musician uses — for one problem type, in numbered steps.

HARD RULES:
- Every musical claim must come from the provided problem explanations or
  method card. Invent NOTHING about any recording. If a fact is not in the
  provided material, do not state it.
- 3 to 5 steps. Each step: a short label and one or two sentences. The last
  step's label is "Answer".
- Steps teach the DECISION (what to listen for first, what rules it out),
  not just the fact.
- British English. Never name an exam board. Never say "again" or refer to
  previous attempts. No HTML beyond <p>, <strong>, <em> in step content.
- The intro tells the student to play the excerpt before reading on (when an
  excerpt is referenced).

Return ONLY a JSON array of exactly the requested examples:
[{"difficulty": "bronze", "intro": "...", "passage_ref": "id-or-null",
  "steps": [{"label": "...", "content": "<p>...</p>"}]}]
passage_ref must be one of the listed passage ids (pick the one the chosen
problem uses) or null. Each example must walk a skill ITS OWN tier tests,
chosen from that tier's problem list."""


def lesson_brief(pd, title, want):
    lines = ["LESSON: " + title,
             "METHOD CARD: " + plain((pd.get("method_card") or {}).get("content"))[:900]]
    ids = [p["id"] for p in pd.get("passages") or []]
    lines.append("PASSAGE IDS: " + ", ".join(ids))
    for tier in want:
        lines.append("\n%s TIER PROBLEMS:" % tier.upper())
        for p in (pd.get("problem_bank") or {}).get(tier, []):
            opts = p.get("options") or []
            sol = (p.get("solutions") or [None])[0]
            ans = opts[sol] if isinstance(sol, int) and sol < len(opts) else ""
            lines.append("- Q: %s | passage: %s | answer: %s | explanation: %s"
                         % (plain(p.get("question"))[:110], p.get("passage_id"),
                            plain(ans)[:60], plain(p.get("explanation"))[:260]))
    lines.append("\nWrite exactly %d example(s), difficulties: %s."
                 % (len(want), ", ".join(want)))
    return "\n".join(lines)


def validate(examples, want, passage_ids):
    errs = []
    if [e.get("difficulty") for e in examples] != want:
        errs.append("difficulties wrong: %s" % [e.get("difficulty") for e in examples])
    for e in examples:
        ref = e.get("passage_ref")
        if ref and ref not in passage_ids:
            errs.append("%s: unknown passage %s" % (e.get("difficulty"), ref))
        steps = e.get("steps") or []
        if not (3 <= len(steps) <= 5):
            errs.append("%s: %d steps" % (e.get("difficulty"), len(steps)))
        elif steps[-1].get("label", "").lower() != "answer":
            errs.append("%s: last step not Answer" % e.get("difficulty"))
        blob = json.dumps(e)
        if re.search(r"<(script|img|iframe)", blob, re.I):
            errs.append("%s: forbidden markup" % e.get("difficulty"))
        if re.search(r"(?i)\b(AQA|Edexcel|OCR|Eduqas|WJEC)\b", blob):
            errs.append("%s: board name" % e.get("difficulty"))
        if not plain(e.get("intro")):
            errs.append("%s: empty intro" % e.get("difficulty"))
    return errs


def assemble(example, passages):
    q = "<p>" + plain(example["intro"]) + "</p>"
    ref = example.get("passage_ref")
    if ref:
        p = next((x for x in passages if x["id"] == ref), None)
        if p:
            q += p["text"]
    return {"difficulty": example["difficulty"], "question": q,
            "steps": example["steps"]}


def main():
    sb = get_client()
    cl = anthropic.Anthropic()
    subj = [s for s in sb.table("subjects").select("id,slug").execute().data
            if s["slug"] == "music-aqa"][0]["id"]
    units = {u["slug"]: u["id"] for u in sb.table("units").select("id,slug,subject_id")
             .execute().data if u["subject_id"] == subj}

    backup, writes = {}, []
    cost_in = cost_out = 0
    for uslug in UNITS:
        rows = sb.table("lessons").select("id,lesson_number,title,practice_data") \
            .eq("unit_id", units[uslug]).order("lesson_number").execute().data
        for l in rows:
            pd = l["practice_data"]
            keep = []
            want = ["bronze", "silver", "gold"]
            if uslug == "score-reading":
                keep = [w for w in (pd.get("worked_examples") or [])
                        if (w.get("difficulty") or "").lower() == "bronze"][:1]
                want = ["silver", "gold"]
            brief = lesson_brief(pd, l["title"], want)
            r = cl.messages.create(model=MODEL, max_tokens=4000, system=SYSTEM,
                                   messages=[{"role": "user", "content": brief}])
            cost_in += r.usage.input_tokens
            cost_out += r.usage.output_tokens
            text = "".join(getattr(b, "text", "") or "" for b in r.content)
            m = re.search(r"\[[\s\S]*\]", text)
            if not m:
                print("%s L%d: NO JSON — skipped" % (uslug, l["lesson_number"]))
                continue
            try:
                examples = json.loads(m.group(0))
            except ValueError:
                print("%s L%d: JSON parse failed — skipped" % (uslug, l["lesson_number"]))
                continue
            ids = {p["id"] for p in pd.get("passages") or []}
            errs = validate(examples, want, ids)
            if errs:
                print("%s L%d: REJECTED — %s" % (uslug, l["lesson_number"], "; ".join(errs)))
                continue
            new_we = keep + [assemble(e, pd.get("passages") or []) for e in examples]
            print("%s L%d: %s" % (uslug, l["lesson_number"],
                                  ", ".join("%s (%s, %d steps)" % (
                                      e["difficulty"], e.get("passage_ref") or "no excerpt",
                                      len(e["steps"])) for e in examples)))
            backup["%s/%d" % (uslug, l["lesson_number"])] = {
                "id": l["id"], "worked_examples": pd.get("worked_examples")}
            pd["worked_examples"] = new_we
            writes.append((l["id"], pd))

    print("\nlessons authored: %d | tokens %d in / %d out | cost ~$%.2f"
          % (len(writes), cost_in, cost_out,
             cost_in / 1e6 * 2 + cost_out / 1e6 * 10))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, pd in writes:
        sb.table("lessons").update({"practice_data": pd}).eq("id", lid).execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
