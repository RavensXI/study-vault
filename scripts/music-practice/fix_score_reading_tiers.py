# -*- coding: utf-8 -*-
"""Two defects Tom found reviewing the rebuilt Score Reading unit.

1. STACKED EXTRACTS GET CUT OFF. Teaching passages held two figures each, and
   the passage panel is a capped scroll box, so the second was clipped. Every
   passage is now split so one figure = one passage. Questions that pointed at
   a combined passage are re-pointed at the half that actually shows the thing
   being asked about.

2. GOLD WAS UNPASSABLE ON ITS OWN TERMS. A tier passes on four correct in a row
   or 75% overall, but gold held two questions: four in a row is unreachable and
   75% of two means both. Gold is now six questions in every lesson, all
   follow-and-check on longer extracts — which also answers "a bit easy".

    python fix_score_reading_tiers.py            apply
    python fix_score_reading_tiers.py --restore  undo
"""
import copy, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client
from notation import playable

BACKUP = os.path.join(HERE, "_score_reading_tiers_backup.json")
H = "X:1\nT:\nM:%s\nL:1/4\nK:%s\n"


def P(abc, notes, tempo, title, cap, hint="Play it as often as you need."):
    return playable(abc, notes, tempo=tempo, title=title, caption=cap, hint=hint)


def q(pid, text, opts, correct, expl):
    return {"input_type": "multiple_choice", "passage_id": pid, "question": text,
            "options": opts, "solutions": [correct], "explanation": expl}


FIG = re.compile(r"<figure\b.*?</figure>", re.S)


def split_passages(pd):
    """One figure per passage. Returns (new_passages, id_remap) where remap sends
    an old id to the id of its FIRST fragment."""
    out, remap = [], {}
    for p in pd["passages"]:
        figs = FIG.findall(p["text"])
        if len(figs) <= 1:
            out.append(p)
            remap[p["id"]] = [p["id"]]
            continue
        made = []
        for i, f in enumerate(figs, 1):
            # keep the figure's own title as the passage label where there is one
            m = re.search(r'class="sv-notefig-title">(.*?)</figcaption>', f)
            label = re.sub(r"<[^>]+>", "", m.group(1)) if m else "%s (%d)" % (p["label"], i)
            nid = "%s-%d" % (p["id"], i)
            out.append({"id": nid, "label": label, "text": f})
            made.append(nid)
        remap[p["id"]] = made
    return out, remap


# ---- new gold extracts: longer, and each breaks the score in a different way --
GOLD = {
1: [P(H % ("4/4", "C") + "C D E F | G F E D | C D E F | G4 |",
       [(60,1),(62,1),(64,1),(65,1),(67,1),(65,1),(64,1),(62,1),
        (60,1),(62,1),(64,1),(69,1),(67,4)], 112, "Extract H",
       "One printed note is not the pitch you hear.", "The rhythm is correct throughout."),
     P(H % ("4/4", "C") + "C C C C | C C C C | C4 |",
       [(60,1),(60,1),(60,1),(60,1),(60,1),(60,2),(False,0),(60,1),(60,4)], 108, "Extract I",
       "One printed note is not the length you hear.", "Every pitch is correct. Count the beats."),
     P(H % ("3/4", "C") + "C D E | F G A | B c d | c4 |",
       [(60,1),(62,1),(64,1),(65,2),(False,0),(69,1),(71,1),(72,1),(74,1),(72,3)], 116, "Extract J",
       "The performance skips something that is printed.",
       "Follow the climb bar by bar. One step is missing.")],
2: [P(H % ("4/4", "C") + "G2 G2 | G G G G | G3 G | G4 |",
       [(67,2),(67,2),(67,1),(67,2),(False,0),(67,1),(67,2),(67,2),(67,4)], 104, "Extract E",
       "One bar is not played with the printed rhythm.",
       "All one pitch, so listen only to the lengths."),
     P(H % ("6/8", "C") + "GGG GGG | GGG GGG | A3 |",
       [(67,1/3.)]*6 + [(67,.5),(67,1/6.),(67,.5),(67,1/6.),(67,.5),(67,1/6.)] + [(69,1)],
       88, "Extract F", "One bar is not played in even threes.",
       "One bar swings; the other is even."),
     P(H % ("4/4", "C") + "C3 D | E3 F | G3 A | c4 |",
       [(60,3),(62,1),(64,2),(65,2),(67,3),(69,1),(72,4)], 104, "Extract G",
       "One dotted note is not held for its printed length.",
       "Each bar should begin with a three-beat note.")],
3: [P(H % ("4/4", "C") + "C E G c | G E C2 | C E G c | e4 |",
       [(60,1),(64,1),(67,1),(72,1),(67,1),(64,1),(60,2),
        (60,1),(64,1),(67,1),(71,1),(76,4)], 112, "Extract E",
       "One printed note is not the pitch you hear.",
       "The arch shape repeats. Listen to the second time round."),
     P(H % ("4/4", "C") + "C D E F | G A B c | B A G F | E4 |",
       [(60,1),(62,1),(64,1),(65,1),(67,1),(69,1),(71,1),(76,1),
        (71,1),(69,1),(67,1),(65,1),(64,4)], 116, "Extract F",
       "The line is printed entirely stepwise. The performance leaps once.",
       "Where does the smooth movement break?"),
     P(H % ("4/4", "D") + "D E ^F G | A4 |",
       [(62,1),(64,1),(65,1),(67,1),(69,4)], 100, "Extract G",
       "The key signature says two sharps. One note is played as if it were not.",
       "Listen to the third note against the printed sharp.")],
4: [P(H % ("4/4", "C") + ".C .D .E .F | (GABc) | .d .c .B .A | G4 |",
       [(60,.55),(62,.55),(64,.55),(65,.55),(67,1),(69,1),(71,1),(72,1),
        (74,1),(72,1),(71,1),(69,1),(67,4)], 108, "Extract G",
       "One printed articulation is not what you hear.",
       "Bar 3 is printed staccato. Is it played that way?"),
     P(H % ("4/4", "C") + "!p!C D E F | !f!G A B c | !p!d4 |",
       [(60,1),(62,1),(64,1),(65,1),(67,1),(69,1),(71,1),(74,1),(76,4)], 108, "Extract H",
       "The dynamics are played correctly. One pitch is not.",
       "Follow the printed notes through the loud bar."),
     P(H % ("4/4", "C") + "(CDEF) | .G .A .B .c | (dcBA) | G4 |",
       [(60,1),(62,1),(64,1),(65,1),(67,.55),(69,.55),(71,.55),(72,.55),
        (74,1),(72,1),(71,1),(69,1),(67,2)], 108, "Extract I",
       "One printed note is not the length you hear.",
       "The articulation is correct throughout. Count the last bar.")],
}

GOLD_Q = {
1: [("Play Extract H. One printed note is not the pitch you hear. Which bar?",
     ["Bar 1", "Bar 2", "Bar 3", "Bar 4"], 2,
     "Bar 3 is printed as the same rising figure as bar 1 — C, D, E, F. The fourth beat sounds "
     "well above the printed F, so the line jumps instead of stepping. Bars 1 and 2 are exactly "
     "as written, which is what makes the repeat worth checking."),
    ("Play Extract I. Every pitch is correct, but one note is not the printed length. Where?",
     ["Bar 1, beat 2", "Bar 2, beat 2", "Bar 2, beat 4", "Bar 3"], 1,
     "Bar 2 is printed as four even crotchets. The second one is held for two beats, so the third "
     "printed note never sounds and the bar still totals four. On a single repeated pitch there is "
     "no melodic clue at all — only the rhythm gives it away."),
    ("Play Extract J. Something printed is skipped. What, and where?",
     ["Bar 1 — the first note", "Bar 2 — the middle note",
      "Bar 3 — the middle note", "Nothing is skipped"], 1,
     "The score climbs one step per note throughout. In bar 2 the performance goes F then A, "
     "missing the printed G, so the bar contains two notes where three are written and the climb "
     "jumps. Counting notes per bar against the page catches this faster than listening for a "
     "wrong pitch.")],
2: [("Play Extract E. One bar is not played with the printed rhythm. Which?",
     ["Bar 1", "Bar 2", "Bar 3", "Bar 4"], 1,
     "Bar 2 is printed as four crotchets. What sounds is crotchet, minim, crotchet — the second "
     "note takes the third note's beat. The bar still lasts four beats, so only reading along "
     "reveals it."),
    ("Play Extract F. One bar is not played in even threes. Which?",
     ["Bar 1", "Bar 2", "Bar 3", "Neither — both are compound"], 1,
     "6/8 gives two beats, each splitting into three EVEN quavers. Bar 2 is played long-short, "
     "long-short — a lopsided swing the page does not ask for. The beaming still shows even "
     "groups of three, so the performance and the notation disagree."),
    ("Play Extract G. One dotted note is not held for its printed length. Which bar?",
     ["Bar 1", "Bar 2", "Bar 3", "Bar 4"], 1,
     "Every bar is printed as a dotted minim (3 beats) plus a crotchet. In bar 2 the first note is "
     "held for only two beats and the second stretches to two, so the dotted long-short shape "
     "becomes two equal halves and the dot is effectively ignored.")],
3: [("Play Extract E. The arch shape is printed twice. One note differs the second time. Which beat?",
     ["Bar 3, beat 2", "Bar 3, beat 4", "Bar 4", "Bar 1, beat 3"], 1,
     "Bars 1 and 3 are printed identically — C, E, G, C. On the fourth beat of bar 3 you hear a "
     "note below the printed top C, so the second arch does not reach as high as the first. "
     "Comparing a repeat against its first appearance is a standard Section A task."),
    ("Play Extract F. The line is printed entirely stepwise, but the performance leaps once. Where?",
     ["Bar 1", "Bar 2, beat 4", "Bar 3, beat 1", "Bar 4"], 1,
     "The printed line walks up and back down by step throughout. On the last beat of bar 2 the "
     "performance jumps past the printed C, breaking the conjunct movement you can see on the page."),
    ("Play Extract G. The key signature shows two sharps. Which note is played as if it were not sharpened?",
     ["The first", "The second", "The third", "The last"], 2,
     "The key signature sharpens every F and C in the piece, so the third note is printed as "
     "F sharp. It sounds a semitone lower — an F natural — which is why the line loses its "
     "brightness at that point. A key signature applies all the way through, not just to bar 1.")],
4: [("Play Extract G. One printed articulation is not what you hear. Which bar?",
     ["Bar 1", "Bar 2", "Bar 3", "Bar 4"], 2,
     "Bar 3 is printed with staccato dots but is played smoothly and joined, with no gaps between "
     "the notes. Bars 1 and 2 are played exactly as marked, so the contrast you can hear between "
     "them is correct and only the third bar disagrees with the page."),
    ("Play Extract H. The dynamics are played correctly. One pitch is not. Where?",
     ["Bar 1, beat 3", "Bar 2, beat 3", "Bar 2, beat 4", "Bar 3"], 2,
     "Bar 2 is printed as a stepwise climb G, A, B, C. The last beat sounds above the printed C, "
     "so the loud bar overshoots. The dynamic change at bar 2 is played exactly as written, which "
     "draws the ear away from the wrong note."),
    ("Play Extract I. The articulation is right throughout, but one note is not the printed length. Where?",
     ["Bar 1", "Bar 2", "Bar 3", "Bar 4"], 3,
     "The last bar is printed as a semibreve — four beats. It sounds for two and then stops, so the "
     "extract ends early. Checking that a final long note actually lasts its full value is easy to "
     "forget once the interesting material has gone past.")],
}


def main():
    sb = get_client()
    unit = [u for u in sb.table("units").select("id,slug").execute().data
            if u["slug"] == "score-reading"][0]["id"]
    rows = {r["lesson_number"]: r for r in sb.table("lessons")
            .select("id,lesson_number,practice_data").eq("unit_id", unit).execute().data}

    if "--restore" in sys.argv:
        with open(BACKUP, "r", encoding="utf-8") as f:
            for num, pd in json.load(f).items():
                sb.table("lessons").update({"practice_data": pd}).eq("id", rows[int(num)]["id"]).execute()
        print("restored")
        return
    if not os.path.exists(BACKUP):
        with open(BACKUP, "w", encoding="utf-8") as f:
            json.dump({str(n): rows[n]["practice_data"] for n in (1, 2, 3, 4)}, f)
        print("backed up ->", BACKUP)

    for n in (1, 2, 3, 4):
        pd = copy.deepcopy(rows[n]["practice_data"])
        passages, remap = split_passages(pd)

        # a question pointing at a split passage follows the fragment whose text
        # still contains the figure it was written about; default to the first
        for tier in pd["problem_bank"]:
            for item in pd["problem_bank"][tier]:
                old = item["passage_id"]
                if old in remap and remap[old][0] != old:
                    item["passage_id"] = remap[old][0]

        for i, fig in enumerate(GOLD[n]):
            passages.append({"id": "gold-%d" % (i + 1), "label": re.sub(
                r"<[^>]+>", "", re.search(r'sv-notefig-title">(.*?)</figcaption>', fig).group(1)),
                "text": fig})
        for i, (text, opts, correct, expl) in enumerate(GOLD_Q[n]):
            pd["problem_bank"]["gold"].append(q("gold-%d" % (i + 1), text, opts, correct, expl))

        pd["passages"] = passages
        ids = {p["id"] for p in passages}
        counts = {}
        for tier in pd["problem_bank"]:
            counts[tier] = len(pd["problem_bank"][tier])
            for item in pd["problem_bank"][tier]:
                assert item["passage_id"] in ids, (n, item["passage_id"])
                assert 0 <= item["solutions"][0] < len(item["options"])
                assert item["explanation"]
        assert all(p["text"].count("</figure>") == 1 for p in passages), n
        assert counts["gold"] >= 5, (n, counts)
        sb.table("lessons").update({"practice_data": pd}).eq("id", rows[n]["id"]).execute()
        print("L%d  passages=%-2d  bronze=%d silver=%d gold=%d"
              % (n, len(passages), counts["bronze"], counts["silver"], counts["gold"]))


if __name__ == "__main__":
    main()
