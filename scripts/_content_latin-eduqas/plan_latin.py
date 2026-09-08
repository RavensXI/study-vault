# -*- coding: utf-8 -*-
"""Phase 1 planning call for GCSE Latin (Eduqas / WJEC C580QS), free tier.

This is a FRESH build: no other board offers this subject on the platform, so
the driver's cross-board planning path (which requires a source plan and a
source catalogue) does not apply. This script runs the same PLANNING_PROMPT
system prompt against the spec with grounded web research enabled, mandates the
unit skeleton that the spec's 2027 prescriptions and the article/practice
heuristic imply, and writes plan.json into the driver's run dir so every
downstream driver stage can read it unchanged.

Usage: python scripts/_content_latin-eduqas/plan_latin.py
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "api_build"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import driver as D  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CFG_PATH = os.path.join(HERE, "config_latin-eduqas.json")

UNIT_SKELETON = """
MANDATED UNIT SKELETON — use exactly these units, slugs, formats and lesson
counts. You choose the lesson titles, descriptions, spec_references,
section_markers and the accent palette; you do NOT change the structure.

ARTICLE UNITS (21 lessons)

1. slug `language-paper-method`, 3 lessons — how the language paper works and
   the method for reading, comprehending and translating an unseen Latin
   narrative, plus derivations and the short optional final section (English
   into Latin, or recognising and explaining accidence and syntax). This is the
   only article unit for the language component; the drilling lives in the
   practice units below.

2. slug `heroes-and-villains`, 4 lessons — the literature and sources theme
   examined in 2027. Prescribed texts: Cicero, Philippic 2.118-119 (a
   politician recalls his own bravery); Livy, History 2.10 (Horatius saves
   Rome); Propertius, Elegy 4.6.3-46, 53-60 (divine support for Augustus);
   Sallust, Bellum Catilinae 25 (a badly behaved woman); Tacitus, Annals 4.1
   and 4.59 (a hero or a villain?); Virgil, Aeneid 8.478-495 (a king's gruesome
   behaviour); Virgil, Aeneid 11.648-658, 664-665, 676-689 (the Volscian
   warrior, Camilla). Plus the prescribed picture sources. The theme's three
   stated aspects are: the characteristics of a Roman hero; can women be
   heroes?; Roman anti-heroes. Group the texts so every prescribed text is
   covered and the last lesson handles the picture sources and the extended
   evaluative answer that draws on the whole theme.

3. slug `come-dine-with-me`, 4 lessons — the second literature and sources theme
   examined in 2027. Prescribed texts: Aulus Gellius, Attic Nights 2.24 (Roman
   thrift); Juvenal, Satire 11.64-80 (an old-fashioned meal); Martial, Epigrams
   3.60 (a change of status is not acknowledged); Ovid, Metamorphoses
   1.221-232, 236-239 (a gruesome taste test goes wrong); Ovid, Metamorphoses
   8.664-688 (good hospitality); Petronius, Cena Trimalchionis 31-34, adapted
   (a host displays his wealth); Pliny, Letters 2.6 (how not to treat your
   guests); Seneca, de Clementia 1.18 (a meal for the lampreys). Plus the
   prescribed picture sources. The theme's three stated aspects are: the kind of
   foods eaten in wealthy and in poorer households; the importance of
   hospitality; food as a way to display wealth and power. Same rule: cover
   every prescribed text, and end with the picture sources and the extended
   evaluative answer.

4. slug `narratives-livy-and-virgil`, 4 lessons — the narratives prescription
   examined in 2027: Livy, "Hannibal crosses the Alps" (Livy 21.1, 4, 22, 28,
   32, 35-37, prose) and Virgil, "Hercules and Cacus" (Aeneid 8.152-336,
   verse). Two lessons on each narrative; the last lesson must also cover
   answering the extended evaluative question across a whole narrative and the
   difference between responding to prose and to verse.

5. slug `roman-civilisation`, 6 lessons — the Roman civilisation topics examined
   in 2027: Slavery in the Roman World (3 lessons, covering the five areas of
   study in Appendix C Topic 7) and Roman Festivals and Worship (3 lessons,
   covering the five areas of study in Appendix C Topic 8).

PRACTICE UNITS (12 lessons)

6. slug `vocabulary`, 4 lessons — the 440-word defined vocabulary list, grouped
   into four coherent semantic fields so that every one of the 440 words falls
   into exactly one lesson. State the grouping in each lesson's
   section_markers.

7. slug `accidence`, 5 lessons — the forms listed in Appendix B: nouns of the
   five declensions; verbs (present, future, imperfect); verbs (perfect,
   pluperfect and the irregular verbs sum, possum, eo, fero, volo, nolo);
   passive, deponent and participles; adjectives, adverbs and pronouns
   including comparatives and superlatives.

8. slug `syntax-and-translation`, 3 lessons — the syntax listed in Appendix B:
   uses of the cases, prepositions and expressions of time; subordinate clauses
   (relative, purpose, result, temporal, causal, concessive, conditional);
   indirect statement, question and command with the subjunctive, together with
   the English-into-Latin sentence work the short final section allows.

Total: 33 lessons across 8 units.
"""

EXTRA = """
ADDITIONAL BUILD CONSTRAINTS FOR THIS SUBJECT

- Subject slug MUST be `latin-eduqas`. exam_board MUST be the string
  "Eduqas / WJEC". spec_code "C580QS". school_id null. subject_type
  "full-gcse-100-exam".
- This is a FRESH build. No other board offers Latin on the platform, so there
  is no existing_board_plan: OMIT `content_transfer` blocks entirely, set
  `baseline_transferability` to "unique", and leave `unique_to_source` and
  `unique_to_target` as empty arrays.
- This subject is MIXED format. Return BOTH `article_units` and
  `practice_units`, each in the schema given above. Every unit needs slug, name,
  subtitle, body_class, accent, accent_light, accent_badge, lesson_count,
  sort_order and lessons. body_class is `unit-latin-N` where N is sort_order.
  sort_order runs 1-8 in the order the skeleton lists them.
- accent_badge MUST be accent + "33" (9 characters, lower-case hex). A palette
  drawn from Roman fresco and mosaic colours suits this subject: deep reds,
  ochres, bronze, olive, indigo, terracotta. Do not use the same accent twice.
- The 2027 examination series is the one our students sit. Plan ONLY the 2027
  prescriptions. Never plan a lesson on the 2024-2026 themes ("Romans in the
  Countryside", "Love and Marriage"), the 2024-2025 narratives (Suetonius Nero,
  Ovid's Perseus) or the 2024-2026 civilisation topics (Roman family life, the
  city of Rome).
- Lesson descriptions: 60-100 characters, plain unicode, student-facing, no
  board name, no codes.
- `question_type_names`: this board publishes no per-question mark tariffs in
  the specification, so the type names MUST NOT contain a number of marks.
  Use tariff-free names that describe the task, for example
  "Comprehension - Short Answer", "Translation into English",
  "Derivation", "Grammar - Recognise and Explain",
  "Literary Style - Analyse the Effect", "Source Analysis",
  "Extended Evaluative Response", "Roman Civilisation - Explain".
  Return between 6 and 9 such names, covering every article unit.
- `quote_ticker_quotes`: 6 entries. Latin quotations with an English
  translation after a slash, from genuinely attested classical authors, plus
  well-known Latin proverbs. Only quote what you are certain is verbatim.
- The teaching_brief must cite a source for every entry, and must include the
  practical realities of a small-entry classical subject: the momentum-test
  format, the open-book literature papers, the fact that the qualification is
  non-tiered, and the derivation element.

RESEARCH BUDGET: use web search 6-10 times, on the awarding body's own teacher
pages, its published examiners' reports for GCSE Latin, the Cambridge School
Classics Project, and Classical Association / Classics for All teaching
guidance. Research informs pedagogy and emphasis only, never content.
"""


def main():
    cfg = D.load_config(CFG_PATH)
    planning_doc = D.read(os.path.join(cfg["docs_dir"], "PLANNING_PROMPT.md"))
    system = D.extract_prompt_section(planning_doc, "## System prompt",
                                      "## User message template")
    spec_core = D.read(os.path.join(cfg["build_dir"], "spec_core.md"))
    assess = D.read(os.path.join(cfg["build_dir"], "assessment_rules.md"))
    house = D.read(os.path.join(cfg["build_dir"], "house_rules.md"))
    dvl = json.load(io.open(os.path.join(cfg["build_dir"], "dvl.json"), encoding="utf-8"))
    dvl_txt = "\n".join("%s = %s" % (p["latin"], p["english"])
                        for p in dvl["dvl_latin_english"])

    user = (
        "SUBJECT: Latin\nEXAM BOARD: Eduqas / WJEC\nSPEC CODE: C580QS\n"
        "SCHOOL_ID: null\nTARGET AUDIENCE: free-tier\n"
        "EXAMINATION SERIES OUR STUDENTS SIT: summer 2027\n\n"
        "<spec>\n%s\n</spec>\n\n"
        "<assessment_rules>\n%s\n</assessment_rules>\n\n"
        "<house_rules>\n%s\n</house_rules>\n\n"
        "<defined_vocabulary_list count=\"%d\">\n%s\n</defined_vocabulary_list>\n\n"
        "%s\n%s\nGenerate the plan JSON."
        % (spec_core, assess, house, len(dvl["dvl_latin_english"]), dvl_txt,
           UNIT_SKELETON, EXTRA))

    print("planning call: system %dk chars, user %dk chars"
          % (len(system) // 1000, len(user) // 1000))
    cl = D.client()
    with cl.messages.stream(
        model=D.MODEL_PLAN,
        max_tokens=40000,
        thinking={"type": "adaptive"},
        tools=[{"type": "web_search_20260209", "name": "web_search", "max_uses": 10}],
        system=[{"type": "text", "text": system}],
        messages=[{"role": "user", "content": [
            {"type": "text", "text": user,
             "cache_control": {"type": "ephemeral"}}]}],
    ) as stream:
        msg = stream.get_final_message()

    text = "".join(b.text for b in msg.content if b.type == "text")
    io.open(os.path.join(cfg["run_dir"], "plan_raw.txt"), "w",
            encoding="utf-8").write(text)
    rec = D.log_usage(cfg, "plan", D.MODEL_PLAN, "plan", msg.usage)
    print("plan usage: in=%d out=%d searches=%s stop=%s ($%.3f)"
          % (rec["input_tokens"], rec["output_tokens"], rec["web_searches"],
             msg.stop_reason, D.cost_of(rec)))
    plan = D.parse_json_reply(text)
    D.write_json(os.path.join(cfg["run_dir"], "plan.json"), plan)
    art = plan.get("article_units", [])
    pra = plan.get("practice_units", [])
    print("plan saved: %d article units (%d lessons), %d practice units (%d lessons)"
          % (len(art), sum(len(u.get("lessons", [])) for u in art),
             len(pra), sum(len(u.get("lessons", [])) for u in pra)))
    if plan.get("gaps"):
        print("GAPS:")
        for g in plan["gaps"]:
            print("  -", g)


if __name__ == "__main__":
    main()
