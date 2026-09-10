# -*- coding: utf-8 -*-
"""Seed a rebuild of one AQA GCSE Drama (8261) set-play unit in `drama-aqa`.

The three units rebuilt with this script were flagged `needs-rebuild` by the
retro fact-check programme because the original lessons contained INVENTED plot
points and characters. The fix is not a better prompt — it is a source bank.

Per play this writes:
  * the build context doc (spec slice + assessment rules + house rules + the
    whole source bank)                                  -> spec_md
  * the source bank on its own (the fact-check authority) -> factcheck_context_doc
  * a deterministic quote-gate corpus built mechanically from the source bank's
    own quoted spans (plus, for The Empress, the full play text)
                                                        -> quote_gate_corpus
  * the assessment-rules doc, quoted from the specification only
  * plan.json, state.json and the driver config.

The lesson ROWS are never deleted: this build patches the eight existing rows
in place, so lesson ids, slugs and hero images survive. Titles are re-patched
because the eight-lesson shape changes (one plot lesson becomes two).

Usage:  python scripts/api_build/setup_drama_play.py the-empress
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = r"C:\Users\tshau\Documents\Study Vault"
SCRATCH = (r"C:\Users\tshau\AppData\Local\Temp\claude"
           r"\C--Users-tshau-Documents-Study-Vault"
           r"\88006801-843c-4d74-957a-5eebdef537b9\scratchpad\drama")
SRC = os.path.join(REPO, "scripts", "_content_drama-aqa", "_source")
KIT = r"C:\Users\tshau\.claude\jobs\4059242c\tmp"

SUBJECT_ID = "77ce8c70-9ea9-4293-83c3-fadfa31b034f"   # drama-aqa (school_id NULL)

# --------------------------------------------------------------------------
# Assessment context. Every statement below is quoted or directly paraphrased
# from the AQA GCSE Drama 8261 specification (version 1.7, 26 April 2022),
# specs/aqa/drama-8261-8261.md. Nothing here is inferred.
# --------------------------------------------------------------------------
ASSESSMENT = """# AQA GCSE Drama 8261 — assessment rules for the set-play questions

These statements come from the AQA specification (version 1.7, 26 April 2022).
They are the ONLY authority on exam structure for this unit. Anything not
stated here must not be claimed.

## The written paper
- The written paper is called Understanding drama. It is 1 hour and 45 minutes,
  OPEN BOOK, marked out of 80, and worth 40% of the GCSE.
- It has three compulsory parts: theatre roles and terminology; the study of the
  set text; and the live theatre production.
- The theatre roles and terminology part is four multiple-choice questions on
  professional theatre maker roles and/or terminology, marked out of 4.
- The set-text part is marked out of 44. The live theatre part is marked out
  of 32.
- Students must not answer on the same play for the set text and for the live
  production: the live production seen cannot be their set play.

## The set-text questions
- Students answer short and extended questions on one set play chosen from the
  prescribed list of nine.
- ONE EXTRACT from each set play is PRINTED IN THE QUESTION PAPER. Students
  answer questions relating to that extract, referring to the whole play as
  appropriate to the demands of the question.
- Students are expected to know and understand the characteristics and the
  context of the WHOLE play they have studied.
- Where relevant, students may support their answers with sketches or diagrams.
- All students must be prepared to answer questions from the perspective of a
  PERFORMER.
- The paper includes one compulsory short answer question for all students
  linking DESIGN AND CONTEXT and/or THEATRICAL CONVENTIONS. Students do not need
  practical experience of design to answer it.
- One part offers students the choice of answering as either a PERFORMER or a
  DESIGNER (lighting, sound, set, costume, puppets).
- Students may refer to a clean copy of their play in the exam. It must not be
  annotated and must not contain any additional notes, marks, alterations or
  inclusions.
- Specific editions are prescribed for each play.

## Assessment objectives
- AO1: create and develop ideas to communicate meaning for theatrical
  performance. AO2: apply theatrical skills to realise artistic intentions in
  live performance. AO3: demonstrate knowledge and understanding of how drama
  and theatre is developed and performed. AO4: analyse and evaluate their own
  work and the work of others.
- The written paper assesses knowledge and understanding of how drama and
  theatre is developed and performed, including in connection to a set play,
  and the ability to analyse and evaluate the live theatre work of others. AO2
  is assessed practically, not on the written paper.

## Hard limits on what may be claimed
- Do NOT state a per-question mark tariff as if the specification set one: the
  specification gives only the 4 / 44 / 32 totals for the three parts.
- Do NOT reproduce, paraphrase or imitate AQA's level of response band
  descriptors, and never use "Level 1"-style band names.
- Do NOT invent extra parts, extra questions, timings for individual questions,
  or a choice of set-play question within the paper.
- Do NOT claim marks are awarded for spelling, punctuation and grammar on this
  paper.
"""

HOUSE_RULES = """## StudyVault house rules for this unit (non-negotiable)

- British English spelling and punctuation throughout (theatre, colour, realise,
  behaviour, programme).
- NEVER use board paper codes, specification codes or part names in
  student-facing text. Never write the specification number, and never write
  "Section A", "Section B", "Section C", "Component 1", "Component 2",
  "Component 3", "Paper 1" or any similar shorthand ANYWHERE in the lesson —
  the platform validator hard-bans them. Write "the written paper", "the
  set-play questions", "the extract question", "the performer-or-designer
  question", "the extended staging question".
- Never name the exam board as an actor ("AQA wants...", "the examiner is
  looking for..."). Describe the task, not the board's supposed preferences.
- Never reproduce or paraphrase band descriptors. Where a mark scheme needs
  bands, use StudyVault's neutral vocabulary only: Mastering / Secure /
  Developing / Emerging. Never "Level 4", never "Award 3 marks for".

### Grounding — the point of this rebuild
- The SOURCE BANK supplied below is the ONLY authority for anything about the
  play: its plot, its scenes, its characters, its stage directions, its
  language, its first production, and its context. If a claim about the play is
  not supported by the source bank, DO NOT MAKE IT. Do not fill a gap from
  general knowledge, from a film adaptation, from another play, or from what
  would "make sense".
- You MAY and SHOULD summarise and paraphrase the plot in detail. Grounded plot
  knowledge is exactly what these lessons exist to give. Summarising a plot is
  not a copyright problem.
- What IS a copyright problem is reproducing the playwright's words. Therefore:
  place inside quotation marks ONLY a span that appears in the source bank's
  list of quotable spans (or a shorter span taken from one). Keep every quotation
  under fifteen words. Never reproduce a speech, a song stanza or a run of
  dialogue. Prefer paraphrase; quote only where the exact wording carries the
  teaching point.
- Where the source bank marks something [DISPUTED] or [UNCLEAR] or says it is
  "not established by the sources consulted", the lesson must stay
  non-committal on that detail: teach around it, or say plainly that productions
  differ. NEVER resolve an uncertainty by inventing a detail. Never write a
  practice question, knowledge check or flashcard that turns on a disputed
  detail.
- Never tell the student that source material was limited, never apologise for
  the amount of quotation, and never mention this source bank. Write with
  authority about what you do know.

### Drama content rules
- PERFORMER AND DESIGNER LENS. Every lesson must teach students to think as a
  performer AND as a designer about at least one named moment. Worked examples
  and the exam-tip block must carry both vocal/physical choices and at least one
  design discipline (lighting, sound, set or costume).
- CONCRETE, NAMED CHOICES. "Dark lighting" and "sad music" are Developing-band
  answers. Name the element: a profile lantern with a breakup gobo, a steel-blue
  wash, a slow cross-fade, a low sustained cello drone, a worn wool coat in
  faded ochre, a downstage-left position, three metres of proxemic distance, a
  rising pace across four short lines.
- STAGECRAFT VOCABULARY, glossed on first use: stage left and right, upstage
  and downstage, blocking, proxemics, levels, focus, tableau, naturalistic and
  stylised, lighting state, wash, special, gobo, cross-fade, blackout, sound
  cue, soundscape, underscore, direct address, fourth wall, multi-roling,
  ensemble, transition, sightlines, and the staging configurations (proscenium
  arch, thrust, traverse, theatre in the round, end on, promenade).
- STAGING CONFIGURATIONS. At least one lesson per unit should weigh how a named
  moment would change in two different configurations.
- PRACTICE QUESTIONS: exactly 6 per lesson, drawn from the registered question
  type names supplied. The "marks" field is the StudyVault rubric as a string
  using Mastering / Secure / Developing / Emerging — never a number, never a
  board band. Question stems must ask about performing, directing or designing a
  NAMED moment, never about a reproduced line of dialogue.
- KNOWLEDGE CHECKS: exactly 5 per lesson, and exactly this mix — 2 of type
  "mcq", 2 of type "fill", 1 of type "match". Canonical shapes only: mcq and
  fill carry "options" plus "correct" (an integer index); match carries "left",
  "right" and "order". Never an "answers" array, never a "pairs" array.
- FLASHCARDS: 10 to 12 per lesson. Each answer 30 words or fewer; no two cards
  in the deck share an answer; no answer is a list ("X, Y and Z"); no answer
  restates its question; a one-word answer only where the question begins What /
  Who / When / Where / Which / Name / Give / State, or the answer is a number or
  a date. Mix card types: character to function, moment to what it reveals, term
  to definition, choice to effect on the audience.
- GLOSSARY: at least six inline glossary entries per lesson. Drama is
  terminology-dense, so this is easy without padding.
- description: 60 to 100 characters.
- Question fields (practice question text, knowledge checks, flashcards,
  glossary) are PLAIN TEXT with real unicode characters. Only the *_html fields
  use HTML entities.
- Write for GCSE students aged 15 to 16.
"""

QUESTION_TYPES = [
    "1 mark — Identify",
    "2 marks — Define",
    "4 marks — Explain Effect",
    "4 marks — Short Analysis",
    "8 marks — Interpret as Performer",
    "8 marks — Interpret as Designer",
    "12 marks — Analyse Intentions",
    "20 marks — Extended Staging Response",
]

TEACHING_BRIEF = {
    "unit_shape": (
        "Eight lessons on one set play. Lesson 1 is context and the playwright; "
        "lessons 2 and 3 walk the story in order so that every later lesson can "
        "name real moments; lesson 4 is characters and relationships; lesson 5 is "
        "themes; lesson 6 is form, structure and dramatic methods; lesson 7 is "
        "staging and design; lesson 8 is exam practice across the performer, "
        "director and designer question types. No overview lesson and no "
        "practitioner-biography lesson: where a practitioner or company genuinely "
        "shaped this play, that belongs inside lessons 6 and 7."),
    "per_lesson": (
        "Every lesson names specific moments of the play and turns them into "
        "concrete performer and designer choices with a stated effect on the "
        "audience. Every lesson glosses its stagecraft terms. Every lesson links "
        "at least one choice to the play's social, cultural or historical "
        "context, because the paper carries a compulsory short question linking "
        "design and context and/or theatrical conventions."),
    "grounding": (
        "The supplied source bank is the sole authority on the play. Paraphrase "
        "its plot freely; quote only its listed quotable spans; stay "
        "non-committal wherever it records a dispute or a gap."),
    "practice_mix": (
        "6 practice questions per lesson spanning the registered types. At least "
        "one performer question and at least one designer question in every "
        "lesson. Extended questions must name the moment and ask for a "
        "substantiated directorial judgement. Mark schemes use the StudyVault "
        "rubric and reward concrete named choices anchored to a named moment "
        "with a named effect."),
    "audience": (
        "GCSE students aged 15 to 16 sitting an OPEN BOOK written paper with a "
        "printed extract in front of them. They need to know the whole play well "
        "enough to place any extract, and to have a stock of concrete staging "
        "choices ready to deploy."),
}

# --------------------------------------------------------------------------
# The three units. unit_id is the live Supabase row; the rebuild patches those
# eight rows in place and never deletes them.
# --------------------------------------------------------------------------
PLAYS = {
    "the-empress": {
        "unit_slug": "the-empress",
        "unit_id": "d7a76fb7-7f0f-4e51-9c01-1349426ee100",
        "unit_name": "The Empress",
        "subtitle": "Tanika Gupta's two-act epic of ayahs, lascars and the Queen Empress",
        "accent": "#9d174d",
        "play": "The Empress",
        "author": "Tanika Gupta",
        "edition": "Methuen Drama, Student Editions",
        "sourcebank": "the-empress_sourcebank.md",
        "full_text": "_empress_play.txt",
        "scope": (
            "AQA GCSE Drama, the study of a set play, where the set play is 'The Empress' "
            "by Tanika Gupta (Methuen Drama, Student Editions, with commentary and notes "
            "by Jane Garnett). The play is in two acts of fifteen scenes each, set between "
            "1887 and 1901, and was premiered by the Royal Shakespeare Company at the Swan "
            "Theatre, Stratford-upon-Avon, in 2013, directed by Emma Rice. Any character, "
            "scene, line, event or production detail not in the supplied source bank is out "
            "of scope and must be treated as fabricated. Rani and Queen Victoria never meet."),
        "lessons": [
            (1, "Context: Gupta, Empire and the World of the Play",
             "The Victorian Empire, ayahs and lascars, and how Tanika Gupta came to write the play.",
             ["1. Bibliographic facts", "9. Historical context", "2. The play in one paragraph"]),
            (2, "The Story: Act One, 1887",
             "Rani's abandonment at Tilbury and Abdul Karim's arrival at court, scene by scene.",
             ["4. Act One (1887) — scene by scene"]),
            (3, "The Story: Act Two, 1891 to 1901",
             "The Ayahs' Home, Dadabhai's election, the Diamond Jubilee and the burning of the letters.",
             ["5. Act Two — scene by scene"]),
            (4, "Characters: Rani, Hari, Abdul and the Queen",
             "Who everyone is, what they want, and how the play's relationships shift over fourteen years.",
             ["3. Characters", "4. Act One (1887) — scene by scene", "5. Act Two — scene by scene"]),
            (5, "Themes: Empire, Race, Education and Solidarity",
             "The ideas Gupta builds across the two plots, and the moments that carry them.",
             ["6. Themes, with the evidence in the play"]),
            (6, "Form and Methods: Thirty Scenes, Songs and Languages",
             "Cross-cutting, split scenes, the songs, the two languages and the play's mosaic structure.",
             ["7. Form, structure, staging and the first production"]),
            (7, "Staging and Design: Ships, Palaces and the Ayahs' Home",
             "Designing a play that moves from a scrubbed deck to Windsor Castle in seconds.",
             ["7. Form, structure, staging and the first production"]),
            (8, "Exam Practice: Performer, Director and Designer",
             "Working a printed extract from this play into performer, designer and staging answers.",
             ["4. Act One (1887) — scene by scene", "5. Act Two — scene by scene",
              "7. Form, structure, staging and the first production"]),
        ],
    },
    "a-taste-of-honey": {
        "unit_slug": "a-taste-of-honey",
        "unit_id": "6e5bf995-9b84-4e3f-8a59-80c6616e4b6a",
        "unit_name": "A Taste of Honey",
        "subtitle": "Shelagh Delaney's Salford two-hander of mothers, lodgers and survival",
        "accent": "#a16207",
        "play": "A Taste of Honey",
        "author": "Shelagh Delaney",
        "edition": "Methuen Drama",
        "sourcebank": "a-taste-of-honey_sourcebank.md",
        "full_text": None,
        "scope": (
            "AQA GCSE Drama, the study of a set play, where the set play is 'A Taste of "
            "Honey' by Shelagh Delaney (Methuen Drama), first performed by Theatre Workshop "
            "at the Theatre Royal Stratford East in 1958. Any character, scene, line, event "
            "or production detail not in the supplied source bank is out of scope and must "
            "be treated as fabricated. The 1961 film differs from the play and is not the "
            "set text."),
        "lessons": [
            (1, "Context: Salford 1958 and Theatre Workshop",
             "Delaney, the kitchen-sink movement and the world that made this play possible.",
             ["## 9. Context", "## 1. Bibliographic facts"]),
            (2, "The Story: Act One",
             "Helen and Jo move in, Peter arrives, and Jo meets the sailor, scene by scene.",
             ["## 3. The story — Act One", "## 2. Structure and setting"]),
            (3, "The Story: Act Two",
             "Geof moves in, Helen returns, and how the play actually ends.",
             ["## 4. The story — Act Two", "## 5. The ending — stated exactly"]),
            (4, "Characters: Jo, Helen, Geof, Peter and the Boy",
             "Who everyone is, what they want, and how each relationship shifts across the play.",
             ["## 6. Characters", "## 3. The story — Act One", "## 4. The story — Act Two"]),
            (5, "Themes: Motherhood, Class, Race and Sexuality",
             "The ideas Delaney puts on stage and the moments that carry them.",
             ["## 7. Themes and form", "## 9. Context"]),
            (6, "Form and Methods: Direct Address, Music and Comedy",
             "Why the play breaks the fourth wall, and how comedy sits inside a bleak story.",
             ["## 7. Themes and form", "## 2. Structure and setting"]),
            (7, "Staging and Design: The Flat, the Street and the Band",
             "Designing two comfortless playing areas that have to hold a whole year.",
             ["## 7. Themes and form", "## 2. Structure and setting"]),
            (8, "Exam Practice: Performer, Director and Designer",
             "Working a printed extract from this play into performer, designer and staging answers.",
             ["## 3. The story — Act One", "## 4. The story — Act Two", "## 7. Themes and form"]),
        ],
    },
    "things-i-know-to-be-true": {
        "unit_slug": "things-i-know-to-be-true",
        "unit_id": "5dba787f-1506-448c-92b8-f2cfe08d0d78",
        "unit_name": "Things I Know to Be True",
        "subtitle": "Andrew Bovell and Frantic Assembly's family drama in four seasons",
        "accent": "#15803d",
        "play": "Things I Know to Be True",
        "author": "Andrew Bovell",
        "edition": "Nick Hern Modern Plays",
        "sourcebank": "things-i-know-to-be-true_sourcebank.md",
        "full_text": None,
        "scope": (
            "AQA GCSE Drama, the study of a set play, where the set play is 'Things I Know "
            "to Be True' by Andrew Bovell (Nick Hern Modern Plays), created with Frantic "
            "Assembly and State Theatre Company South Australia and premiered in 2016. Any "
            "character, scene, line, event or production detail not in the supplied source "
            "bank is out of scope and must be treated as fabricated. Where the source bank "
            "records that sources disagree or are silent, the lesson must stay "
            "non-committal."),
        "lessons": [
            (1, "Context: Bovell, Frantic Assembly and Suburban Australia",
             "The writers, the company and the world of the Price family's back garden.",
             ["## 1. Bibliographic facts", "## 6. Themes and ideas", "## 3. Setting"]),
            (2, "The Story: The Phone Call to Autumn",
             "The frame, Rosie's return from Berlin, the family gathering and Pip's departure.",
             ["## 4. The story, in order", "## 2. Structure"]),
            (3, "The Story: Winter to the Last Summer",
             "Mark's revelation, Ben's confession, Rosie's leaving and how the play ends.",
             ["## 4. The story, in order"]),
            (4, "Characters: Bob, Fran and the Four Children",
             "Who everyone is, what they want, and how the family's relationships shift.",
             ["## 5. Characters", "## 4. The story, in order"]),
            (5, "Themes: Family, Truth, Identity and Love",
             "The ideas Bovell puts on stage and the moments that carry them.",
             ["## 6. Themes and ideas", "## 4. The story, in order"]),
            (6, "Form and Methods: Monologue, Movement and Season",
             "The seasonal frame, the four monologues and the physical language built with the company.",
             ["## 2. Structure", "## 7. Frantic Assembly staging and method"]),
            (7, "Staging and Design: The Garden, the Bulbs and the Lifts",
             "Designing a play whose emotion is carried as much by bodies as by dialogue.",
             ["## 7. Frantic Assembly staging and method", "## 3. Setting"]),
            (8, "Exam Practice: Performer, Director and Designer",
             "Working a printed extract from this play into performer, designer and staging answers.",
             ["## 4. The story, in order", "## 7. Frantic Assembly staging and method"]),
        ],
    },
}

FACTCHECK_EXTRA = """ADDITIONAL RULE FOR THIS UNIT — THE SOURCE BANK IS THE ONLY AUTHORITY ON THE PLAY.

The SOURCE TEXT block supplied to you is a source bank compiled from the published play text and/or from reconciled published sources, and it is the sole authority for every claim about the play: plot, order of events, scene content, characters and their names, relationships, stage directions, language, first production, design and context.

- Flag as HIGH any statement about the play that the source bank does not support: an event that does not happen, an event in the wrong order, a character who does not exist, a character doing something the bank attributes to someone else, an invented stage direction, an invented production detail, or a wrong account of how the play ends.
- Flag as HIGH any quotation attributed to the play that does not appear verbatim in the source bank's quotable spans (allowing only straight/curly quote and whitespace differences). Supply as the correction either the nearest real span from the bank or, better, a paraphrase with the quotation marks removed.
- Flag as HIGH any lesson claim that resolves something the bank marks [DISPUTED], [UNCLEAR], or "not established by the sources consulted". The correction must make the lesson non-committal on that detail while keeping its teaching point.
- Do NOT use general web knowledge, a film adaptation, or another play to judge these claims. Where the bank is silent and the lesson is also silent, there is no finding.
- Do NOT flag stagecraft suggestions as unsupported: a lesson proposing how a moment COULD be lit, designed or performed is making a creative proposal, not a factual claim, and is fine as long as the moment itself is real and described correctly. A claim about what a REAL production actually did is a factual claim and must be in the bank.
- Do not flag British spelling, pedagogical simplification for age 15-16, or the StudyVault rubric vocabulary (Mastering / Secure / Developing / Emerging).
"""


def read(p):
    return io.open(p, encoding="utf-8").read()


# --------------------------------------------------------------------------
# Deterministic quote-gate corpus. Built mechanically from the spans the source
# bank itself places inside quotation marks, so that the bank's own explanatory
# prose can never be passed off as a line of the play. For The Empress the full
# play text is added as well, because we hold it.
# --------------------------------------------------------------------------
_SPAN_RE = re.compile("\u201c([^\u201d]{2,400})\u201d|\u2018([^\u2019]{2,400})\u2019|\"([^\"]{2,400})\"")

# Craft vocabulary and framing phrases a lesson legitimately puts in quotation
# marks without claiming they are the playwright's words.
GENERIC_ALLOWED = """
kitchen sink kitchen-sink angry young men the fourth wall breaking the fourth wall
direct address in the round end on theatre in the round proscenium arch thrust stage
traverse promenade stage left stage right upstage downstage centre stage
building blocks round by through chair duet physical theatre epic theatre
alienation effect the alienation effect gestus verfremdungseffekt
the method emotion memory given circumstances magic if
kala pani jewel in the crown the white man's burden white man's burden
the empress of famine and the queen of black death
"""


def build_gate_corpus(cfg_play):
    p = PLAYS[cfg_play]
    bank = read(os.path.join(SRC, p["sourcebank"]))
    spans = []
    for m in _SPAN_RE.finditer(bank):
        s = next(g for g in m.groups() if g)
        s = re.sub(r"\s+", " ", s).strip()
        if len(s.split()) >= 2 and s not in spans:
            spans.append(s)
    parts = ["\n".join(spans), GENERIC_ALLOWED]
    if p.get("full_text"):
        fp = os.path.join(SRC, p["full_text"])
        if os.path.exists(fp):
            parts.append(read(fp))
    return "\n\n".join(parts) + "\n"


def build_context(cfg_play):
    p = PLAYS[cfg_play]
    spec_slice = read(os.path.join(REPO, "scripts", "_content_drama-aqa", "_spec_set-play.txt"))
    bank = read(os.path.join(SRC, p["sourcebank"]))
    return "\n".join([
        "# AQA GCSE Drama — set play: %s by %s — build context" % (p["play"], p["author"]),
        "",
        "The prescribed edition is %s." % p["edition"],
        "",
        ASSESSMENT,
        "",
        "## Specification slice for the set-play questions",
        "",
        spec_slice,
        "",
        HOUSE_RULES,
        "",
        "## SOURCE BANK — the only authority on this play",
        "",
        bank,
    ])


def build_plan(cfg_play):
    p = PLAYS[cfg_play]
    lessons = [{
        "number": n,
        "title": t,
        "description": d,
        "spec_references": ["Set play", "Knowledge and understanding",
                            "How meaning is interpreted and communicated"],
        "section_markers": markers,
    } for n, t, d, markers in p["lessons"]]
    return {
        "subject": {"name": "Drama", "slug": "drama-aqa",
                    "exam_board": "AQA", "spec_code": "8261", "school_id": None},
        "article_units": [{
            "name": p["unit_name"], "slug": p["unit_slug"], "subtitle": p["subtitle"],
            "body_class": "unit-" + p["unit_slug"],
            "accent": p["accent"], "accent_light": p["accent"] + "22",
            "accent_badge": p["accent"] + "33",
            "lesson_count": len(lessons), "lessons": lessons,
        }],
        "practice_units": [],
        "question_type_names": QUESTION_TYPES,
        "teaching_brief": TEACHING_BRIEF,
    }


def main(play):
    if play not in PLAYS:
        raise SystemExit("unknown play: %s (want one of %s)" % (play, ", ".join(PLAYS)))
    p = PLAYS[play]
    bank_path = os.path.join(SRC, p["sourcebank"])
    if not os.path.exists(bank_path):
        raise SystemExit("source bank missing: %s — build it before seeding" % bank_path)

    run_dir = os.path.join(SCRATCH, "run-" + play)
    os.makedirs(run_dir, exist_ok=True)
    os.makedirs(SCRATCH, exist_ok=True)

    ctx = os.path.join(SCRATCH, "context_%s.md" % play)
    src = os.path.join(SCRATCH, "source_%s.md" % play)
    gate = os.path.join(SCRATCH, "gate_%s.txt" % play)
    rules = os.path.join(SCRATCH, "assessment_drama_8261.md")

    io.open(ctx, "w", encoding="utf-8").write(build_context(play))
    io.open(src, "w", encoding="utf-8").write(read(bank_path))
    io.open(gate, "w", encoding="utf-8").write(build_gate_corpus(play))
    io.open(rules, "w", encoding="utf-8").write(ASSESSMENT)

    plan = build_plan(play)
    io.open(os.path.join(run_dir, "plan.json"), "w", encoding="utf-8").write(
        json.dumps(plan, ensure_ascii=False, indent=1))

    cfg = {
        "slug": "drama-aqa-" + play,
        "subject_slug": "drama-aqa",
        "subject_name": "Drama",
        "exam_board": "AQA",
        "spec_code": "8261",
        "unit_name": p["unit_name"],
        "spec_md": ctx,
        "factcheck_context_doc": src,
        "factcheck_search_max": 2,
        # Opus thinking bills against max_tokens before the findings JSON starts;
        # 8000 truncated 6 of 8 checks on the first run.
        "factcheck_max_tokens": 24000,
        "unitcheck_max_tokens": 32000,
        "factcheck_system_extra": FACTCHECK_EXTRA,
        "quote_gate_corpus": gate,
        "assessment_rules_doc": rules,
        "scope_statement": p["scope"],
        "patch_titles": True,
        "keep_hero_caption": True,
        "reference_lesson": os.path.join(SCRATCH, "reference_lesson.json"),
        "docs_dir": os.path.join(REPO, "docs"),
        "validator": os.path.join(REPO, "scripts", "_validate_content_json.py"),
        "factcheck_out_dir": os.path.join(REPO, "scripts", "_fact_check"),
        "run_dir": run_dir,
    }
    cfg_path = os.path.join(REPO, "scripts", "api_build", "config_drama-aqa-%s.json" % play)
    io.open(cfg_path, "w", encoding="utf-8").write(json.dumps(cfg, indent=1))

    st_path = os.path.join(run_dir, "state.json")
    st = json.load(io.open(st_path, encoding="utf-8")) if os.path.exists(st_path) else {}
    st["subject_id"] = SUBJECT_ID
    io.open(st_path, "w", encoding="utf-8").write(json.dumps(st, indent=1))

    print("play:     ", p["play"])
    print("  bank    %s (%d chars)" % (bank_path, os.path.getsize(bank_path)))
    print("  context %s (%d chars)" % (ctx, os.path.getsize(ctx)))
    print("  gate    %s (%d chars)" % (gate, os.path.getsize(gate)))
    print("  config  %s" % cfg_path)
    print("  run_dir %s" % run_dir)
    print("  lessons %d" % len(plan["article_units"][0]["lessons"]))


if __name__ == "__main__":
    main(sys.argv[1])
