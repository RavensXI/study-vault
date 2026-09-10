# -*- coding: utf-8 -*-
"""Phase 4 fact-check for the GCSE Latin article lessons.

Same checker prompt and same output contract as the driver's own factcheck
stage, with one change that matters here: each lesson is checked against ONLY
the booklets that cover its own set material, instead of one enormous shared
corpus attached to every request. That keeps the quotation authority exact
(a Livy lesson is never judged against Virgil's text) and keeps the bill down.

Lessons in the language unit get no source text: that component is unseen, so
their illustrative Latin is composed rather than quoted, and the checker is
told to judge it as composed Latin.

Usage:
    python scripts/_content_latin-eduqas/factcheck_latin.py submit
    python scripts/_content_latin-eduqas/factcheck_latin.py poll
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

CORPUS = {
    "heroes-and-villains": {"*": ["comp2_heroes_and_villains",
                                  "comp2_heroes_student_booklet",
                                  "comp2_heroes_translation"]},
    "come-dine-with-me": {"*": ["comp2_come_dine_with_me",
                                "comp2_come_dine_student_booklet",
                                "comp2_come_dine_translation"]},
    "narratives-livy-and-virgil": {
        1: ["comp3a_livy_hannibal", "comp3a_livy_hannibal_translation"],
        2: ["comp3a_livy_hannibal", "comp3a_livy_hannibal_translation"],
        3: ["comp3a_virgil_hercules_cacus",
            "comp3a_virgil_hercules_cacus_translation"],
        4: ["comp3a_virgil_hercules_cacus",
            "comp3a_virgil_hercules_cacus_translation",
            "comp3a_livy_hannibal_translation"],
    },
    "roman-civilisation": {
        1: ["comp3b_slavery"], 2: ["comp3b_slavery"], 3: ["comp3b_slavery"],
        4: ["comp3b_festivals"], 5: ["comp3b_festivals"], 6: ["comp3b_festivals"],
    },
}

LATIN_RULES = """
SUBJECT-SPECIFIC RULES FOR GCSE LATIN

LATIN ACCURACY. Check every Latin word, phrase and sentence in the lesson:
- Is it correctly formed? Wrong case ending, wrong tense, wrong person, an
  adjective not agreeing with its noun, or a preposition with the wrong case is
  a HIGH finding, because a student will copy it.
- Is the English gloss beside it actually what the Latin means? A mistranslation
  is a HIGH finding.
- Is a claimed grammatical label right? Calling a perfect a pluperfect, an
  ablative an accusative, a purpose clause a result clause: HIGH.
- Latin must be written WITHOUT macrons. Macrons are a MEDIUM finding.

SET TEXTS. Where a SOURCE TEXT document is supplied, it is the awarding body's
own published booklet for this lesson's set material and is the PRIMARY
authority. Any Latin presented as a quotation from the set text must appear
verbatim in it. Any claim about what happens in the narrative, who says what, or
what a picture source shows must be supported by it. A quotation not found in
the booklet is a HIGH finding: supply the nearest real wording as the
correction.

WHERE NO SOURCE TEXT IS SUPPLIED, the lesson belongs to the language component,
which is examined on unseen material. Its Latin is composed for teaching, so do
NOT flag it for being absent from any set text — but DO check that it is
correct Latin, that it uses the defined vocabulary, and that any grammatical
claim about it is right.

SCOPE. The 2027 examination series is the one these students sit. Flag as HIGH
any lesson that teaches the retired prescriptions as though they were assessed:
the themes "Romans in the Countryside" and "Love and Marriage", the narratives
Suetonius "Nero" and Ovid "The Adventures of Perseus", and the Roman
civilisation topics "Roman family life" and "The City of Rome".

BOARD NAMING. This subject's lessons must never name the exam board or use a
specification, paper, component or section code. Report any occurrence of
"Eduqas", "WJEC", "C580QS", "Component 1/2/3", "Section A", "Section B" or
"Paper 1" in student-facing text as a HIGH finding on the field it appears in,
with the neutral wording as the correction.

TIERING. This qualification is not tiered. Any mention of Foundation or Higher
tier is a HIGH finding.
"""


def sources_for(cfg, unit_slug, number):
    spec = CORPUS.get(unit_slug)
    if not spec:
        return []
    names = spec.get("*") or spec.get(number, [])
    return [(n, D.read(os.path.join(cfg["source_dir"], n + ".md"))) for n in names]


def stage_submit(cfg):
    st = D.load_state(cfg)
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    lessons_dir = os.path.join(cfg["run_dir"], "lessons")
    rules = D.assessment_rules_block(cfg)
    scope = cfg.get("scope_statement", "")
    titles = {}
    for u in plan["article_units"]:
        for l in u["lessons"]:
            titles[D.lesson_key(u["slug"], l["number"])] = (u, l)

    cl = D.client()
    reqs = []
    for cid in st.get("content_ok", []):
        if cid not in titles:
            continue
        u, l = titles[cid]
        obj = json.load(io.open(os.path.join(lessons_dir, cid + ".json"), encoding="utf-8"))
        payload = {k: obj.get(k) for k in
                   ("content_html", "exam_tip_html", "conclusion_html",
                    "knowledge_checks", "flashcard_questions", "glossary_terms",
                    "practice_questions")}
        srcs = sources_for(cfg, u["slug"], l["number"])
        system = [{"type": "text", "text": D.FACTCHECK_SYSTEM + "\n" + LATIN_RULES}]
        if srcs:
            system.append({"type": "text", "text":
                           "SOURCE TEXT (primary authority for quotations and "
                           "for what the set material says):\n\n"
                           + "\n\n".join("<document name=\"%s\">\n%s\n</document>"
                                         % (n, t) for n, t in srcs)})
        user = ("LESSON: %s — unit \"%s\", lesson %d: %s\n"
                "TARGET BOARD: GCSE %s. This board publishes no per-question mark "
                "tariffs for this subject, so the registered question type names "
                "carry no marks: %s\n"
                "SCOPE FOR THIS SUBJECT: %s\n\n%s\n%s\n\n"
                "Fact-check this lesson. Return the findings JSON."
                % (cid, u["name"], l["number"], l["title"], cfg["subject_name"],
                   " | ".join(plan.get("question_type_names", [])), scope, rules,
                   json.dumps(payload, ensure_ascii=False)))
        reqs.append({"custom_id": cid, "params": {
            "model": D.MODEL_FACTCHECK, "max_tokens": 8000,
            "tools": [{"type": "web_search_20260209", "name": "web_search",
                       "max_uses": 6}],
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }})
    batch = cl.messages.batches.create(requests=reqs)
    st["factcheck_batch_id"] = batch.id
    D.save_state(cfg, st)
    print("factcheck batch submitted: %s (%d lessons, %d with a source corpus)"
          % (batch.id, len(reqs),
             sum(1 for r in reqs if len(r["params"]["system"]) > 1)))


def stage_poll(cfg):
    D.stage_pollfactcheck(cfg)


def main():
    cfg = D.load_config(CFG_PATH)
    stage = sys.argv[1] if len(sys.argv) > 1 else "submit"
    (stage_submit if stage == "submit" else stage_poll)(cfg)


if __name__ == "__main__":
    main()
