# -*- coding: utf-8 -*-
"""Latin-accuracy check over the practice banks.

The pipeline normally skips fact-checking for practice-format subjects, because
maths and language drills are checked by their own QA scripts. Latin is the
case that argues for an exception: 240 problems of composed Latin, every one of
which a student will take as a model of correct usage. A wrong ending, a wrong
case after a preposition, or a mislabelled clause is taught as fact.

Opus checks each lesson's whole bank against the specification's own accidence
and syntax list and against the defined vocabulary slice the lesson owns, then
`apply` rewrites only the problems it flags.

    python scripts/_content_latin-eduqas/factcheck_practice_latin.py submit
    python scripts/_content_latin-eduqas/factcheck_practice_latin.py poll
    python scripts/_content_latin-eduqas/factcheck_practice_latin.py apply
    python scripts/_content_latin-eduqas/factcheck_practice_latin.py pollapply
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts", "api_build"))
sys.path.insert(0, HERE)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import driver as D  # noqa: E402
import practice_latin as P  # noqa: E402

CFG_PATH = os.path.join(HERE, "config_latin-eduqas.json")

SYSTEM = """You are checking a GCSE Latin practice lesson before publication. Every Latin word in it is a model a fifteen-year-old will copy, so an error here is taught as fact.

CHECK EVERY PIECE OF LATIN in the JSON you are given — in problems, answers, accepted answers, word banks, distractors, explanations, worked examples, the method card, and the translations attached to each sentence.

Flag as HIGH:
- a wrongly formed Latin word: wrong case ending, wrong number, wrong gender, wrong tense, wrong person, wrong conjugation or declension pattern
- an adjective that does not agree with its noun in case, number and gender
- a preposition governing the wrong case
- a verb given the wrong principal parts, or a deponent treated as active in form
- an English translation or gloss that does not match the Latin
- a wrong grammatical label: calling a perfect a pluperfect, an ablative an accusative, a purpose clause a result clause, a complementary infinitive a historic infinitive
- a `spot_correct` problem whose sentence contains MORE than one error, or whose stated `error_word` is not actually wrong, or whose `correction` is itself wrong
- a `sentence_builder` or `reorder` whose `correct_order` does not produce grammatical Latin
- a `gap_fill` whose stated answer does not fit the sentence, or whose `wrong` explanation misdescribes the wrong form
- a `vocab_match` pair whose English is not a meaning the defined vocabulary list gives for that word
- an English-into-Latin (`direction: to_target`) problem that breaks the specification's restrictions for that question: it must be a single clause, third person singular or plural, present, imperfect or perfect indicative active, first conjugation verbs only, first and second declension nouns and adjectives only, nominative and accusative only

Flag as MEDIUM:
- Latin that is grammatically possible but unidiomatic or misleading for a beginner
- a macron anywhere (this subject's house style is without macrons)
- a claim about the exam that the assessment rules do not state, including any invented mark tariff, timing or question count
- an explanation that is correct but would confuse a student at this level

Flag as LOW: minor imprecision unlikely to cost marks.

DO NOT flag: simplification that is appropriate for GCSE, style preferences, word-order choices that are legitimate Latin, or the absence of macrons.

VOCABULARY: the lesson's own slice of the defined vocabulary list is supplied. A word from outside the whole 440-word list may be used only if it is glossed for the student; flag an unglossed outside word as MEDIUM.

Return ONLY a JSON object, no code fences:
{
  "findings": [
    {
      "severity": "high" | "medium" | "low",
      "location": "problem_bank.silver[2]" or "worked_examples[0]" or "method_card",
      "claim": "the exact text that is wrong",
      "problem": "what is wrong",
      "correction": "the corrected text, ready to substitute"
    }
  ]
}
An empty findings array means the lesson verified clean."""


def stage_submit(cfg):
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    data = json.load(io.open(os.path.join(cfg["run_dir"], "practice_data.json"),
                             encoding="utf-8"))
    spec = D.read(cfg["spec_md"])
    reqs = []
    for u, l in P.practice_lessons(plan):
        cid = D.lesson_key(u["slug"], l["number"])
        if cid not in data:
            continue
        words = P.lesson_words(cfg, u["slug"], l["number"])
        slice_txt = ""
        if words:
            slice_txt = ("\nTHIS LESSON'S VOCABULARY SLICE:\n"
                         + "\n".join("%s = %s" % (w["latin"], w["english"])
                                     for w in words))
        user = ("LESSON: %s — unit \"%s\", lesson %d: %s\nWHAT IT DRILLS: %s\n%s\n\n"
                "PRACTICE JSON:\n%s\n\nCheck it. Return the findings JSON."
                % (cid, u["name"], l["number"], l["title"],
                   "; ".join(l.get("section_markers", [])), slice_txt,
                   json.dumps(data[cid], ensure_ascii=False)))
        reqs.append({"custom_id": cid, "params": {
            "model": D.MODEL_FACTCHECK, "max_tokens": 24000,
            "system": [{"type": "text", "text": SYSTEM},
                       {"type": "text",
                        "text": "THE SPECIFICATION, ITS ACCIDENCE AND SYNTAX LIST, "
                                "AND THE COMPLETE DEFINED VOCABULARY LISTS:\n" + spec,
                        "cache_control": {"type": "ephemeral", "ttl": "1h"}}],
            "messages": [{"role": "user", "content": user}],
        }})
    batch = D.client().messages.batches.create(requests=reqs)
    st = D.load_state(cfg)
    st["practice_fc_batch"] = batch.id
    D.save_state(cfg, st)
    print("practice fact-check batch submitted: %s (%d lessons)" % (batch.id, len(reqs)))


def stage_poll(cfg):
    st = D.load_state(cfg)
    out = D.collect_batch(cfg, st["practice_fc_batch"], "practice-factcheck",
                          "raw_practice_fc")
    if out is None:
        return
    texts, errors = out
    findings, bad = {}, {}
    for cid, t in sorted(texts.items()):
        try:
            findings[cid] = D.parse_json_reply(t).get("findings", [])
        except Exception as e:
            bad[cid] = str(e)
    counts = {"high": 0, "medium": 0, "low": 0}
    for cid, fl in findings.items():
        for f in fl:
            counts[f.get("severity", "low")] = counts.get(f.get("severity", "low"), 0) + 1
    D.write_json(os.path.join(cfg["run_dir"], "practice_factcheck.json"),
                 {"counts": counts, "findings": findings, "unparsed": bad})
    print("practice fact-check: HIGH=%d MED=%d LOW=%d across %d lessons%s"
          % (counts["high"], counts["medium"], counts["low"], len(findings),
             (" — UNPARSED: %s" % list(bad)) if bad else ""))
    for cid, fl in sorted(findings.items()):
        hi = [f for f in fl if f.get("severity") == "high"]
        if hi:
            print("  %s: %d HIGH" % (cid, len(hi)))
            for f in hi[:4]:
                print("     -", (f.get("problem") or "")[:150])


def stage_apply(cfg):
    st = D.load_state(cfg)
    report = json.load(io.open(os.path.join(cfg["run_dir"], "practice_factcheck.json"),
                               encoding="utf-8"))
    data = json.load(io.open(os.path.join(cfg["run_dir"], "practice_data.json"),
                             encoding="utf-8"))
    reqs = []
    for cid, fl in sorted(report["findings"].items()):
        fl = [f for f in fl if f.get("severity") in ("high", "medium")]
        if not fl:
            continue
        user = ("Apply ONLY the corrections below to this GCSE Latin practice JSON. "
                "Change nothing else: same keys, same problem order, same tier "
                "counts (8 Bronze, 6 Silver, 6 Gold), same input_type on every "
                "problem, same three worked examples with the final step still "
                "carrying \"isAnswer\": true.\n\n"
                "House rules the result must still obey: no exam board name, no "
                "specification, paper, component or section code, no invented mark "
                "tariff or timing, no Foundation or Higher tier, Latin without "
                "macrons, and the dictation and role_play input types are banned.\n\n"
                "CORRECTIONS:\n%s\n\nPRACTICE JSON:\n%s\n\n"
                "Return the complete corrected JSON only, no code fences."
                % (json.dumps(fl, ensure_ascii=False),
                   json.dumps(data[cid], ensure_ascii=False)))
        reqs.append({"custom_id": cid, "params": {
            "model": D.MODEL_CONTENT, "max_tokens": 64000,
            "messages": [{"role": "user", "content": user}]}})
    if not reqs:
        print("no HIGH/MEDIUM practice findings — nothing to apply")
        return
    batch = D.client().messages.batches.create(requests=reqs)
    st["practice_applyfix_batch"] = batch.id
    D.save_state(cfg, st)
    print("practice applyfixes batch submitted: %s (%d lessons)" % (batch.id, len(reqs)))


def stage_pollapply(cfg):
    st = D.load_state(cfg)
    out = D.collect_batch(cfg, st["practice_applyfix_batch"], "practice-applyfixes",
                          "raw_practice_applyfix")
    if out is None:
        return
    texts, errors = out
    path = os.path.join(cfg["run_dir"], "practice_data.json")
    data = json.load(io.open(path, encoding="utf-8"))
    ok, bad = 0, {}
    for cid, t in sorted(texts.items()):
        try:
            obj = D.parse_json_reply(t)
        except Exception as e:
            bad[cid] = "parse: %s" % e
            continue
        probs = []
        for tier, want in P.TIER_TARGET.items():
            got = len((obj.get("problem_bank") or {}).get(tier) or [])
            if got != want:
                probs.append("%s %d != %d" % (tier, got, want))
            for i, p in enumerate((obj["problem_bank"][tier] if not probs else [])):
                probs += ["%s[%d] %s" % (tier, i, x) for x in P.check_problem(p)]
        if probs:
            bad[cid] = probs[:6]
            continue
        data[cid] = obj
        ok += 1
    D.write_json(path, data)
    print("practice fixes applied to %d lessons; %d rejected %s"
          % (ok, len(bad), bad or ""))
    if errors:
        print("errored:", errors)


def main():
    cfg = D.load_config(CFG_PATH)
    stage = sys.argv[1] if len(sys.argv) > 1 else "submit"
    {"submit": stage_submit, "poll": stage_poll,
     "apply": stage_apply, "pollapply": stage_pollapply}[stage](cfg)


if __name__ == "__main__":
    main()
