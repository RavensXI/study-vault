# -*- coding: utf-8 -*-
"""The last two groups: maths-ocr algebra L9, and score-reading L1-L4.

Both were short of 4 in at least one tier, which means 75% demanded 100%.

Score-reading gets NEW generated extracts for its new questions rather than
re-pointing at existing passages, so every question is guaranteed to match the
notation it refers to. The arithmetic in the maths question is recomputed here
and asserted against the stored answer before anything is written.

    python fix_last_tiers.py [--dry-run|--restore]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client
from notation import playable

BACKUP = os.path.join(HERE, "_last_tiers_backup.json")
H = "X:1\nT:\nM:%s\nL:1/4\nK:%s\n"

# ---------------------------------------------------------------- maths -----
# 3x + 4y = 10 and 5x - 2y = 8.  Double the second: 10x - 4y = 16; add: 13x = 26.
MATHS = {
    "input_type": "xy_pair", "calculator": False,
    "display": "Solve \\(3x + 4y = 10\\) and \\(5x - 2y = 8\\)",
    "solutions": [2, 1],
    "hint": "Double the second equation to make the y terms +4y and -4y, then add.",
    "guided_steps": [
        {"say": "The y terms are +4y and -2y. Doubling the second equation gives -4y, which "
                "cancels with +4y when you add.",
         "pre": "5x × 2 = ", "post": "x", "answer": 10, "hint": "Multiply every term."},
        {"pre": "-2y × 2 = ", "post": "y", "answer": -4, "hint": "Keep the sign."},
        {"pre": "and the right-hand side: 8 × 2 = ", "answer": 16,
         "hint": "The right-hand side is multiplied too — the step everyone forgets."},
        {"pre": "Add the equations: 3x + 10x = ", "post": "x", "answer": 13,
         "hint": "The y terms cancel."},
        {"pre": "10 + 16 = ", "answer": 26, "hint": "Add the right-hand sides."},
        {"pre": "So 13x = 26, giving x = ", "answer": 2, "phase": "solve"},
        {"pre": "Substitute into 3x + 4y = 10: 4y = 10 - 6 = ", "answer": 4,
         "hint": "3 × 2 = 6."},
        {"pre": "So y = ", "answer": 1, "phase": "solve"}],
}

# -------------------------------------------------------- score reading -----
def P(abc, notes, tempo, title, cap=""):
    return playable(abc, notes, tempo=tempo, title=title, caption=cap,
                    hint="Play it as often as you need.")


SR = {
1: [("bronze", P(H % ("4/4", "C") + "C2 C2 | C C C C |",
                 [(60, 2), (60, 2), (60, 1), (60, 1), (60, 1), (60, 1)], 96, "Extract K"),
     "Play Extract K. Which bar contains more notes?",
     ["Bar 1", "Bar 2", "They contain the same number", "Neither — it is one long note"], 1,
     "Bar 2 lights up four times, bar 1 only twice. Both bars last the same length of time, so the "
     "notes in bar 2 must each be shorter — which is what the hollow and filled heads are telling "
     "you on the page."),
    ("silver", P(H % ("4/4", "C") + "C D E F | E D C2 |",
                 [(60, 1), (62, 1), (64, 1), (65, 1), (64, 1), (62, 1), (60, 2)], 100, "Extract L"),
     "Play Extract L. What shape does the melody make?",
     ["It rises throughout", "It falls throughout",
      "It rises, then falls back to where it began", "It stays on one note"], 2,
     "The line climbs for four notes and then comes back down to its starting pitch. Seeing the "
     "arch on the page and hearing it at the same time is the whole point of following a score."),
    ("silver", P(H % ("4/4", "C") + "C z C z | C4 |",
                 [(60, 1), (None, 1), (60, 1), (None, 1), (60, 4)], 92, "Extract M"),
     "Play Extract M. What happens on beats 2 and 4 of the first bar?",
     ["The notes are played very quietly", "Nothing sounds — those are rests",
      "The notes are played by a different instrument", "The tempo slows down"], 1,
     "The highlight goes out because nothing is sounding. Those gaps are rests, and they are "
     "written on the stave just as deliberately as the notes.")],
2: [("bronze", P(H % ("4/4", "C") + "G G G2 |", [(67, 1), (67, 1), (67, 2)], 96, "Extract H"),
     "Play Extract H. Which note lasts longest, and how many beats?",
     ["The first, 2 beats", "The last, 2 beats", "The last, 3 beats", "They are all equal"], 1,
     "The last note is hollow with a stem — a minim, 2 beats — while the first two are filled "
     "crotchets of 1 beat each. Together they fill the four-beat bar."),
    ("silver", P(H % ("3/4", "C") + "G2 G | G G G |", [(67, 2), (67, 1), (67, 1), (67, 1), (67, 1)],
                 96, "Extract I"),
     "Play Extract I. How many beats are in each bar, and how do you know?",
     ["Four — there are four notes in bar 2",
      "Three — the time signature reads 3 over 4, and each bar totals three beats",
      "Two — the first bar has two notes", "Six — the bars are compound"], 1,
     "The top number of the time signature gives the beats per bar. Bar 1 is a minim plus a "
     "crotchet (2 + 1) and bar 2 is three crotchets — both total three.")],
3: [("bronze", P(H % ("4/4", "C") + "C C E E | G G c2 |",
                 [(60, 1), (60, 1), (64, 1), (64, 1), (67, 1), (67, 1), (72, 2)], 100, "Extract H"),
     "Play Extract H. How does the melody move overall?",
     ["It falls", "It rises", "It stays level throughout", "It rises then falls"], 1,
     "Each pair of notes sits higher on the stave than the pair before, and the sound climbs with "
     "them. Higher on the page always means higher in pitch."),
    ("silver", P(H % ("4/4", "C") + "C G C' G | C4 |",
                 [(60, 1), (67, 1), (72, 1), (67, 1), (60, 4)], 100, "Extract I"),
     "Play Extract I. Is this movement conjunct or disjunct?",
     ["Conjunct — it moves by step", "Disjunct — it moves by leap",
      "Neither — it stays on one note", "Conjunct — it uses only four notes"], 1,
     "The notes jump across several lines and spaces rather than moving to the neighbouring one, "
     "and it sounds angular. Movement by leap is disjunct; stepwise movement is conjunct.")],
4: [("bronze", P(H % ("4/4", "C") + "!f!C D E F | !p!G4 |",
                 [(60, 1), (62, 1), (64, 1), (65, 1), (67, 4)], 100, "Extract J"),
     "Look at Extract J. Which two dynamic markings appear, and in which order?",
     ["p then f — quiet, then loud", "f then p — loud, then quiet",
      "mf then ff", "Only one marking appears"], 1,
     "The f sits below the first note and the p below the last bar. A dynamic mark applies from "
     "where it appears until the next one changes it, so this extract begins loud and drops to "
     "quiet."),
    ("silver", P(H % ("4/4", "C") + ".C .D .E .F | (GABc) |",
                 [(60, .55), (62, .55), (64, .55), (65, .55), (67, 1), (69, 1), (71, 1), (72, 1)],
                 100, "Extract K"),
     "Play Extract K. How does bar 2 differ from bar 1 in the way the notes are played?",
     ["Bar 2 is louder",
      "Bar 1 is short and detached (staccato); bar 2 is smooth and joined (legato)",
      "Bar 2 is faster", "Bar 1 uses a different instrument"], 1,
     "The dots above bar 1 mean staccato, so each note stops early and leaves a gap. The curved "
     "line over bar 2 is a slur, asking for legato — the notes run into one another.")],
}


def main():
    dry = "--dry-run" in sys.argv
    sb = get_client()

    got = None
    # verify the maths before touching anything
    x, y = MATHS["solutions"]
    assert 3 * x + 4 * y == 10 and 5 * x - 2 * y == 8, "maths answer does not satisfy both equations"
    print("maths verified: x=%s y=%s satisfies both equations" % (x, y))

    sub_m = [s for s in sb.table("subjects").select("id,slug,school_id")
             .eq("slug", "maths-ocr").execute().data if not s["school_id"]][0]
    u_m = [u for u in sb.table("units").select("id,slug").eq("subject_id", sub_m["id"])
           .execute().data if u["slug"] == "algebra"][0]["id"]
    sub_s = [s for s in sb.table("subjects").select("id,slug,school_id")
             .eq("slug", "music-aqa").execute().data if not s["school_id"]][0]
    u_s = [u for u in sb.table("units").select("id,slug").eq("subject_id", sub_s["id"])
           .execute().data if u["slug"] == "score-reading"][0]["id"]

    targets = [(u_m, 9)] + [(u_s, n) for n in (1, 2, 3, 4)]

    if "--restore" in sys.argv:
        with open(BACKUP, "r", encoding="utf-8") as f:
            for lid, pd in json.load(f).items():
                sb.table("lessons").update({"practice_data": pd}).eq("id", lid).execute()
        print("restored")
        return

    saved = {}
    for uid, num in targets:
        row = sb.table("lessons").select("id,practice_data").eq("unit_id", uid) \
            .eq("lesson_number", num).single().execute().data
        pd = json.loads(json.dumps(row["practice_data"]))
        before = {t: len(pd["problem_bank"][t]) for t in ("bronze", "silver", "gold")}

        if uid == u_m:
            if not any(g.get("display") == MATHS["display"] for g in pd["problem_bank"]["gold"]):
                pd["problem_bank"]["gold"].append(json.loads(json.dumps(MATHS)))
            label = "maths algebra L9"
        else:
            for tier, fig, text, opts, correct, expl in SR[num]:
                if any(g.get("question") == text for g in pd["problem_bank"][tier]):
                    continue
                pid = "extra-%s-%d" % (tier, len(pd["passages"]))
                pd["passages"].append({"id": pid, "label": text[:40], "text": fig})
                assert 0 <= correct < len(opts) and len(set(opts)) == len(opts)
                pd["problem_bank"][tier].append({
                    "input_type": "multiple_choice", "passage_id": pid, "question": text,
                    "options": opts, "solutions": [correct], "explanation": expl})
            label = "score-reading L%d" % num

        after = {t: len(pd["problem_bank"][t]) for t in ("bronze", "silver", "gold")}
        assert all(after[t] >= 4 for t in after), (label, after)
        ids = {p["id"] for p in pd.get("passages") or []}
        for t in after:
            for g in pd["problem_bank"][t]:
                if g.get("passage_id"):
                    assert g["passage_id"] in ids, (label, g["passage_id"])
        saved[row["id"]] = row["practice_data"]
        if not dry:
            sb.table("lessons").update({"practice_data": pd}).eq("id", row["id"]).execute()
        print("  %-20s b %d->%d  s %d->%d  g %d->%d"
              % (label, before["bronze"], after["bronze"], before["silver"], after["silver"],
                 before["gold"], after["gold"]))

    if not dry and saved and not os.path.exists(BACKUP):
        with open(BACKUP, "w", encoding="utf-8") as f:
            json.dump(saved, f)
        print("backup ->", BACKUP)
    print(("DRY RUN — " if dry else "") + "lessons updated: %d" % len(targets))


if __name__ == "__main__":
    main()
