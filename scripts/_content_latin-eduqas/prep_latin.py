# -*- coding: utf-8 -*-
"""Phase 3 prep for GCSE Latin article lessons.

Writes requests_content.json in the driver's run dir, in exactly the shape
`driver.py submit` expects. Differs from the driver's own `prep` stage in one
way that matters for this subject: the literature and civilisation lessons each
carry the awarding body's own published booklet text for their set material, so
the agent never has to recall a passage from memory. The language-paper lessons
carry no booklet (the language component is unseen).

Usage: python scripts/_content_latin-eduqas/prep_latin.py
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

# Per-unit source bundles, keyed by unit slug, then by lesson number where a
# unit's lessons need different material. "*" applies to every lesson.
BUNDLES = {
    "heroes-and-villains": {"*": [
        "comp2_heroes_and_villains",            # the prescription itself
        "comp2_heroes_student_booklet",         # Latin text with vocabulary help
        "comp2_heroes_translation",             # parallel English translation
        "comp2_heroes_notes_commentary",        # the board's own commentary
    ]},
    "come-dine-with-me": {"*": [
        "comp2_come_dine_with_me",
        "comp2_come_dine_student_booklet",
        "comp2_come_dine_translation",
        "comp2_come_dine_notes_commentary",
    ]},
    "narratives-livy-and-virgil": {
        1: ["comp3a_livy_hannibal", "comp3a_livy_hannibal_student_booklet",
            "comp3a_livy_hannibal_translation",
            "comp3a_livy_hannibal_notes_commentary"],
        2: ["comp3a_livy_hannibal", "comp3a_livy_hannibal_student_booklet",
            "comp3a_livy_hannibal_translation",
            "comp3a_livy_hannibal_notes_commentary"],
        3: ["comp3a_virgil_hercules_cacus",
            "comp3a_virgil_hercules_cacus_student_booklet",
            "comp3a_virgil_hercules_cacus_translation",
            "comp3a_virgil_hercules_cacus_notes_commentary"],
        4: ["comp3a_virgil_hercules_cacus",
            "comp3a_virgil_hercules_cacus_student_booklet",
            "comp3a_virgil_hercules_cacus_translation",
            "comp3a_virgil_hercules_cacus_notes_commentary",
            "comp3a_livy_hannibal_translation"],
    },
    "roman-civilisation": {
        1: ["comp3b_slavery"], 2: ["comp3b_slavery"], 3: ["comp3b_slavery"],
        4: ["comp3b_festivals"], 5: ["comp3b_festivals"], 6: ["comp3b_festivals"],
    },
}

REMINDER = """
HOUSE RULES REMINDER (these override anything in the reference lesson):
- Never name the exam board and never use a specification, paper, component or
  section code anywhere. Write "the exam board", "the specification", "your
  exam", "this paper", "the language paper", "the literature and sources
  paper", "the narratives paper", "the Roman civilisation paper".
- Never invent a mark tariff, a timing, a question count or a per-objective
  mark split. The specification publishes none for this subject.
- This qualification is NOT tiered: no <div class="higher-only">, never mention
  Foundation or Higher.
- Free tier: no <!-- DIAGRAM --> placeholder, no diagram_prompt, no
  diagram_style.
- Wrap every Latin word or phrase in <em> (phrases and sentences) or <strong>
  (single words and forms), with the English meaning in plain text after an
  em dash entity. Put paradigm and vocabulary lists in <ul> with one pair per
  <li>, each <li> carrying its own data-narration-id.
- Write Latin WITHOUT macrons, matching the defined vocabulary list.
- The "marks" field of each practice question is the StudyVault rubric as a
  string (Mastering / Secure / Developing / Emerging), never a number.
- practice_questions: exactly 6, each "type" exactly matching one of the
  registered question type names.
- knowledge_checks: exactly 5, exactly 2 "mcq" + 2 "fill" + 1 "match", in the
  canonical shapes (mcq and fill carry "options" plus the integer "correct";
  match carries "left", "right", "order").
- flashcard_questions: 10-14 cards, each answer 30 words or fewer, no two cards
  sharing an answer, no list answers.
"""

SOURCE_RULE = """
SET MATERIAL FOR THIS LESSON

The documents below are the awarding body's own published booklets for the
material this lesson teaches. They are the ONLY permitted source for Latin
quotations, line references, plot detail and character detail.

- Every Latin phrase you put in quotation marks or in <em>/<strong> must appear
  VERBATIM in the booklet text below. If you cannot find it there, paraphrase in
  English instead — never reconstruct a line from memory.
- Keep quotations short (a few words to one line) and always gloss them in
  English immediately afterwards.
- Do not teach any text, author, topic or example that is not in these
  documents or in the specification extract.
- The English translations supplied are the board's own; use them to explain
  meaning, but write your own prose rather than copying whole sentences.
"""


def read_source(cfg, name):
    path = os.path.join(cfg["source_dir"], name + ".md")
    return D.read(path)


def bundle_for(unit_slug, lesson_number):
    b = BUNDLES.get(unit_slug)
    if not b:
        return []
    if "*" in b:
        return b["*"]
    return b.get(lesson_number, [])


def main():
    cfg = D.load_config(CFG_PATH)
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    system = D.shared_system_blocks(cfg, plan)
    # Batch requests run in parallel, so cache markers on a batched prefix lose
    # money more often than they save it — strip them (same reasoning as the
    # driver's own prep stage).
    system = [{k: v for k, v in blk.items() if k != "cache_control"} for blk in system]

    requests = []
    for u in plan["article_units"]:
        for l in u["lessons"]:
            names = bundle_for(u["slug"], l["number"])
            src = ""
            if names:
                parts = []
                for n in names:
                    parts.append("<document name=\"%s\">\n%s\n</document>"
                                 % (n, read_source(cfg, n)))
                src = SOURCE_RULE + "\n" + "\n\n".join(parts) + "\n"
            user = (
                "UNIT: %s — %s\nUNIT ACCENT COLOUR: %s\n"
                "LESSON %d of %d: %s\n"
                "PLANNED DESCRIPTION (refine to 60-100 chars if needed): %s\n"
                "SPEC REFERENCES: %s\n"
                "SECTION MARKERS (find these in the specification extract above; "
                "they scope THIS lesson's content): %s\n"
                "%s%s\nGenerate the complete lesson as a JSON object."
            ) % (u["name"], u.get("subtitle", ""), u["accent"],
                 l["number"], len(u["lessons"]), l["title"],
                 l.get("description", ""),
                 json.dumps(l.get("spec_references", []), ensure_ascii=False),
                 json.dumps(l.get("section_markers", []), ensure_ascii=False),
                 src, REMINDER)
            requests.append({
                "custom_id": D.lesson_key(u["slug"], l["number"]),
                "params": {
                    "model": D.MODEL_CONTENT,
                    "max_tokens": 32000,
                    "system": system,
                    "messages": [{"role": "user", "content": user}],
                },
            })

    D.write_json(os.path.join(cfg["run_dir"], "requests_content.json"), requests)
    total_sys = sum(len(b["text"]) for b in system)
    print("prepped %d article content requests" % len(requests))
    print("shared system prefix: %dk chars" % (total_sys // 1000))
    for r in requests:
        print("  %-28s user %6dk chars"
              % (r["custom_id"], len(r["params"]["messages"][0]["content"]) // 1000))


if __name__ == "__main__":
    main()
