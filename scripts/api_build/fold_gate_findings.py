# -*- coding: utf-8 -*-
"""Fold quote-gate misses into a run's factcheck.json as findings.

Split out of run_drama_play.py so the same fold can be applied to a run whose
stages were driven by hand (as happened on 8-9 September 2026, when a stalled
batch queue meant the plays were advanced stage by stage rather than by the
orchestrator).

A miss is a span the lesson placed inside quotation marks that does not appear
in the play's quotable-span corpus. That is not automatically a fabrication:
lessons legitimately quote their own scene labels, scare-quotes and examples of
weak student phrasing. So the finding asks the fixer to judge the span first,
and to leave the lesson's own wording alone.

Usage: python scripts/api_build/fold_gate_findings.py <config.json> <gate_report.json>
"""
import io
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROBLEM = ("This span is inside quotation marks in the lesson but does not appear in the "
           "source bank's list of quotable spans. The play is in copyright and the source "
           "bank is the only authority for its wording, so no unverified wording may be "
           "presented as the playwright's words.")

CORRECTION = (
    "JUDGE THE SPAN FIRST. If the lesson presents it as words spoken or written in the play "
    "— dialogue, a stage direction, a song lyric, a line attributed to a character — remove "
    "the quotation marks and rewrite the sentence as paraphrase, keeping its teaching point, "
    "and do NOT substitute a different quotation unless that one is on the quotable-span "
    "list. If instead it is the lesson's OWN wording — a scene label, a scare-quote, an "
    "example of a weak student phrase, a term being defined, a hypothetical line of an "
    "answer — then it is not a quotation from the play and you must LEAVE IT EXACTLY AS IT "
    "IS. Never add a caveat, apology or note about sources: the student must not see one.")


def main(cfg_path, gate_path):
    cfg = json.load(io.open(cfg_path, encoding="utf-8"))
    fc_path = cfg["run_dir"] + "\\factcheck.json"
    fc = json.load(io.open(fc_path, encoding="utf-8"))
    if fc.get("_gate_folded"):
        print("already folded — nothing to do")
        return
    gate = json.load(io.open(gate_path, encoding="utf-8"))
    added = 0
    for lesson, spans in gate.get("lessons_with_misses", {}).items():
        for s in spans:
            fc["findings"].append({
                "severity": "medium", "field": "content_html", "lesson": lesson,
                "claim": s, "problem": PROBLEM, "correction": CORRECTION,
                "source": "quote_gate",
            })
            added += 1
    fc["_gate_folded"] = True
    counts = {"high": 0, "medium": 0, "low": 0}
    for f in fc["findings"]:
        counts[f.get("severity", "low")] = counts.get(f.get("severity", "low"), 0) + 1
    fc["counts"] = counts
    io.open(fc_path, "w", encoding="utf-8").write(
        json.dumps(fc, ensure_ascii=False, indent=1))
    print("folded %d quote-gate misses; factcheck.json now HIGH=%d MED=%d LOW=%d"
          % (added, counts["high"], counts["medium"], counts["low"]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
