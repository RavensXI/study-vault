# -*- coding: utf-8 -*-
"""Edexcel Phase 5: give every set work the annotated-player treatment in
its two study lessons — the plain sv-embed of the WORK is replaced by the
sv-annotated-player (YT mode) with authored pin drafts; context embeds in
the same lessons stay as plain embeds.

Pin TIMES are drafts from documented structure (the admin 'Adjust pins'
mode is the fine-tuning tool, as on the Eduqas study pieces). For the
Bach and Beethoven videos the movement may sit inside a longer film —
pins there are movement-relative drafts flagged for the review pass.

Run: python edexcel_players.py [--apply]
Backup: _backup_edexcel_players_2026-08-16.json
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
from eduqas_annotated_players import player_html

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_edexcel_players_2026-08-16.json")

# (unit, [lessons], yt id, est dur s, credit, label, pins [(t, label, tip)])
WORKS = [
    ("aos1-instrumental-music", [2, 3], "LHjbRMIIhuM", 300,
     "Performance by the Netherlands Bach Society, streamed from YouTube "
     "&mdash; not hosted by StudyVault. Bach: Brandenburg Concerto No. 5, "
     "3rd movement.", "Brandenburg 5/iii",
     [(0, "Fugal opening", "Violin and flute launch the gigue-like subject "
       "in imitation &mdash; count the entries as they stack up."),
      (25, "Harpsichord joins the argument", "Not just continuo filler: "
       "the harpsichord takes the subject as an equal concertino voice."),
      (75, "B section", "The music turns to the minor and lightens &mdash; "
       "concertino textures dominate before the return."),
      (150, "Da capo return", "The opening fugal material comes back "
       "&mdash; the A-B-A frame completing itself."),
      (210, "Drive to the close", "Sequences press towards the final "
       "cadence in D major.")]),
    ("aos1-instrumental-music", [4, 5], "hcczxDKkYhU", 540,
     "Fabian M&uuml;ller, streamed from YouTube (Deutsche Grammophon) "
     "&mdash; not hosted by StudyVault. Beethoven: Piano Sonata No. 8 "
     "&lsquo;Path&eacute;tique&rsquo;, 1st movement.", "Pathétique i",
     [(0, "Grave", "The heavy C minor chords and dotted rhythms &mdash; "
       "an introduction with the weight of an opera scene."),
      (100, "Allegro di molto", "The rocketing first subject over tremolo "
       "left hand &mdash; agitated, driving, staccato."),
      (165, "Second subject", "The contrasting theme &mdash; note how it "
       "arrives in the UNEXPECTED minor before brightening."),
      (255, "Development &mdash; Grave returns", "The slow introduction "
       "erupts back mid-movement: Beethoven's structural shock."),
      (430, "Recapitulation", "The first subject storms home in C minor."),
      (515, "Coda", "One last Grave memory, then the abrupt final "
       "cadence.")]),
    ("aos2-vocal-music", [2, 3], "sdSA0jcnBNo", 240,
     "Helen Watts, streamed from YouTube &mdash; not hosted by "
     "StudyVault. Purcell: Music for a While.", "Music for a While",
     [(0, "The ground alone", "The repeating bass line is laid out bare "
       "&mdash; learn its shape now so you can track it under "
       "everything."),
      (15, "Voice enters", "The vocal line floats across the ground's "
       "joins &mdash; phrase lengths deliberately overlapping the bass."),
      (70, "Word painting", "Listen for the famous falling, repeated-note "
       "effects as the text turns to drops and easing pain."),
      (150, "Return", "The opening material comes back &mdash; the A "
       "section rounded off after the contrast."),
      (215, "Final cadence", "Suspensions resolve and the ground finally "
       "comes to rest.")]),
    ("aos2-vocal-music", [4, 5], "2ZBtPf7FOoM", 180,
     "Official video (Top of the Pops, 1974), streamed from YouTube "
     "&mdash; not hosted by StudyVault. Queen: Killer Queen.",
     "Killer Queen",
     [(0, "Fingersnaps and piano", "The urbane opening groove &mdash; "
       "piano-led, poised, deliberately unhurried."),
      (12, "Verse 1", "Melody-dominated homophony with the piano "
       "strutting underneath."),
      (45, "Chorus", "The stacked, multitracked backing vocals arrive "
       "&mdash; Queen's studio signature."),
      (80, "Verse 2 and build", "Listen for the added guitar layers and "
       "panning effects."),
      (110, "Guitar solo", "Brian May's composed solo &mdash; melodic, "
       "layered, with the bell-like overdub effects."),
      (150, "Final chorus", "Texture at its fullest to the wry ending.")]),
    ("aos3-stage-and-screen", [2, 3], "l0Bs_eaXaCo", 345,
     "Original Broadway cast recording, streamed from YouTube &mdash; not "
     "hosted by StudyVault. Schwartz: Defying Gravity (Wicked).",
     "Defying Gravity",
     [(0, "Dialogue into song", "The recitative-like exchange &mdash; "
       "theatre first, song second."),
      (50, "The Unlimited motif", "The rising motif with its concealed "
       "rainbow-song quotation &mdash; rhythm disguised, notes intact."),
      (95, "First chorus", "The title idea takes flight &mdash; note the "
       "leap on the key word."),
      (185, "The build", "Key lifts and driving quavers stack the "
       "tension scene-length."),
      (290, "Final flight", "The climactic section &mdash; the fullest "
       "orchestration and the highest vocal writing in the number.")]),
    ("aos3-stage-and-screen", [4, 5], "54hoKbTWon4", 330,
     "John Williams and the Vienna Philharmonic, streamed from YouTube "
     "(Deutsche Grammophon) &mdash; not hosted by StudyVault. Williams: "
     "Star Wars Main Title.", "Star Wars Main Title",
     [(0, "Fanfare", "Brass hurl out the rising fourths and fifths with "
       "triplet upbeats &mdash; instant announcement."),
      (18, "Main theme", "The heroic A theme in B flat major &mdash; "
       "triadic, wide-leaping, doubled in octaves."),
      (55, "Lyrical B section", "Strings take the contrasting theme "
       "&mdash; the romance inside the adventure."),
      (95, "Return", "The fanfare material drives back in."),
      (140, "Close", "Percussion punctuation and brass stabs carry the "
       "title music to its cadence.")]),
    ("aos4-fusions", [2, 3], "U6vkehDfYXI", 420,
     "Official audio, streamed from YouTube &mdash; not hosted by "
     "StudyVault. Afro Celt Sound System: Release (1999).", "Release",
     [(0, "Drone and atmosphere", "The synth drone opens the space "
       "&mdash; nothing metric yet, just colour."),
      (60, "Voice", "The keening, ornamented vocal line enters over the "
       "drone."),
      (150, "The traditions meet", "Uilleann pipes and West African "
       "strings/percussion in dialogue over the programmed pulse."),
      (250, "Full groove", "Every layer in: Celtic melody, African "
       "cross-rhythm, electronic engine."),
      (350, "Breakdown and return", "Layers strip back before the final "
       "build &mdash; dance-music architecture inside a fusion track.")]),
    ("aos4-fusions", [4, 5], "8vOkY94xjnY", 330,
     "Official audio, streamed from YouTube &mdash; not hosted by "
     "StudyVault. Esperanza Spalding: Samba Em Preludio (2010).",
     "Samba Em Preludio",
     [(0, "Voice and bass alone", "The duet opening &mdash; rubato, "
       "intimate, the double bass as the only harmony."),
      (70, "Guitar and tempo", "Bossa nova comping arrives and the music "
       "finds its pulse."),
      (150, "Bass solo", "The virtuosic centrepiece &mdash; foundation "
       "instrument as soloist."),
      (240, "Voice returns", "The song material comes back with the "
       "ensemble now full."),
      (305, "Close", "The texture thins back towards the duet — the arch "
       "completing.")]),
]


def main():
    sb = get_client()
    sub = sb.table("subjects").select("id").eq("slug", "music-edexcel") \
        .execute().data[0]["id"]
    units = {u["slug"]: u["id"] for u in
             sb.table("units").select("id,slug,subject_id").execute().data
             if u["subject_id"] == sub}
    backup, writes = {}, []
    for uslug, nums, yt, dur, credit, label, pins in WORKS:
        for num in nums:
            row = sb.table("lessons").select("id,content_html") \
                .eq("unit_id", units[uslug]).eq("lesson_number", num) \
                .execute().data[0]
            ch = row["content_html"]
            if "sv-annotated-player" in ch:
                print("%s L%d: player already present — skipped" % (uslug, num))
                continue
            figs = re.findall(r'<figure class="sv-embed".*?</figure>', ch, re.S)
            target = [f for f in figs if "embed/%s" % yt in f]
            if not target:
                print("%s L%d: !! no embed of %s found" % (uslug, num, yt))
                continue
            ch = ch.replace(target[0],
                            player_html(row["id"], yt, dur, credit, label,
                                        pins))
            backup[row["id"]] = row["content_html"]
            writes.append((row["id"], ch))
            print("%s L%d: %s player in (%d pins)" % (uslug, num, label,
                                                      len(pins)))
    print("\nlessons to write:", len(writes))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, ch in writes:
        sb.table("lessons").update({"content_html": ch}).eq("id", lid) \
            .execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
