# -*- coding: utf-8 -*-
"""Score Reading L1, rebuilt around play-along notation.

Designed from scratch rather than patched. AQA Section A is a listening paper:
notation appears WITH music playing, and the questions join what you hear to
what you see. So the lesson teaches the first skill that makes any of that
possible — keeping your place in a moving score — before it names a single
symbol. Symbols come later in the unit, once they mean something.

Every example plays, with a highlight moving note by note. Nothing here can be
answered from a definition; you have to follow.

    python build_score_reading_L1_play.py            apply
    python build_score_reading_L1_play.py --restore  put the previous version back
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client
from notation import playable, card, figure

BACKUP = os.path.join(HERE, "_score_reading_L1_play_backup.json")
H = "X:1\nT:\nM:4/4\nL:1/4\nK:C\n"

# ---------------------------------------------------------- teaching -------
T_STEADY = playable(H + "C C C C |", [(60, 1)] * 4, tempo=92,
                    title="One note, one beat",
                    caption="Four notes, all the same length. The highlight moves at a steady walking pace "
                            "&mdash; that pace is the <b>beat</b>.")

T_LONG = playable(H + "C C C2 |", [(60, 1), (60, 1), (60, 2)], tempo=92,
                  title="A longer note holds the highlight",
                  caption="The third note is hollow, and the highlight stays on it for twice as long. "
                          "You can hear it and see it at the same time.")

T_SHAPE = playable(H + "C D E F | G4 |", [(60, 1), (62, 1), (64, 1), (65, 1), (67, 4)], tempo=100,
                   title="Higher on the page means higher in sound",
                   caption="The notes climb the stave and the sound climbs with them. This is the single "
                           "most useful thing a score tells you.")

T_REST = playable(H + "C z C z |", [(60, 1), (None, 1), (60, 1), (None, 1)], tempo=92,
                  title="Silence is written down too",
                  caption="Where the sound stops, the highlight goes out. Those gaps are <b>rests</b> "
                          "&mdash; silence is notated just as carefully as sound.")

# ------------------------------------------------------------ extracts -----
E_A = playable(H + "C D C E | D4 |", [(60, 1), (62, 1), (60, 1), (64, 1), (62, 4)], tempo=96,
               title="Extract A", caption="", hint="Play as often as you like.")
E_B = playable(H + "C C2 C | C4 |", [(60, 1), (60, 2), (60, 1), (60, 4)], tempo=96,
               title="Extract B", caption="", hint="Play as often as you like.")
E_C = playable(H + "G F E D | C4 |", [(67, 1), (65, 1), (64, 1), (62, 1), (60, 4)], tempo=96,
               title="Extract C", caption="", hint="Play as often as you like.")
E_D = playable(H + "C D E F | G2 G2 | A4 |",
               [(60, 1), (62, 1), (64, 1), (65, 1), (67, 2), (67, 2), (69, 4)], tempo=104,
               title="Extract D", caption="", hint="Play as often as you like.")
E_E = playable(H + "C E G E | C4 |", [(60, 1), (64, 1), (67, 1), (64, 1), (60, 4)], tempo=100,
               title="Extract E", caption="", hint="Play as often as you like.")

# --- follow-and-check: the audio deliberately DIFFERS from the engraving -----
# playable() takes the engraving and the sounding notes separately, so a
# mismatch needs no new machinery. This is the hard exercise: it cannot be
# guessed from the options, and it forces genuine simultaneous reading and
# listening rather than "count the highlights".
# Engraved:  C D E F | G F E D | C E G c | G4
# Played:    bar 3 has A instead of G on beat 3.
E_F = playable(H + "C D E F | G F E D | C E G c | G4 |",
               [(60, 1), (62, 1), (64, 1), (65, 1),
                (67, 1), (65, 1), (64, 1), (62, 1),
                (60, 1), (64, 1), (69, 1), (72, 1),      # <- 69 where the score prints G (67)
                (67, 4)], tempo=112,
               title="Extract F",
               caption="The performance contains <b>one</b> note that does not match the printed score.",
               hint="Follow the printed notes as it plays. Something will not line up.")

# Engraved:  a steady climb. Played: bar 2 is rhythmically wrong (two beats swapped for one long).
E_G = playable(H + "C D E F | G A B c | d4 |",
               [(60, 1), (62, 1), (64, 1), (65, 1),
                (67, 2), (False, 0), (71, 1), (72, 1),   # <- G held 2 beats; the printed A never sounds
                (74, 4)], tempo=112,
               title="Extract G",
               caption="Again, the performance departs from the score once.",
               hint="This time listen to the rhythm as much as the pitch.")

PASSAGES = [
    {"id": "t-beat", "label": "The beat", "text": T_STEADY + T_LONG},
    {"id": "t-shape", "label": "Shape and silence", "text": T_SHAPE + T_REST},
    {"id": "e-a", "label": "Extract A", "text": E_A},
    {"id": "e-b", "label": "Extract B", "text": E_B},
    {"id": "e-c", "label": "Extract C", "text": E_C},
    {"id": "e-d", "label": "Extract D", "text": E_D},
    {"id": "e-e", "label": "Extract E", "text": E_E},
    {"id": "e-f", "label": "Extract F", "text": E_F},
    {"id": "e-g", "label": "Extract G", "text": E_G},
]

METHOD = {
    "title": "Following a score while it plays",
    "content": (
        "<p>In the exam the music is playing while you look at the notation. You are never asked to "
        "read it in silence. So the first skill is simply <strong>keeping your place</strong>: "
        "knowing which mark on the page is making the sound you are hearing right now.</p>"
        "<p>Press play on each example below and watch. Do not try to name anything yet.</p>"
        + T_STEADY + T_LONG + T_SHAPE + T_REST +
        "<p>Once you can follow a line, everything else in this unit is just labelling what you are "
        "already tracking.</p>"),
    "steps": [
        "Play the extract once without trying to answer anything. Just watch the highlight.",
        "Play it again and tap the beat with your finger. Notice which notes hold for more than one tap.",
        "Play it a third time and watch whether the notes climb, fall, or stay level.",
        "Only now read the question.",
    ],
}

WORKED = [{
    "difficulty": "bronze",
    "question": "How many notes are in this extract, and which one is longest?<br>" + E_B,
    "steps": [
        {"label": "Step 1 — count the highlights",
         "content": "<p>Play it and count how many times a note lights up. Four.</p>"},
        {"label": "Step 2 — watch how long each stays lit",
         "content": "<p>The second note stays lit for two taps of the beat while the first and third "
                    "get one each. The last one holds longest of all.</p>"},
        {"label": "Step 3 — check it against the page",
         "content": "<p>The notes that held longer are the hollow ones. Filled notes went past quickly. "
                    "That is the clue you will use for the rest of the unit.</p>"},
        {"label": "Answer",
         "content": "<p>Four notes. The last is longest, and the second is longer than the first and "
                    "third.</p>"},
    ],
}]

BANK = {
    "bronze": [
        {"input_type": "multiple_choice", "passage_id": "e-a",
         "question": "Play Extract A. How many notes are there?",
         "options": ["Four", "Five", "Six", "Seven"], "solutions": [1],
         "explanation": "Five notes light up: four short ones, then a long one to finish. Counting the "
                        "highlights is the most reliable way to check you are following the right line."},
        {"input_type": "multiple_choice", "passage_id": "e-c",
         "question": "Play Extract C. Does the tune rise or fall?",
         "options": ["It rises throughout", "It falls throughout",
                     "It rises then falls", "It stays on the same note"], "solutions": [1],
         "explanation": "Each note sits lower on the stave than the one before, and the sound drops with "
                        "it. Higher on the page always means higher in pitch."},
        {"input_type": "multiple_choice", "passage_id": "e-b",
         "question": "Play Extract B. Which note is held longest?",
         "options": ["The first", "The second", "The third", "The last"], "solutions": [3],
         "explanation": "The final note keeps the highlight for four beats — a whole bar. The second note "
                        "holds for two, and the first and third for one each."},
    ],
    "silver": [
        {"input_type": "multiple_choice", "passage_id": "e-d",
         "question": "Play Extract D. In which bar does the tune stop climbing and hold?",
         "options": ["Bar 1", "Bar 2", "Bar 3", "It never holds"], "solutions": [1],
         "explanation": "Bar 1 climbs a note at a time. In bar 2 the highlight stays on the same pitch for "
                        "two longer notes before moving up once more in bar 3. Bar lines are the thin "
                        "vertical strokes crossing the stave."},
        {"input_type": "multiple_choice", "passage_id": "e-e",
         "question": "Play Extract E. Which describes its shape best?",
         "options": ["Rises, then falls back", "Falls, then rises back",
                     "Rises all the way", "Stays level"], "solutions": [0],
         "explanation": "The line climbs for three notes, then comes back down to where it started. You can "
                        "see the arch on the page and hear it at the same time — that matching is the "
                        "whole skill."},
    ],
    "gold": [
        {"input_type": "multiple_choice", "passage_id": "e-a",
         "question": "Play Extract A again. Its last note is hollow and the others are filled in. What did "
                     "you hear that matches?",
         "options": ["The hollow note was louder",
                     "The hollow note was higher",
                     "The hollow note lasted longer",
                     "The hollow note was played by a different instrument"], "solutions": [2],
         "explanation": "A hollow head means a longer note, and you heard it hold while the filled ones "
                        "went past in a beat each. You have just read a note value off the page by ear."},
        {"input_type": "multiple_choice", "passage_id": "e-f",
         "question": "Play Extract F. The performance departs from the printed score in exactly one "
                     "place. In which bar?",
         "options": ["Bar 1", "Bar 2", "Bar 3", "Bar 4"], "solutions": [2],
         "explanation": "Bar 3 is printed C&ndash;E&ndash;G&ndash;C, climbing evenly. What sounds on the "
                        "third beat is a note higher than the printed G, so the line jumps further than "
                        "the page says. Following the printed notes while listening is exactly what "
                        "Section A asks of you when it prints an extract of the music being played."},
        {"input_type": "multiple_choice", "passage_id": "e-g",
         "question": "Play Extract G. Again the performance departs from the score once. What is wrong, "
                     "and where?",
         "options": ["Bar 1 — a note is played too short",
                     "Bar 2 — a note is held too long and the next one is missed",
                     "Bar 3 — the last note is too low",
                     "Bar 2 — two notes are swapped in order"], "solutions": [1],
         "explanation": "The score prints four separate notes climbing through bar 2. In the performance "
                        "the first of them is held for two beats, so the note that should follow it never "
                        "sounds — the bar still lasts four beats, which is why it is easy to miss. "
                        "Checking rhythm against the page, not just pitch, is the harder half of the skill."},
    ],
}

PD = {"passages": PASSAGES, "method_card": METHOD, "worked_examples": WORKED,
      "problem_bank": BANK,
      "exam_context": {"title": "Why this comes first",
                       "content": "<p>Section A plays music and may show you up to 12 bars of it. Every "
                                  "question about that notation assumes you can keep your place while it "
                                  "sounds. Get that, and naming time signatures and note values is "
                                  "straightforward.</p>"}}


def main():
    sb = get_client()
    unit = [u for u in sb.table("units").select("id,slug").execute().data
            if u["slug"] == "score-reading"][0]["id"]
    row = sb.table("lessons").select("id,practice_data").eq("unit_id", unit) \
        .eq("lesson_number", 1).single().execute().data

    if "--restore" in sys.argv:
        with open(BACKUP, "r", encoding="utf-8") as f:
            sb.table("lessons").update({"practice_data": json.load(f)}).eq("id", row["id"]).execute()
        print("restored")
        return
    if not os.path.exists(BACKUP):
        with open(BACKUP, "w", encoding="utf-8") as f:
            json.dump(row["practice_data"], f)
        print("backed up ->", BACKUP)

    ids = {p["id"] for p in PASSAGES}
    n = 0
    for tier in BANK:
        for q in BANK[tier]:
            n += 1
            assert q["passage_id"] in ids, q["passage_id"]
            assert 0 <= q["solutions"][0] < len(q["options"])
            assert q["explanation"]
    sb.table("lessons").update({
        "practice_data": PD,
        "title": "Following a Score: Keeping Your Place While the Music Plays",
        "description": "Learn to follow notation while it sounds — the skill every other score-reading "
                       "question depends on. Every example plays, with the notes lighting up as you hear them.",
    }).eq("id", row["id"]).execute()
    print("applied: %d passages, %d questions" % (len(PASSAGES), n))


if __name__ == "__main__":
    main()
