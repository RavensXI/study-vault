# -*- coding: utf-8 -*-
"""PROTOTYPE rebuild of score-reading L1 "Reading Rhythm".

The old lesson showed 19th-century scans at 40% size with nothing marked, and
asked "look at the score and find X" of a student who cannot read music. It also
marked the Mozart time signature as 4/4 when the score plainly shows cut common.
See SCORE_READING_AUDIT.md.

This version:
  - teaches on the notation before testing it — every teaching point is an
    engraved figure with the thing under discussion ringed and labelled;
  - uses purpose-made examples, so the answer is always actually visible;
  - asks questions that require LOOKING, not recalling a definition;
  - is SVG throughout, so it stays sharp at any size and never renders at 87px.

Backs up the existing practice_data first.
    python build_score_reading_L1.py              apply
    python build_score_reading_L1.py --restore    put the old lesson back
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client
from notation import figure, card, row

BACKUP = os.path.join(HERE, "_score_reading_L1_backup.json")

# ---------------------------------------------------------------- figures ----
F_WHERE = card(figure("X:1\nT:\nM:4/4\nL:1/4\nK:C\nG G G G | B2 B2 |",
                      ring=[("meterSig", "the time signature")], width=1200),
               "Where to look",
               "It appears once, just after the clef, at the very start &mdash; not on every line.")

F_ANATOMY = card(figure("X:1\nT:\nM:4/4\nL:1/4\nK:C\nG G G G |",
                        ring=[("meterSig", "4 over 4")],
                        note_labels=[(0, "1"), (1, "2"), (2, "3"), (3, "4")],
                        brackets=[(0, 3, "four beats, then the bar line")], width=1000),
                 "Reading the two numbers",
                 "Top: how many beats in each bar. Bottom: 4 means the beat is a crotchet.")

# Tom's confusion, and it was my fault: the old text said "a tail or a beam
# shortens it again", which makes a minim ambiguous — it is hollow AND carries a
# vertical line. That line is a STEM, not a tail. Separate the three parts
# explicitly, and give each note its own cell so the labels cannot collide.
_V = [("G4", "semibreve<br><b>4 beats</b><br>hollow, no stem"),
      ("G2", "minim<br><b>2 beats</b><br>hollow, with stem"),
      ("G", "crotchet<br><b>1 beat</b><br>filled, with stem"),
      ("G/2", "quaver<br><b>half a beat</b><br>filled, one tail"),
      ("G//", "semiquaver<br><b>quarter beat</b><br>filled, two tails")]
F_VALUES = row([("X:1\nT:\nM:4/4\nL:1/4\nK:C\n%s|" % v, c) for v, c in _V],
               "The five note values",
               "Three things to look at: is the <b>head</b> hollow or filled, and how many "
               "<b>tails</b> does it have? The <b>stem</b> &mdash; the vertical line &mdash; is "
               "just a handle. It never changes the length.")

F_DOT = row([("X:1\nT:\nM:4/4\nL:1/4\nK:C\nG2|", "minim<br><b>2 beats</b>"),
             ("X:1\nT:\nM:4/4\nL:1/4\nK:C\nG3|", "dotted minim<br><b>3 beats</b><br>2 + half of 2"),
             ("X:1\nT:\nM:4/4\nL:1/4\nK:C\nG|", "crotchet<br><b>1 beat</b>"),
             ("X:1\nT:\nM:4/4\nL:1/4\nK:C\nG3/2|", "dotted crotchet<br><b>1&frac12; beats</b><br>1 + half of 1")],
            "A dot adds half of whatever the note is worth",
            "It does <b>not</b> always add one beat. Add half of the note's own value: a minim "
            "(2) gains 1 and becomes 3; a crotchet (1) gains a half and becomes 1&frac12;.")

F_SIMPLE = card(figure("X:1\nT:\nM:2/4\nL:1/8\nK:C\nGG GG |",
                       ring=[("meterSig", "simple time")],
                       brackets=[(0, 1, "beat 1 splits in 2"), (2, 3, "beat 2 splits in 2")],
                       width=1000),
                "Simple time &mdash; each beat divides into 2",
                "A top number of 2, 3 or 4 means simple time.")

F_COMPOUND = card(figure("X:1\nT:\nM:6/8\nL:1/8\nK:C\nGGG GGG |",
                         ring=[("meterSig", "compound time")],
                         brackets=[(0, 2, "beat 1 splits in 3"), (3, 5, "beat 2 splits in 3")],
                         width=1100),
                  "Compound time &mdash; each beat divides into 3",
                  "A top number of 6, 9 or 12 means compound time. This is what the exam tests.")

F_ANACRUSIS = card(figure("X:1\nT:\nM:4/4\nL:1/4\nK:C\nG | c3 G | c4 |",
                          note_labels=[(0, "anacrusis")], width=1200),
                   "An anacrusis is an incomplete bar at the start",
                   "The music begins before the first full bar. Also called an upbeat or pick-up.")

# question stimuli — unlabelled, so the student must actually read them
Q_34 = card(figure("X:1\nT:\nM:3/4\nL:1/4\nK:C\nG G G | B2 B |", width=1000),
            None, "Extract 1")
Q_98 = card(figure("X:1\nT:\nM:9/8\nL:1/8\nK:C\nGGG GGG GGG |", width=1100),
            None, "Extract 2")
Q_DOT = card(figure("X:1\nT:\nM:4/4\nL:1/4\nK:C\nc3 G | G2 G2 |", width=1100),
             None, "Extract 3")
Q_ANAC = card(figure("X:1\nT:\nM:4/4\nL:1/4\nK:C\nG G | c2 c2 | c4 |", width=1200),
              None, "Extract 4")

PASSAGES = [
    {"id": "teach-where", "label": "Finding the time signature", "text": F_WHERE + F_ANATOMY},
    {"id": "teach-values", "label": "Note values", "text": F_VALUES + F_DOT},
    {"id": "teach-simple-compound", "label": "Simple and compound time",
     "text": F_SIMPLE + F_COMPOUND},
    {"id": "teach-anacrusis", "label": "Anacrusis", "text": F_ANACRUSIS},
    {"id": "q-34", "label": "Extract 1", "text": Q_34},
    {"id": "q-98", "label": "Extract 2", "text": Q_98},
    {"id": "q-dot", "label": "Extract 3", "text": Q_DOT},
    {"id": "q-anac", "label": "Extract 4", "text": Q_ANAC},
]

METHOD = {
    "title": "How to read rhythm from a score",
    "content": (
        "<p>Section A can show you up to 12 bars of staff notation. You are not asked to play it "
        "&mdash; only to read four things off it. This lesson shows you each one on the stave "
        "before it asks you anything.</p>"
        "<p><strong>1. The time signature.</strong> Two numbers stacked at the very start, just "
        "after the clef.</p>" + F_WHERE + F_ANATOMY +
        "<p><strong>2. How long each note lasts.</strong> Every note is built from up to three "
        "parts, and only two of them affect the length. The <strong>head</strong> is hollow (long) "
        "or filled (shorter). The <strong>tails</strong> &mdash; the little flags, or the beams "
        "joining notes together &mdash; halve it again for each one. The <strong>stem</strong>, the "
        "plain vertical line, changes nothing at all: a minim is hollow and has a stem, and it is "
        "still 2 beats.</p>" + F_VALUES + F_DOT +
        "<p><strong>3. Simple or compound.</strong> This is the distinction examiners ask for most "
        "often, and it is decided by the top number alone.</p>" + F_SIMPLE + F_COMPOUND +
        "<p><strong>4. An anacrusis.</strong> A short, incomplete bar before the first full one.</p>"
        + F_ANACRUSIS),
    "steps": [
        "Find the two stacked numbers just after the clef. That is the time signature.",
        "Read the top number: that is how many beats are in each bar.",
        "Is the top number 2, 3 or 4 (simple) or 6, 9 or 12 (compound)?",
        "Look at the very first bar. If it is short, that is an anacrusis.",
    ],
}

WORKED = [{
    "difficulty": "bronze",
    "question": ("Work out the time signature of this extract, and say how many beats are in each "
                 "bar.<br>" + Q_34),
    "steps": [
        {"label": "Step 1 — find it",
         "content": "<p>Look immediately after the clef. Two numbers are stacked there: 3 over 4.</p>"},
        {"label": "Step 2 — read the top number",
         "content": "<p>The top number is 3, so there are <strong>three beats in every bar</strong>. "
                    "Count the notes between the bar lines and you will find three.</p>"},
        {"label": "Step 3 — read the bottom number",
         "content": "<p>The bottom number is 4, which means the beat is a crotchet. So: three "
                    "crotchet beats per bar.</p>"},
        {"label": "Answer",
         "content": "<p>3/4 &mdash; three crotchet beats in every bar. Because the top number is 3, "
                    "this is <strong>simple</strong> time.</p>"},
    ],
}]

BANK = {
    "bronze": [
        {"input_type": "multiple_choice", "passage_id": "q-34",
         "question": "Look at Extract 1. What is the time signature?",
         "options": ["2/4", "3/4", "4/4", "6/8"], "solutions": [1],
         "explanation": "The two stacked numbers just after the clef read 3 over 4. Three crotchet "
                        "beats in every bar — count the notes between the bar lines and you get three."},
        {"input_type": "multiple_choice", "passage_id": "q-34",
         "question": "Look at Extract 1 again. How many beats are in each bar?",
         "options": ["Two", "Three", "Four", "Six"], "solutions": [1],
         "explanation": "The TOP number of a time signature tells you the number of beats. Here it is "
                        "3, so three beats per bar."},
        {"input_type": "multiple_choice", "passage_id": "teach-values",
         "question": "In the figure above, how many crotchets last as long as one semibreve?",
         "options": ["Two", "Three", "Four", "Eight"], "solutions": [2],
         "explanation": "A semibreve is 4 beats and a crotchet is 1, so four crotchets fill the same "
                        "time as one semibreve. Each value on the ladder is half the one above it."},
    ],
    "silver": [
        {"input_type": "multiple_choice", "passage_id": "q-98",
         "question": "Look at Extract 2. Is this simple or compound time, and how do you know?",
         "options": ["Simple — the top number is 9",
                     "Compound — the top number is 9, and the notes group in threes",
                     "Simple — there are quavers in the bar",
                     "Compound — the bottom number is 8"], "solutions": [1],
         "explanation": "The top number decides it. 6, 9 or 12 means compound, so each beat divides "
                        "into three — and you can see the quavers beamed in groups of three. The "
                        "bottom number tells you which note gets the beat, not simple versus compound."},
        {"input_type": "multiple_choice", "passage_id": "q-dot",
         "question": "Look at Extract 3. How many beats does the first note last?",
         "options": ["Two", "Three", "Four", "One and a half"], "solutions": [1],
         "explanation": "It is a minim (2 beats) with a dot after it. A dot adds half the note's value "
                        "again, so 2 + 1 = 3 beats. The rest of the bar is a single crotchet, making 4."},
    ],
    "gold": [
        {"input_type": "multiple_choice", "passage_id": "q-anac",
         "question": "Look at Extract 4. What is unusual about the first bar?",
         "options": ["It is missing a time signature",
                     "It is an anacrusis — an incomplete bar before the first full one",
                     "It contains a triplet",
                     "It is in a different time signature from the rest"], "solutions": [1],
         "explanation": "The time signature is 4/4, but the opening bar holds only two crotchet beats. "
                        "An incomplete opening bar is an anacrusis, also called an upbeat or pick-up. "
                        "The music begins before the first complete bar."},
        {"input_type": "multiple_choice", "passage_id": "teach-simple-compound",
         "question": "A piece is in 12/8. Using the figures above, how many beats per bar does it have, "
                     "and how does each one divide?",
         "options": ["Twelve beats, each dividing into two",
                     "Four beats, each dividing into three",
                     "Three beats, each dividing into four",
                     "Six beats, each dividing into two"], "solutions": [1],
         "explanation": "In compound time the top number counts quavers, not beats: twelve quavers in "
                        "threes gives four beats per bar, each a dotted crotchet. Same logic as the 6/8 "
                        "figure, which has six quavers making two beats."},
    ],
}

PD = {"passages": PASSAGES, "method_card": METHOD, "worked_examples": WORKED,
      "problem_bank": BANK, "exam_context": {
          "title": "What Section A asks",
          "content": "<p>You may be shown up to 12 bars and asked for the time signature, the number "
                     "of beats in a bar, whether the metre is simple or compound, or to name a "
                     "rhythmic feature such as an anacrusis or a dotted rhythm.</p>"}}


def main():
    sb = get_client()
    unit = [u for u in sb.table("units").select("id,slug").execute().data
            if u["slug"] == "score-reading"][0]["id"]
    row = sb.table("lessons").select("id,title,practice_data") \
        .eq("unit_id", unit).eq("lesson_number", 1).single().execute().data

    if "--restore" in sys.argv:
        with open(BACKUP, "r", encoding="utf-8") as f:
            sb.table("lessons").update({"practice_data": json.load(f)}).eq("id", row["id"]).execute()
        print("restored the original L1")
        return

    if not os.path.exists(BACKUP):
        with open(BACKUP, "w", encoding="utf-8") as f:
            json.dump(row["practice_data"], f)
        print("backed up original ->", BACKUP)

    n = sum(len(v) for v in BANK.values())
    assert n == 7, n
    for tier in BANK:
        for q in BANK[tier]:
            assert q["passage_id"] in {p["id"] for p in PASSAGES}, q["passage_id"]
            assert 0 <= q["solutions"][0] < len(q["options"])
            assert q["explanation"]
    sb.table("lessons").update({"practice_data": PD}).eq("id", row["id"]).execute()
    print("PROTOTYPE applied to score-reading L1 (%s)" % row["id"][:8])
    print("  %d passages, %d questions, %d worked example" % (len(PASSAGES), n, len(WORKED)))
    print("  restore with: python build_score_reading_L1.py --restore")


if __name__ == "__main__":
    main()
