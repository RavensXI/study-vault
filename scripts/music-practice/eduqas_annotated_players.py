# -*- coding: utf-8 -*-
"""Give the two Eduqas prepared extracts the AQA set-study treatment
(Tom's review finding, 16 Aug): replace the plain sv-embed video figure
with the sv-annotated-player (YouTube mode — the format pioneered on the
AQA Queen study piece) and convert every dead sv-listen box into a live
one by appending numbered sv-ap-ref jump chips that seek the player.

Listen-box captions and their data-narration-id are preserved verbatim —
the narration extractor skips <button>, so manifests stay valid. The
embed figcaptions carry no narration ids (verified), so replacing the
embed figure needs no manifest surgery.

Pin times are AUTHORED DRAFTS from documented song/movement structure;
the player's admin adjusting mode (drag pins, save) is the fine-tuning
tool against the real video. data-dur is initial-layout only — the
runtime re-reads the true duration from the YouTube API.

Run: python eduqas_annotated_players.py [--apply]
Backup: _backup_annotated_players_2026-08-16.json
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_annotated_players_2026-08-16.json")

AFRICA_YT, AFRICA_DUR = "FTQbiNvZqaY", 272
BADIN_YT, BADIN_DUR = "BsiqjGgwuU8", 85

AFRICA_CREDIT = ("Official video, streamed from YouTube &mdash; not hosted "
                 "by StudyVault. Toto: Africa (1982).")
BADIN_CREDIT = ("Performance by the Netherlands Bach Society, streamed from "
                "YouTube &mdash; not hosted by StudyVault. Bach: Badinerie, "
                "Orchestral Suite No. 2 in B minor, BWV 1067.")

# per lesson: (unit, num, yt, dur, credit, track_label,
#              pins [(t, label, tip)], refmap [(caption_fragment, [pin_nums])])
LESSONS = [
    ("aos4-popular-music", 3, AFRICA_YT, AFRICA_DUR, AFRICA_CREDIT, "Africa",
     [(0, "Intro",
       "Layered ostinato &mdash; a GS-1 synth kalimba doubled by real "
       "marimba, before the half-time groove enters underneath."),
      (27, "Verse",
       "The half-time groove: the snare lands on beat 3 only, over steady "
       "sixteenth notes on the hi-hat."),
      (58, "Verse into chorus",
       "Listen for the lift: the harmony brightens and backing vocals stack "
       "in thirds as the hook arrives."),
      (68, "Chorus",
       "&lsquo;Bless the rains&rsquo; &mdash; the melody doubled in vocal "
       "harmony, the fullest texture so far."),
      (170, "Synth solo",
       "The CS-80 solo &mdash; warm, breathy, slightly detuned. Compare its "
       "timbre with the intro synth."),
      (205, "Final choruses",
       "Texture at its peak, then the layers strip back to the opening "
       "ostinato to close the arch.")],
     [("the opening bars", [1]),
      ("the verse drum groove", [2]),
      ("verse into chorus", [3]),
      ("comparing the synth intro with a later chorus", [1, 4])]),

    ("aos4-popular-music", 4, AFRICA_YT, AFRICA_DUR, AFRICA_CREDIT, "Africa",
     [(0, "Ostinato layers",
       "Separate the strands: the synth kalimba pattern, the marimba "
       "doubling it, and the pulse beneath."),
      (27, "Verse texture",
       "Melody-dominated homophony &mdash; voice on top, bass and drums "
       "locking the half-time feel below."),
      (68, "Chorus harmony",
       "Backing vocals in thirds create the &lsquo;lifted&rsquo; chorus "
       "sound &mdash; count the vocal layers."),
      (170, "Solo timbre",
       "The CS-80 lead: breathy, detuned, expressive. How does its shape "
       "echo the vocal hook?"),
      (205, "Outro",
       "The layers leave one by one until the ostinato stands alone "
       "&mdash; the texture arch completes.")],
     [("the opening synth-and-marimba ostinato", [1]),
      ("how the backing vocals harmonise in thirds", [3]),
      ("the synthesizer solo section", [4])]),

    ("aos1-forms-and-devices", 3, BADIN_YT, BADIN_DUR, BADIN_CREDIT,
     "Badinerie",
     [(0, "A section",
       "Flute leads over the continuo in B minor; two-bar ideas passed "
       "between flute and violins."),
      (11, "A closes",
       "A perfect cadence in F sharp minor, the dominant minor &mdash; the "
       "A section&rsquo;s destination."),
      (15, "A repeated",
       "Binary form: each half is repeated. Same music, second hearing "
       "&mdash; notice more ornamentation if the player adds any."),
      (32, "B section",
       "Begins in F sharp minor and works back through related keys, "
       "including D major, towards B minor."),
      (55, "Dialogue and dynamics",
       "Short phrases echoed between flute and strings; terraced dynamics "
       "&mdash; loud then suddenly soft, no gradual change.")],
     [("BWV 1067", [1]),
      ("what to listen for in the form", [3, 4]),
      ("dialogue between flute and strings", [5])]),

    ("aos1-forms-and-devices", 4, BADIN_YT, BADIN_DUR, BADIN_CREDIT,
     "Badinerie",
     [(0, "Opening flute solo",
       "Count the bars before the strings answer &mdash; the flute states "
       "the idea alone over continuo."),
      (11, "Cadence in F sharp minor",
       "The goal of Section A: a perfect cadence in the dominant minor, "
       "not the relative major."),
      (15, "A repeat",
       "The repeat is structural &mdash; binary form asks you to hear each "
       "half twice."),
      (32, "B begins",
       "From F sharp minor onward: sequences drive the music back home "
       "to B minor."),
      (50, "Forte then piano",
       "Terraced dynamics: a phrase played forte, then immediately echoed "
       "piano &mdash; find one pair.")],
     [("track the A section", [1, 2]),
      ("count how many bars", [1]),
      ("played forte and then imm", [5])]),
]


def player_html(lesson_id, yt, dur, credit, track_label, pins):
    btns = []
    for i, (t, label, tip) in enumerate(pins, 1):
        pct = 100.0 * t / dur
        btns.append(
            '<button type="button" class="sv-ap-pin" data-track="t1" '
            'data-cid="t1c%d" data-t="%d" style="left:%.2f%%">%d'
            '<span class="sv-ap-tip"><strong>%d &middot; %s</strong>%s'
            "</span></button>" % (i, t, pct, i, i, label, tip))
    return (
        '<figure class="sv-annotated-player sv-ap-yt" data-lesson-id="%s">'
        '<div class="sv-ap-bar"><button type="button" class="sv-ap-play">'
        "&#9654;</button>"
        '<span class="sv-ap-tick">0:00 / &ndash;:&ndash;&ndash;</span>'
        '<div class="sv-ap-tracks"><button type="button" '
        'class="sv-ap-trackbtn sv-ap-trackbtn--on" data-track="t1" '
        'data-yt="%s" data-dur="%d">%s</button></div></div>'
        '<div class="sv-ap-media"><div class="sv-ap-video">'
        '<div class="sv-ap-ytmount"></div></div>'
        '<div class="sv-ap-wrap"><div class="sv-ap-track">'
        '<div class="sv-ap-trackfill"></div></div>%s</div></div>'
        '<figcaption class="sv-listen-credit">%s</figcaption></figure>'
        % (lesson_id, yt, dur, track_label, "".join(btns), credit))


def chip(pins, n):
    t = pins[n - 1][0]
    return ('<button type="button" class="sv-ap-ref" data-t="%d" '
            'data-track="t1">%d</button>' % (t, n))


def main():
    sb = get_client()
    sub = sb.table("subjects").select("id").eq("slug", "music-eduqas") \
        .execute().data[0]["id"]
    units = {u["slug"]: u["id"] for u in
             sb.table("units").select("id,slug,subject_id").execute().data
             if u["subject_id"] == sub}
    backup, writes = {}, []
    for uslug, num, yt, dur, credit, tl, pins, refmap in LESSONS:
        row = sb.table("lessons").select("id,content_html") \
            .eq("unit_id", units[uslug]).eq("lesson_number", num) \
            .execute().data[0]
        ch = row["content_html"]
        # 0. a fact-check stray the main fixer's wordings missed (L4 n7):
        # Section A ends in the dominant MINOR, not a brighter major key.
        # Narrated caption -> re-narrate this lesson after applying.
        ch = ch.replace(
            "try to hear the point where the music settles into a brighter, "
            "major-key sound",
            "try to hear the point where the music arrives in a new key "
            "&mdash; F sharp minor, the dominant minor")
        # 1. embed figure -> annotated player
        embeds = re.findall(r'<figure class="sv-embed.*?</figure>', ch, re.S)
        assert len(embeds) == 1, "%s L%d: %d embed figures" % (uslug, num,
                                                               len(embeds))
        ch = ch.replace(embeds[0],
                        player_html(row["id"], yt, dur, credit, tl, pins))
        # 2. dead listen boxes -> chips appended inside the figcaption
        figs = re.findall(r'<figure class="sv-listen".*?</figure>', ch, re.S)
        used = set()
        for frag, pin_nums in refmap:
            hits = [f for f in figs if frag in re.sub(r"&\w+;", "'", f)
                    or frag in f]
            assert len(hits) == 1, "%s L%d: fragment %r matched %d figures" \
                % (uslug, num, frag, len(hits))
            fig = hits[0]
            assert fig not in used, "fragment %r re-matched a figure" % frag
            used.add(fig)
            chips = " " + "".join(chip(pins, n) for n in pin_nums)
            # some builder output lacks the inner figcaption — chips then
            # go at the end of the figure itself
            anchor = ("</figcaption>" if "</figcaption>" in fig
                      else "</figure>")
            cap_close = fig.rindex(anchor)
            newfig = fig[:cap_close] + chips + fig[cap_close:]
            ch = ch.replace(fig, newfig)
        unconverted = [f for f in figs if f not in used]
        assert not unconverted, "%s L%d: %d listen boxes not mapped" \
            % (uslug, num, len(unconverted))
        backup[row["id"]] = row["content_html"]
        writes.append((row["id"], ch, "%s L%d" % (uslug, num)))
        print("%s L%d: player in, %d boxes converted (%d pins)"
              % (uslug, num, len(refmap), len(pins)))
    print("\nlessons to write:", len(writes))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, ch, label in writes:
        sb.table("lessons").update({"content_html": ch}).eq("id", lid) \
            .execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
