# -*- coding: utf-8 -*-
"""Score Reading L2-L4, on the ladder established by L1.

L1 taught keeping your place while the music sounds. These name what the
student is already tracking, in the order that makes each one learnable:
  L2  rhythm    - how long, read off the page
  L3  pitch     - how far, and which key
  L4  the rest  - dynamics, articulation, clefs, and a longer extract

Every example plays. Gold in each lesson is follow-and-check: the performance
departs from the printed score once, and the student says where. That cannot be
guessed or answered from a definition.

    python build_score_reading_L2_L4.py            apply
    python build_score_reading_L2_L4.py --restore  put the originals back
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client
from notation import playable, figure, card, row

BACKUP = os.path.join(HERE, "_score_reading_L2_L4_backup.json")


def H(m="4/4", k="C"):
    return "X:1\nT:\nM:%s\nL:1/4\nK:%s\n" % (m, k)


def mc(title, content, steps):
    return {"title": title, "content": content, "steps": steps}


def q(pid, text, opts, correct, expl):
    return {"input_type": "multiple_choice", "passage_id": pid, "question": text,
            "options": opts, "solutions": [correct], "explanation": expl}


# =========================================================== L2 — RHYTHM ====
L2_VALUES = row([(H() + "%s|" % v, c) for v, c in [
    ("G4", "semibreve<br><b>4 beats</b><br>hollow, no stem"),
    ("G2", "minim<br><b>2 beats</b><br>hollow, with stem"),
    ("G", "crotchet<br><b>1 beat</b><br>filled, with stem"),
    ("G/2", "quaver<br><b>half a beat</b><br>filled, one tail"),
    ("G//", "semiquaver<br><b>quarter beat</b><br>filled, two tails")]],
    "The five note values",
    "Only two things change the length: is the <b>head</b> hollow or filled, and how many "
    "<b>tails</b>? The <b>stem</b> is just a handle &mdash; a minim is hollow, has a stem, and is "
    "still 2 beats.")

L2_HEAR = playable(H() + "G4 | G2 G2 | G G G G |",
                   [(67, 4), (67, 2), (67, 2), (67, 1), (67, 1), (67, 1), (67, 1)], tempo=96,
                   title="The same bar, three ways",
                   caption="One semibreve, then two minims, then four crotchets. Every bar lasts the "
                           "same time &mdash; only the number of notes inside it changes.")

L2_DOT = row([(H() + "G2|", "minim<br><b>2 beats</b>"),
              (H() + "G3|", "dotted minim<br><b>3 beats</b><br>2 + half of 2"),
              (H() + "G|", "crotchet<br><b>1 beat</b>"),
              (H() + "G3/2|", "dotted crotchet<br><b>1&frac12; beats</b><br>1 + half of 1")],
             "A dot adds half of whatever the note is worth",
             "It does <b>not</b> always add one beat. Add half the note's own value.")

L2_DOTHEAR = playable(H() + "G2 G2 | G3 G |", [(67, 2), (67, 2), (67, 3), (67, 1)], tempo=92,
                      title="Hear the dot",
                      caption="Bar 1 is two even minims. Bar 2 is the same minim with a dot, so it runs "
                              "on into a third beat before the last note arrives.")

L2_SIMPLE = playable(H("2/4") + "GG GG |", [(67, .5)] * 4, tempo=88,
                     title="Simple time &mdash; each beat splits in 2",
                     caption="A top number of 2, 3 or 4. Count 1-and 2-and.")
L2_COMP = playable(H("6/8") + "GGG GGG |", [(67, 1 / 3.0)] * 6, tempo=88,
                   title="Compound time &mdash; each beat splits in 3",
                   caption="A top number of 6, 9 or 12. Count 1-and-a 2-and-a. This is the distinction "
                           "Section A asks for most often.")

L2_QA = playable(H("3/4") + "G G G | A2 G |", [(67, 1), (67, 1), (67, 1), (69, 2), (67, 1)],
                 tempo=96, title="Extract A", caption="", hint="Play as often as you like.")
L2_QB = playable(H() + "G3 G | G2 G2 |", [(67, 3), (67, 1), (67, 2), (67, 2)], tempo=96,
                 title="Extract B", caption="", hint="Play as often as you like.")
L2_QC = playable(H("6/8") + "GGG GGG | A3 |", [(67, 1 / 3.0)] * 6 + [(69, 1)], tempo=84,
                 title="Extract C", caption="", hint="Play as often as you like.")
# gold: printed as four even crotchets in bar 2; played as a dotted pair
L2_QD = playable(H() + "C D E F | G G G G | c4 |",
                 [(60, 1), (62, 1), (64, 1), (65, 1),
                  (67, 1.5), (67, .5), (67, 1), (67, 1),
                  (72, 4)], tempo=104,
                 title="Extract D",
                 caption="The performance departs from the printed rhythm in one bar.",
                 hint="The pitches are all correct. Listen to the lengths.")

L2 = {
    "title": "Reading Rhythm: How Long Each Note Lasts",
    "description": "Note values, dotted notes and the difference between simple and compound time — "
                   "each one played, so you hear the length as you see it.",
    "pd": {
        "passages": [
            {"id": "t-values", "label": "Note values", "text": L2_VALUES + L2_HEAR},
            {"id": "t-dot", "label": "Dotted notes", "text": L2_DOT + L2_DOTHEAR},
            {"id": "t-metre", "label": "Simple and compound", "text": L2_SIMPLE + L2_COMP},
            {"id": "q-a", "label": "Extract A", "text": L2_QA},
            {"id": "q-b", "label": "Extract B", "text": L2_QB},
            {"id": "q-c", "label": "Extract C", "text": L2_QC},
            {"id": "q-d", "label": "Extract D", "text": L2_QD},
        ],
        "method_card": mc(
            "Reading how long a note lasts",
            "<p>In Lesson 1 you followed a line while it played. Now put names to the lengths you were "
            "already hearing.</p>" + L2_VALUES + L2_HEAR + L2_DOT + L2_DOTHEAR +
            "<p>Then the metre: how the beats themselves are grouped and divided.</p>" +
            L2_SIMPLE + L2_COMP,
            ["Find the time signature. The top number is how many beats fill a bar.",
             "Is the top number 2, 3 or 4 (simple) or 6, 9 or 12 (compound)?",
             "For each note, check the head first, then count the tails.",
             "Look for dots. A dot adds half of that note's own value."]),
        "worked_examples": [{
            "difficulty": "bronze",
            "question": "How many beats does the first note of this extract last?<br>" + L2_QB,
            "steps": [
                {"label": "Step 1 — read the head",
                 "content": "<p>It is hollow, so it is at least a minim: 2 beats.</p>"},
                {"label": "Step 2 — check for a dot",
                 "content": "<p>There is a dot after it. A dot adds half the note's own value, and half "
                            "of 2 is 1.</p>"},
                {"label": "Step 3 — confirm by ear",
                 "content": "<p>Play it and tap the beat. The first note holds for three taps before the "
                            "next one arrives.</p>"},
                {"label": "Answer", "content": "<p>Three beats &mdash; a dotted minim.</p>"}]}],
        "problem_bank": {
            "bronze": [
                q("t-values", "A note has a hollow head and a stem, and no tail. How long is it?",
                  ["4 beats", "2 beats", "1 beat", "Half a beat"], 1,
                  "That is a minim: 2 beats. Hollow means long, and the stem — the plain vertical line — "
                  "never changes the length. Only a semibreve, which has no stem at all, is longer."),
                q("q-b", "Play Extract B. How many beats does the first note last?",
                  ["Two", "Three", "Four", "One and a half"], 1,
                  "A hollow head with a dot: the minim is 2 beats and the dot adds half of 2, making 3. "
                  "Tap the beat while it plays and you will feel it hold for three."),
                q("t-metre", "A piece has a 6/8 time signature. Is it simple or compound time?",
                  ["Simple — the bottom number is 8", "Compound — the top number is 6",
                   "Simple — there are six beats", "Compound — it has quavers"], 1,
                  "The TOP number decides it: 6, 9 or 12 means compound, so each beat divides into three. "
                  "The bottom number only tells you which note gets the beat."),
            ],
            "silver": [
                q("q-a", "Play Extract A. How many beats are in each bar?",
                  ["Two", "Three", "Four", "Six"], 1,
                  "The time signature reads 3 over 4 — three crotchet beats per bar. Count the highlight: "
                  "it moves three times before the bar line each time."),
                q("q-c", "Play Extract C. How do the beats divide?",
                  ["Into two, so it is simple time", "Into three, so it is compound time",
                   "Into four, so it is simple time", "They do not divide"], 1,
                  "You can hear the quavers grouping in threes, and see them beamed in threes on the page. "
                  "6/8 is compound duple: two beats a bar, each a dotted crotchet worth three quavers."),
                q("t-dot", "A dotted crotchet lasts how long?",
                  ["Two beats", "One and a half beats", "Three beats", "Half a beat"], 1,
                  "A crotchet is 1 beat and the dot adds half of 1. The rule is always 'half of the note's "
                  "own value' — which is why the same dot makes a minim 3 but a crotchet 1½."),
            ],
            "gold": [
                q("q-d", "Play Extract D. The pitches are all correct, but one bar is not played as "
                         "printed. Which one, and what changed?",
                  ["Bar 1 — the notes are played too fast",
                   "Bar 2 — the first note is lengthened and the second shortened",
                   "Bar 3 — the last note is too short",
                   "Bar 2 — a note is missing altogether"], 1,
                  "Bar 2 is printed as four even crotchets. What sounds is a long-short pair followed by "
                  "two even notes — the first note borrows half a beat from the second, giving the "
                  "dotted, lopsided feel. The bar still totals four beats, which is exactly why this is "
                  "easy to miss unless you are reading along."),
                q("t-metre", "Why can a piece in 3/4 and a piece in 6/8 both have six quavers in a bar, "
                             "yet feel completely different?",
                  ["They cannot — six quavers always sound the same",
                   "3/4 groups them as three pairs, 6/8 as two threes",
                   "6/8 is always faster than 3/4",
                   "3/4 is simple because it uses crotchets and 6/8 is compound because it uses quavers"], 1,
                  "Same six quavers, different grouping. 3/4 is three crotchet beats each splitting in "
                  "two; 6/8 is two dotted-crotchet beats each splitting in three. The beaming on the page "
                  "shows you which, and the accent pattern lets you hear it."),
            ]}}}

# ============================================================ L3 — PITCH ====
L3_STEP = playable(H() + "C D E F | G4 |", [(60, 1), (62, 1), (64, 1), (65, 1), (67, 4)], tempo=100,
                   title="Moving by step",
                   caption="Each note is the very next line or space up. Stepwise movement sounds smooth "
                           "and joined &mdash; the technical word is <b>conjunct</b>.")
L3_LEAP = playable(H() + "C G C' G | C4 |", [(60, 1), (67, 1), (72, 1), (67, 1), (60, 4)], tempo=100,
                   title="Moving by leap",
                   caption="These jump several lines at a time. Leaping movement sounds bold and angular "
                           "&mdash; the technical word is <b>disjunct</b>.")
L3_SHAPE = playable(H() + "C E G c | G E C2 |",
                    [(60, 1), (64, 1), (67, 1), (72, 1), (67, 1), (64, 1), (60, 2)], tempo=104,
                    title="The shape on the page is the shape you hear",
                    caption="This one arches: up to a peak, then back down. You can see it before you "
                            "hear it, which is what makes following a score worth doing.")
L3_KEY = card(figure(H("4/4", "D") + "D E ^F G | A4 |", ring=[("keySig", "the key signature")],
                     width=1200),
              "The key signature sits between the clef and the time signature",
              "These sharps or flats apply to every bar in the piece, not just the first. Two sharps "
              "means D major (or B minor).")
L3_ACC = card(figure(H() + "C ^C D _E |", ring=[("accid", "an accidental")], width=1100),
              "An accidental changes one note, there and then",
              "A sharp, flat or natural written next to a note applies for the rest of that bar only. "
              "Accidentals appearing repeatedly often signal a change of key.")

L3_QA = playable(H() + "C D E D | C4 |", [(60, 1), (62, 1), (64, 1), (62, 1), (60, 4)], tempo=100,
                 title="Extract A", caption="", hint="Play as often as you like.")
L3_QB = playable(H() + "C G E c | G4 |", [(60, 1), (67, 1), (64, 1), (72, 1), (67, 4)], tempo=100,
                 title="Extract B", caption="", hint="Play as often as you like.")
L3_QC = playable(H() + "G F E D | C E G c |",
                 [(67, 1), (65, 1), (64, 1), (62, 1), (60, 1), (64, 1), (67, 1), (72, 1)], tempo=104,
                 title="Extract C", caption="", hint="Play as often as you like.")
# gold: printed stepwise climb; bar 2 beat 2 sounds a third too high
L3_QD = playable(H() + "C D E F | G A B c | d4 |",
                 [(60, 1), (62, 1), (64, 1), (65, 1),
                  (67, 1), (72, 1), (71, 1), (72, 1),
                  (74, 4)], tempo=108,
                 title="Extract D",
                 caption="One printed note is not the pitch you hear.",
                 hint="The rhythm is correct throughout. Follow the shape.")

L3 = {
    "title": "Reading Pitch: Steps, Leaps, Shape and Key",
    "description": "Tell stepwise movement from leaps, read the shape of a line off the page, and find "
                   "the key signature and accidentals — with every example played.",
    "pd": {
        "passages": [
            {"id": "t-move", "label": "Step and leap", "text": L3_STEP + L3_LEAP},
            {"id": "t-shape", "label": "Shape", "text": L3_SHAPE},
            {"id": "t-key", "label": "Key and accidentals", "text": L3_KEY + L3_ACC},
            {"id": "q-a", "label": "Extract A", "text": L3_QA},
            {"id": "q-b", "label": "Extract B", "text": L3_QB},
            {"id": "q-c", "label": "Extract C", "text": L3_QC},
            {"id": "q-d", "label": "Extract D", "text": L3_QD},
        ],
        "method_card": mc(
            "Reading pitch and shape",
            "<p>Higher on the page is higher in sound. Everything in this lesson follows from that.</p>"
            + L3_STEP + L3_LEAP + L3_SHAPE +
            "<p>Then two things that tell you which notes the piece is using at all.</p>"
            + L3_KEY + L3_ACC,
            ["Play it once and just watch whether the line rises, falls, or arches.",
             "Ask whether it moves to the next line or space (step) or jumps (leap).",
             "Look between the clef and the time signature for the key signature.",
             "Watch for sharps, flats or naturals written in front of individual notes."]),
        "worked_examples": [{
            "difficulty": "bronze",
            "question": "Is this melody mostly stepwise or mostly leaping?<br>" + L3_QB,
            "steps": [
                {"label": "Step 1 — look before you listen",
                 "content": "<p>The notes are not on neighbouring lines and spaces; there are gaps "
                            "between them.</p>"},
                {"label": "Step 2 — play it",
                 "content": "<p>It sounds bold and jumpy rather than smooth. Each move covers "
                            "noticeable distance.</p>"},
                {"label": "Step 3 — name it",
                 "content": "<p>Movement by leap is <strong>disjunct</strong>. Movement by step is "
                            "<strong>conjunct</strong>. Section A uses both words.</p>"},
                {"label": "Answer", "content": "<p>Mostly leaping — disjunct.</p>"}]}],
        "problem_bank": {
            "bronze": [
                q("q-a", "Play Extract A. How does the melody move?",
                  ["By leap throughout", "By step throughout", "It stays on one note",
                   "It leaps, then steps"], 1,
                  "Every note moves to the next line or space, up then back down. Smooth, joined "
                  "movement like this is called conjunct."),
                q("q-b", "Play Extract B. How does this melody move?",
                  ["By step throughout", "By leap", "It stays on one note", "It only falls"], 1,
                  "The notes jump across several lines at a time, and it sounds angular. Movement by "
                  "leap is called disjunct."),
                q("t-key", "Where in a score do you find the key signature?",
                  ["At the end of the first bar", "Between the clef and the time signature",
                   "Above the top stave", "Next to every note it affects"], 1,
                  "It sits immediately after the clef, before the time signature, and it applies for the "
                  "whole piece — not just the first bar."),
            ],
            "silver": [
                q("q-c", "Play Extract C. Which best describes its shape?",
                  ["It rises, then falls", "It falls, then rises", "It rises throughout",
                   "It stays level"], 1,
                  "Bar 1 descends step by step; bar 2 climbs back up. Being able to describe the contour "
                  "of a line — rising, falling, arching, or a wave — earns marks in Section A."),
                q("t-key", "A sharp is written in front of one note in the middle of a bar. How far does "
                           "it apply?",
                  ["To that note only", "To that note and any repeat of it for the rest of that bar",
                   "To the rest of the piece", "To the whole system"], 1,
                  "An accidental holds for the remainder of the bar it appears in, then lapses at the "
                  "next bar line. That is what distinguishes it from a key signature."),
                q("t-move", "Which word describes a melody that moves mainly by step?",
                  ["Disjunct", "Conjunct", "Chromatic", "Syncopated"], 1,
                  "Conjunct means stepwise; disjunct means leaping. Using the right term rather than "
                  "'it goes up smoothly' is what turns a description into a mark."),
            ],
            "gold": [
                q("q-d", "Play Extract D. The rhythm is correct throughout, but one printed note is not "
                         "the pitch you hear. Where?",
                  ["Bar 1, beat 2", "Bar 2, beat 2", "Bar 2, beat 4", "Bar 3"], 1,
                  "The score prints bar 2 as a continuing stepwise climb: G, A, B, C. What sounds on the "
                  "second beat is well above the printed A — the line jumps up and then has to come back "
                  "down to B, breaking the smooth ascent you can see on the page."),
                q("t-shape", "Why is describing the shape of a melody more useful in the exam than saying "
                             "it 'sounds nice'?",
                  ["Shape is easier to spell",
                   "Shape is a musical feature you can point to in the score and hear at the same time",
                   "Examiners dislike opinions", "Shape is worth double marks"], 1,
                  "Section A rewards naming a feature and saying where it happens. 'The melody rises "
                  "stepwise to a peak in bar 3, then falls by leap' is evidence; 'it sounds nice' is not."),
            ]}}}

# =============================================== L4 — EXPRESSION & FORCES ===
L4_DYN = card(figure(H() + "!p!C D !f!E F | G4 |", ring=[("dynam", "a dynamic marking")], width=1300),
              "Dynamics are letters below the stave",
              "<b>pp</b> very quiet &middot; <b>p</b> quiet &middot; <b>mp</b> moderately quiet &middot; "
              "<b>mf</b> moderately loud &middot; <b>f</b> loud &middot; <b>ff</b> very loud. They tell "
              "the player how loud, from that point on.")
L4_DYNHEAR = playable(H() + "!p!C D E F | !f!G A B c |",
                      [(60, 1), (62, 1), (64, 1), (65, 1), (67, 1), (69, 1), (71, 1), (72, 1)],
                      tempo=104, title="Hear the change",
                      caption="The tone here does not actually change volume &mdash; but on the page you "
                              "can see exactly where the composer asked it to.")
L4_ART = card(figure(H() + ".C .D .E .F | (GABc) |", ring=[("artic", "a staccato dot")], width=1300),
              "Articulation says how each note is played",
              "A dot above or below a note means <b>staccato</b> &mdash; short and detached. A curved "
              "line over several different notes is a <b>slur</b>: play them smoothly, joined "
              "(<b>legato</b>).")
L4_ARTHEAR = playable(H() + ".C .D .E .F | (GABc) |",
                      [(60, .55), (62, .55), (64, .55), (65, .55),
                       (67, 1), (69, 1), (71, 1), (72, 1)], tempo=100,
                      title="Short and detached, then smooth",
                      caption="Bar 1 is staccato: each note stops early, leaving a gap. Bar 2 is slurred, "
                              "so the notes run into one another.")
L4_CLEF = row([(H() + "C D E F|", "<b>treble clef</b><br>higher instruments:<br>flute, violin, "
                                 "right hand of a piano"),
               ("X:1\nT:\nM:4/4\nL:1/4\nK:C clef=bass\nC D E F|",
                "<b>bass clef</b><br>lower instruments:<br>cello, bassoon, left hand of a piano")],
              "The clef tells you which pitches the lines mean",
              "The same five lines mean different notes depending on the clef at the start. In an "
              "orchestral score, woodwind sit at the top, then brass, then percussion, with strings at "
              "the bottom.")
L4_EXTRACT = playable(H() + "!p!C D E F | G2 G2 | !f!c B A G | F E D2 | C4 |",
                      [(60, 1), (62, 1), (64, 1), (65, 1), (67, 2), (67, 2),
                       (72, 1), (71, 1), (69, 1), (67, 1), (65, 1), (64, 1), (62, 2), (60, 4)],
                      tempo=100, title="A longer extract",
                      caption="Five bars, with a dynamic change partway. Section A prints extracts like "
                              "this and asks you to describe what you can see and hear.",
                      hint="Play it a few times before answering.")
# gold: printed staccato bar is played smoothly, and one pitch differs
L4_QGOLD = playable(H() + ".C .D .E .F | G A B c | !f!d4 |",
                    [(60, .55), (62, .55), (64, .55), (65, .55),
                     (67, 1), (69, 1), (72, 1), (72, 1),
                     (74, 4)], tempo=104,
                    title="Extract F",
                    caption="The performance departs from the printed score once, in pitch.",
                    hint="The articulation is played correctly. Follow the notes.")

L4 = {
    "title": "Reading Expression and Forces: Dynamics, Articulation and Clefs",
    "description": "Dynamics, staccato and slurs, and what the clef tells you — then a longer extract "
                   "to read the way Section A asks you to.",
    "pd": {
        "passages": [
            {"id": "t-dyn", "label": "Dynamics", "text": L4_DYN + L4_DYNHEAR},
            {"id": "t-art", "label": "Articulation", "text": L4_ART + L4_ARTHEAR},
            {"id": "t-clef", "label": "Clefs", "text": L4_CLEF},
            {"id": "q-ext", "label": "A longer extract", "text": L4_EXTRACT},
            {"id": "q-f", "label": "Extract F", "text": L4_QGOLD},
        ],
        "method_card": mc(
            "Reading expression and forces",
            "<p>By now you can follow a line, read its lengths and read its shape. What is left is "
            "everything the composer wrote <em>around</em> the notes.</p>"
            + L4_DYN + L4_DYNHEAR + L4_ART + L4_ARTHEAR + L4_CLEF,
            ["Scan below the stave for letters — those are dynamics.",
             "Look above and below the note heads for dots (staccato) and curved lines (slurs).",
             "Check the clef at the start of each stave before you read any pitch.",
             "In a full score, read top to bottom: woodwind, brass, percussion, strings."]),
        "worked_examples": [{
            "difficulty": "bronze",
            "question": "Describe what happens to the dynamics in this extract.<br>" + L4_EXTRACT,
            "steps": [
                {"label": "Step 1 — find the letters",
                 "content": "<p>There is a <strong>p</strong> at the very start and an "
                            "<strong>f</strong> at the beginning of bar 3.</p>"},
                {"label": "Step 2 — translate them",
                 "content": "<p><strong>p</strong> is piano, quiet. <strong>f</strong> is forte, loud.</p>"},
                {"label": "Step 3 — say where",
                 "content": "<p>A mark applies from where it appears until the next one. So bars 1-2 are "
                            "quiet and bars 3-5 are loud.</p>"},
                {"label": "Answer",
                 "content": "<p>It begins quietly (p) and becomes loud (f) at bar 3. Naming the marking "
                            "AND the bar is what earns the mark.</p>"}]}],
        "problem_bank": {
            "bronze": [
                q("t-dyn", "What does the marking mf mean?",
                  ["Very quiet", "Moderately quiet", "Moderately loud", "Very loud"], 2,
                  "mf is mezzo-forte: moderately loud. The ladder runs pp, p, mp, mf, f, ff — 'mezzo' "
                  "means moderately, and it softens whichever word follows it."),
                q("t-art", "A dot is printed above a note head. What does it tell the player?",
                  ["Play it louder", "Hold it for half as long again",
                   "Play it short and detached", "Play it smoothly"], 2,
                  "A dot above or below the head means staccato: short and detached. Do not confuse it "
                  "with a dot AFTER the head, which lengthens the note by half its value."),
                q("q-ext", "Play the longer extract. What dynamic does it begin with?",
                  ["f (loud)", "p (quiet)", "mf (moderately loud)", "pp (very quiet)"], 1,
                  "There is a p below the stave at the start, so it begins quiet. The f at bar 3 marks "
                  "where it changes."),
            ],
            "silver": [
                q("q-ext", "In the longer extract, where does the dynamic change and what to?",
                  ["Bar 2, to p", "Bar 3, to f", "Bar 4, to mf", "It never changes"], 1,
                  "The f appears at the start of bar 3 and applies from there onward. A dynamic mark "
                  "holds until the next one, so bars 1-2 are quiet and bars 3-5 loud."),
                q("t-art", "What is the difference between a curved line over several different notes "
                           "and a dot above one note?",
                  ["They mean the same thing",
                   "The curve means play them smoothly joined; the dot means play that note short",
                   "The curve means repeat; the dot means louder",
                   "The curve means slow down; the dot means speed up"], 1,
                  "A slur asks for legato — smooth and connected. A staccato dot asks for the opposite: "
                  "short, with a gap after it. They are often contrasted deliberately within one phrase."),
                q("t-clef", "A stave begins with a bass clef. What does that tell you?",
                  ["The music is quiet", "The music is slow",
                   "The lines represent lower pitches, so a lower instrument or the left hand",
                   "The music has no key signature"], 2,
                  "The clef redefines what the five lines mean. Bass clef indicates lower-sounding parts "
                  "— cello, bassoon, or a pianist's left hand. Always read the clef before any pitch."),
            ],
            "gold": [
                q("q-f", "Play Extract F. The articulation is played correctly, but one printed note is "
                         "not the pitch you hear. Where?",
                  ["Bar 1, beat 1", "Bar 2, beat 3", "Bar 2, beat 4", "Bar 3"], 1,
                  "Bar 2 is printed as a stepwise climb G, A, B, C. On the third beat you hear the top C "
                  "arrive a beat early, so the printed B never sounds and the note repeats instead. The "
                  "staccato bar before it is played exactly as written, which is what makes this one "
                  "harder to locate."),
                q("q-ext", "A Section A question shows you this extract and asks you to 'describe the "
                           "dynamics and articulation'. Which answer would score best?",
                  ["It starts quietly and gets louder, and sounds quite smooth",
                   "It begins p and changes to f at bar 3; the notes are unmarked, so they are played "
                   "normally rather than staccato or slurred",
                   "It is loud and detached", "p, f, staccato, slur"], 1,
                  "The strongest answer names the marking, translates it, and says WHERE it happens. A "
                  "bare list of terms shows recognition but not reading; a vague impression shows "
                  "neither."),
            ]}}}


def main():
    sb = get_client()
    unit = [u for u in sb.table("units").select("id,slug").execute().data
            if u["slug"] == "score-reading"][0]["id"]
    rows = {r["lesson_number"]: r for r in sb.table("lessons")
            .select("id,lesson_number,title,description,practice_data")
            .eq("unit_id", unit).execute().data}

    if "--restore" in sys.argv:
        with open(BACKUP, "r", encoding="utf-8") as f:
            for num, saved in json.load(f).items():
                sb.table("lessons").update(saved).eq("id", rows[int(num)]["id"]).execute()
        print("restored L2-L4")
        return

    if not os.path.exists(BACKUP):
        with open(BACKUP, "w", encoding="utf-8") as f:
            json.dump({str(n): {"title": rows[n]["title"], "description": rows[n]["description"],
                                "practice_data": rows[n]["practice_data"]} for n in (2, 3, 4)}, f)
        print("backed up ->", BACKUP)

    total = 0
    for num, spec in ((2, L2), (3, L3), (4, L4)):
        pd = spec["pd"]
        ids = {p["id"] for p in pd["passages"]}
        n = 0
        for tier in pd["problem_bank"]:
            for item in pd["problem_bank"][tier]:
                n += 1
                assert item["passage_id"] in ids, (num, item["passage_id"])
                assert 0 <= item["solutions"][0] < len(item["options"]), (num, item["question"][:40])
                assert item["explanation"]
        sb.table("lessons").update({"practice_data": pd, "title": spec["title"],
                                    "description": spec["description"]}) \
            .eq("id", rows[num]["id"]).execute()
        print("L%d: %d passages, %d questions" % (num, len(pd["passages"]), n))
        total += n
    print("total questions:", total)


if __name__ == "__main__":
    main()
