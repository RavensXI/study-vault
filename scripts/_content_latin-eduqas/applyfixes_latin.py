# -*- coding: utf-8 -*-
"""Apply the fact-check and quote-gate corrections to the Latin lesson JSONs.

Same contract as the driver's applyfixes stage, with two changes this build
needs: a 64k output cap (the 32k cap truncated a third of the first content
batch, because adaptive thinking bills against it before any JSON is written),
and the subject's house rules carried into the correction prompt so a fix can
never reintroduce a board name, a code or an invented tariff.

    python scripts/_content_latin-eduqas/applyfixes_latin.py fold    # gate -> findings
    python scripts/_content_latin-eduqas/applyfixes_latin.py submit
    python scripts/_content_latin-eduqas/applyfixes_latin.py poll
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts", "api_build"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import driver as D  # noqa: E402

CFG_PATH = os.path.join(HERE, "config_latin-eduqas.json")

SET_TEXT_UNITS = ("heroes-and-villains", "come-dine-with-me",
                  "narratives-livy-and-virgil")

RULES = """
HOUSE RULES that every corrected field must still obey:
- Never name the exam board; never use a specification, paper, component or
  section code. Write "the language paper", "the literature and sources paper",
  "the narratives paper", "the Roman civilisation paper", "your exam".
- Never state a mark tariff, a timing, a question count or a per-objective mark
  split: the specification publishes none for this subject.
- This qualification is not tiered. Never mention Foundation or Higher.
- Latin is written WITHOUT macrons, wrapped in <em> (phrases) or <strong>
  (single words), with the English meaning in plain text after &mdash;.
- The "marks" field of a practice question is the StudyVault rubric string
  (Mastering / Secure / Developing / Emerging), never a number.
- knowledge_checks stay exactly 2 mcq + 2 fill + 1 match in the canonical
  shapes; flashcard answers stay 30 words or fewer, one fact each, no two cards
  sharing an answer.
"""


def stage_fold(cfg):
    """Fold the deterministic quote-gate misses into the findings."""
    gate_path = os.path.join(cfg["run_dir"], "latin_quote_gate.json")
    gate = json.load(io.open(gate_path, encoding="utf-8"))
    fc_path = os.path.join(cfg["run_dir"], "factcheck.json")
    fc = json.load(io.open(fc_path, encoding="utf-8"))
    fc["findings"] = [f for f in fc["findings"] if f.get("source") != "quote_gate"]
    added = 0
    for lesson, spans in gate.get("lessons_with_misses", {}).items():
        set_text = any(lesson.startswith(u) for u in SET_TEXT_UNITS)
        for s in spans:
            fc["findings"].append({
                "severity": "high" if set_text else "medium",
                "field": "content_html", "lesson": lesson, "source": "quote_gate",
                "claim": s,
                "problem": ("This emphasised span does not appear verbatim in any "
                            "of the published booklets for this lesson's material."),
                "correction": (
                    "If this is presented as a quotation from the set text, replace "
                    "it with the exact wording from the booklet, or mark the omission "
                    "with an ellipsis. If it is a Latin technical term rather than a "
                    "quotation, keep it but make sure the form and the definition are "
                    "correct. If it is ordinary English emphasis, leave it alone."),
            })
            added += 1
    counts = {"high": 0, "medium": 0, "low": 0}
    for f in fc["findings"]:
        counts[f.get("severity", "low")] = counts.get(f.get("severity", "low"), 0) + 1
    fc["counts"] = counts
    D.write_json(fc_path, fc)
    print("folded %d quote-gate misses; totals HIGH=%d MED=%d LOW=%d (%d findings)"
          % (added, counts["high"], counts["medium"], counts["low"], len(fc["findings"])))


def stage_submit(cfg):
    st = D.load_state(cfg)
    report = json.load(io.open(os.path.join(cfg["run_dir"], "factcheck.json"),
                               encoding="utf-8"))
    by_lesson = {}
    for f in report["findings"]:
        if f.get("severity") in ("high", "medium"):
            by_lesson.setdefault(f["lesson"], []).append(f)
    if not by_lesson:
        print("no HIGH/MEDIUM findings — nothing to apply")
        return
    lessons_dir = os.path.join(cfg["run_dir"], "lessons")
    reqs = []
    for cid, fl in sorted(by_lesson.items()):
        obj = json.load(io.open(os.path.join(lessons_dir, cid + ".json"), encoding="utf-8"))
        user = ("Apply ONLY the corrections below to this GCSE Latin lesson JSON. "
                "Change nothing else — no rewrites, no restructuring, no new "
                "narration IDs unless a correction forces one. Keep every "
                "data-narration-id sequence intact and gapless.\n"
                + RULES +
                "\nCORRECTIONS:\n%s\n\nLESSON JSON:\n%s\n\n"
                "Return the complete corrected lesson JSON only, no code fences."
                % (json.dumps(fl, ensure_ascii=False), json.dumps(obj, ensure_ascii=False)))
        p = {"model": D.MODEL_CONTENT, "max_tokens": 64000,
             "messages": [{"role": "user", "content": user}]}
        if st.get("use_structured", True):
            p = D.try_structured(p)
        reqs.append({"custom_id": cid, "params": p})
    batch = D.client().messages.batches.create(requests=reqs)
    st["applyfix_batch_id"] = batch.id
    D.save_state(cfg, st)
    print("applyfixes batch submitted: %s (%d lessons, %d corrections)"
          % (batch.id, len(reqs), sum(len(v) for v in by_lesson.values())))


def stage_poll(cfg):
    D.stage_pollapplyfixes(cfg)


def main():
    cfg = D.load_config(CFG_PATH)
    stage = sys.argv[1] if len(sys.argv) > 1 else "submit"
    {"fold": stage_fold, "submit": stage_submit, "poll": stage_poll}[stage](cfg)


if __name__ == "__main__":
    main()
