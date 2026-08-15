# -*- coding: utf-8 -*-
"""Score Reading: perform the markings (Tom's review, 15 Aug — SR-2/3/4/5).

What was wrong:
- Dynamics were printed but every note sounded at the same volume; the
  teaching caption even apologised for it ("does not actually change volume").
- Legato/slur sounded like normal detached notes (the player left a fixed 8%
  gap after every note).
- Staccato was faked by shortening `beats`, which also shortened the CLOCK,
  so staccato bars rushed. That is what made Extract F/G comparisons feel
  wrong to a reader.
- The dynamics teaching figure ringed the p while the bronze question asks
  about mf.
- L4 Extract H's final note played midi 76 against a printed d (74) — a
  second, unclaimed pitch departure. Genuine data bug.
- L2 Extract F prints bars 1-2 identically and swings bar 2 on purpose (the
  gold task), but nothing said the departure was deliberate, so it read as a
  broken score.

This script rebuilds every playable in score-reading L4 (and re-rings the
dynamics card) using the new vel/art map fields (js/score-player.js), and
patches the L2 Extract F caption. All figure HTML is regenerated with
notation.playable/card/figure, then substituted wherever the old figure
appears: its own passage, the method card, and the worked example.

Backup: _backup_score_playables_2026-08-15.json (whole practice_data, L2+L4).
Run: python regen_l4_playables.py [--apply]
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client
from notation import playable, figure, card

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_score_playables_2026-08-15.json")
FIG = re.compile(r"<figure\b.*?</figure>", re.S)

P_ = 0.45   # piano
F_ = 1.0    # forte


def H(m="4/4", k="C"):
    return "X:1\nT:\nM:%s\nL:1/4\nK:%s\n" % (m, k)


def n(midi, beats, vel=None, art=None):
    o = {}
    if vel is not None:
        o["vel"] = vel
    if art is not None:
        o["art"] = art
    return (midi, beats, o) if o else (midi, beats)


# ── the ten L4 figures ──────────────────────────────────────────────────────
# Each entry: passage_id -> (title-to-match-old-figure, new_html)

DYN_LADDER = ("<b>pp</b> very quiet &middot; <b>p</b> quiet &middot; <b>mp</b> moderately quiet "
              "&middot; <b>mf</b> moderately loud &middot; <b>f</b> loud &middot; <b>ff</b> very "
              "loud. They tell the player how loud, from that point on.")

NEW = {
    # SR-4: the ringed dynamic is now the mf the bronze question asks about
    "t-dyn-1": ("Dynamics are letters below the stave",
                card(figure(H() + "!mf!C D !f!E F | G4 |",
                            ring=[("dynam", "a dynamic marking")], width=1300),
                     "Dynamics are letters below the stave", DYN_LADDER)),
    # SR-3: p and f are now performed, and the caption stops apologising
    "t-dyn-2": ("Hear the change",
                playable(H() + "!p!C D E F | !f!G A B c |",
                         [n(60, 1, P_), n(62, 1, P_), n(64, 1, P_), n(65, 1, P_),
                          n(67, 1, F_), n(69, 1, F_), n(71, 1, F_), n(72, 1, F_)],
                         tempo=104, title="Hear the change",
                         caption="Played as marked: bar 1 is quiet (p), bar 2 loud (f). The "
                                 "change lands exactly where the letter appears on the page.")),
    # SR-5: staccato keeps the beat (short SOUND, full clock); the slur joins up
    "t-art-2": ("Short and detached, then smooth",
                playable(H() + ".C .D .E .F | (GABc) |",
                         [n(60, 1, art="stac"), n(62, 1, art="stac"),
                          n(64, 1, art="stac"), n(65, 1, art="stac"),
                          n(67, 1, art="leg"), n(69, 1, art="leg"),
                          n(71, 1, art="leg"), n(72, 1, art="leg")],
                         tempo=100, title="Short and detached, then smooth",
                         caption="Bar 1 is staccato: each note stops early, leaving a gap. "
                                 "Bar 2 is slurred, so the notes run into one another.")),
    "q-ext": ("A longer extract",
              playable(H() + "!p!C D E F | G2 G2 | !f!c B A G | F E D2 | C4 |",
                       [n(60, 1, P_), n(62, 1, P_), n(64, 1, P_), n(65, 1, P_),
                        n(67, 2, P_), n(67, 2, P_),
                        n(72, 1, F_), n(71, 1, F_), n(69, 1, F_), n(67, 1, F_),
                        n(65, 1, F_), n(64, 1, F_), n(62, 2, F_), n(60, 4, F_)],
                       tempo=100, title="A longer extract",
                       caption="Five bars, with a dynamic change partway. Section A prints "
                               "extracts like this and asks you to describe what you can see "
                               "and hear.",
                       hint="Play it a few times before answering.")),
    # gold: staccato bar as printed, pitch departs at bar 2 beat 3, f finish
    "q-f": ("Extract F",
            playable(H() + ".C .D .E .F | G A B c | !f!d4 |",
                     [n(60, 1, art="stac"), n(62, 1, art="stac"),
                      n(64, 1, art="stac"), n(65, 1, art="stac"),
                      n(67, 1), n(69, 1), n(72, 1), n(72, 1),
                      n(74, 4, F_)],
                     tempo=104, title="Extract F",
                     caption="The performance departs from the printed score once, in pitch.",
                     hint="The articulation is played correctly. Follow the notes.")),
    # gold: bar 3 printed staccato but performed joined — THAT is the task
    "gold-1": ("Extract G",
               playable(H() + ".C .D .E .F | (GABc) | .d .c .B .A | G4 |",
                        [n(60, 1, art="stac"), n(62, 1, art="stac"),
                         n(64, 1, art="stac"), n(65, 1, art="stac"),
                         n(67, 1, art="leg"), n(69, 1, art="leg"),
                         n(71, 1, art="leg"), n(72, 1, art="leg"),
                         n(74, 1, art="leg"), n(72, 1, art="leg"),
                         n(71, 1, art="leg"), n(69, 1, art="leg"),
                         n(67, 4)],
                        tempo=108, title="Extract G",
                        caption="One printed articulation is not what you hear.",
                        hint="Bar 3 is printed staccato. Is it played that way?")),
    # gold: dynamics performed correctly; ONE pitch wrong (bar 2 beat 4).
    # Final note fixed 76 -> 74: it played a second, unclaimed departure.
    "gold-2": ("Extract H",
               playable(H() + "!p!C D E F | !f!G A B c | !p!d4 |",
                        [n(60, 1, P_), n(62, 1, P_), n(64, 1, P_), n(65, 1, P_),
                         n(67, 1, F_), n(69, 1, F_), n(71, 1, F_), n(74, 1, F_),
                         n(74, 4, P_)],
                        tempo=108, title="Extract H",
                        caption="The dynamics are played correctly. One pitch is not.",
                        hint="Follow the printed notes through the loud bar.")),
    # gold: articulation all correct; the final semibreve stops two beats early
    "gold-3": ("Extract I",
               playable(H() + "(CDEF) | .G .A .B .c | (dcBA) | G4 |",
                        [n(60, 1, art="leg"), n(62, 1, art="leg"),
                         n(64, 1, art="leg"), n(65, 1, art="leg"),
                         n(67, 1, art="stac"), n(69, 1, art="stac"),
                         n(71, 1, art="stac"), n(72, 1, art="stac"),
                         n(74, 1, art="leg"), n(72, 1, art="leg"),
                         n(71, 1, art="leg"), n(69, 1, art="leg"),
                         n(67, 2)],
                        tempo=108, title="Extract I",
                        caption="One printed note is not the length you hear.",
                        hint="The articulation is correct throughout. Count the last bar.")),
    "extra-bronze-10": ("Extract J",
                        playable(H() + "!f!C D E F | !p!G4 |",
                                 [n(60, 1, F_), n(62, 1, F_), n(64, 1, F_), n(65, 1, F_),
                                  n(67, 4, P_)],
                                 tempo=100, title="Extract J",
                                 hint="Play it as often as you need.")),
    "extra-silver-11": ("Extract K",
                        playable(H() + ".C .D .E .F | (GABc) |",
                                 [n(60, 1, art="stac"), n(62, 1, art="stac"),
                                  n(64, 1, art="stac"), n(65, 1, art="stac"),
                                  n(67, 1, art="leg"), n(69, 1, art="leg"),
                                  n(71, 1, art="leg"), n(72, 1, art="leg")],
                                 tempo=100, title="Extract K",
                                 hint="Play it as often as you need.")),
}

L2_F_OLD_CAP = "One bar is not played in even threes."
L2_F_NEW_CAP = ("The score is printed correctly &mdash; the performance deliberately departs "
                "from it in one bar. Say which.")


def swap_fig(html, title, new_html):
    """Replace the <figure> block whose title caption contains `title`."""
    hits = 0
    out = []
    last = 0
    for m in FIG.finditer(html):
        block = m.group(0)
        tm = re.search(r'class="sv-notefig-title">(.*?)</figcaption>', block)
        if tm and title in re.sub(r"<[^>]+>", "", tm.group(1)):
            out.append(html[last:m.start()])
            out.append(new_html)
            last = m.end()
            hits += 1
    out.append(html[last:])
    return "".join(out), hits


def main():
    sb = get_client()
    unit = [u for u in sb.table("units").select("id,slug").execute().data
            if u["slug"] == "score-reading"][0]["id"]
    rows = {r["lesson_number"]: r for r in sb.table("lessons")
            .select("id,lesson_number,practice_data").eq("unit_id", unit).execute().data}

    backup = {str(k): rows[k]["practice_data"] for k in (2, 4)}

    # ---------- L4: substitute every rebuilt figure wherever it appears ------
    pd4 = rows[4]["practice_data"]
    for pid, (title, new_html) in NEW.items():
        p = next(x for x in pd4["passages"] if x["id"] == pid)
        _, hits = swap_fig(p["text"], title, new_html)
        assert hits == 1, ("passage %s: expected 1 figure titled %r, found %d"
                           % (pid, title, hits))
        p["text"], _ = swap_fig(p["text"], title, new_html)
        print("  L4 %-16s figure %-38r replaced" % (pid, title))
    mcx = pd4["method_card"]["content"]
    for pid in ("t-dyn-1", "t-dyn-2", "t-art-2"):
        title, new_html = NEW[pid]
        mcx, hits = swap_fig(mcx, title, new_html)
        assert hits == 1, ("method card: figure %r found %d times" % (title, hits))
    pd4["method_card"]["content"] = mcx
    print("  L4 method card: 3 figures replaced")
    we = pd4["worked_examples"][0]["question"]
    we, hits = swap_fig(we, "A longer extract", NEW["q-ext"][1])
    assert hits == 1, "worked example: extract figure found %d times" % hits
    pd4["worked_examples"][0]["question"] = we
    print("  L4 worked example: extract replaced")

    # ---------- L2: Extract F caption says the departure is deliberate ------
    pd2 = rows[2]["practice_data"]
    l2hits = 0
    for p in pd2["passages"]:
        if L2_F_OLD_CAP in p["text"]:
            p["text"] = p["text"].replace(L2_F_OLD_CAP, L2_F_NEW_CAP)
            l2hits += 1
            print("  L2 %s: Extract F caption updated" % p["id"])
        elif L2_F_NEW_CAP in p["text"]:
            l2hits += 1
            print("  L2 %s: Extract F caption already updated (idempotent rerun)" % p["id"])
    assert l2hits == 1, "L2 Extract F caption found %d times" % l2hits

    # ---------- sanity: no 0.55 fake remains in either lesson ----------------
    for num, pd in ((2, pd2), (4, pd4)):
        s = json.dumps(pd)
        fakes = s.count('"beats": 0.55') + s.count('"beats":0.55')
        print("  L%d 0.55-beat fakes remaining: %d" % (num, fakes))
        assert fakes == 0 or num == 2, "L4 still has staccato fakes"

    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    # never clobber the first backup on an idempotent rerun — the second run's
    # "backup" would be the already-fixed state (caught 15 Aug: the rerun for
    # the wider mf ring overwrote the pre-fix L4 snapshot)
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for num, pd in ((2, pd2), (4, pd4)):
        sb.table("lessons").update({"practice_data": pd}).eq("id", rows[num]["id"]).execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
