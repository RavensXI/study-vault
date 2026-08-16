# -*- coding: utf-8 -*-
"""Wire the verified Flow-generated gold clips into the RotW drills
(L1 India & Punjab, L3 Africa, L4 Americas). Every clip shipped here
passed final-artefact probes (3-vote where contested); the call-and-
response generation FAILED verification 0/3 on both takes and is NOT
wired — its synthetic question stays, and the regen note lives in
FLOW_PROMPT_PACK_ROTW.md.

L1: replaces the 3 placeholder hard-synth gold questions with 4 on the
real generated clips. L3: adds the build clip + 2 questions, keeping 2
synth gold. L4: adds the steel pan clip + 2 questions alongside the 4
Dengozo questions.

Run: python wire_rotw_gold_gen.py [--apply]
Backup: _backup_rotw_gold_gen_2026-08-16.json
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client
from gen_drill_peaks import peaks_for
from build_rotw_drills import player_html, mc

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_rotw_gold_gen_2026-08-16.json")
R2 = "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/music-ocr/aos3-rhythms-listening/"
GEN_NOTE = ("AI-generated demonstration in the style of the tradition "
            "&middot; studio-built for this drill")


def passage(pid, heading, filename):
    peaks, dur = peaks_for(os.path.join(HERE, "_rotw_goldcut", filename))
    html = ('<div style="text-align:center;"><p style="font-family:Inter,'
            'sans-serif;font-size:0.95rem;color:var(--text-primary);'
            'margin-bottom:0.75rem;">%s<br><span style="font-size:0.8rem;'
            'color:var(--text-secondary);">%s</span></p>%s</div>'
            % (heading, GEN_NOTE,
               player_html(R2 + filename, {"peaks": peaks, "duration": dur})))
    return {"id": pid, "text": html}


L1_PASSAGES = [
    passage("p-gen-bhangra", "Modern bhangra groove",
            "gold_gen_bhangra.mp3"),
    passage("p-gen-alap", "Sitar, tanpura and tabla &mdash; opening",
            "gold_gen_sitar_alap.mp3"),
    passage("p-gen-cycle", "Sitar, tanpura and tabla &mdash; rhythmic "
            "section", "gold_gen_sitar_cycle.mp3"),
]
L1_GOLD = [
    mc("p-gen-bhangra", "This bhangra track mixes a traditional drum with "
       "modern production. Which pairing do you hear?",
       ["A large double-headed drum (low strokes on the beat, high cracks "
        "between) over a programmed club kick and synth stabs",
        "An orchestra with a drum machine",
        "Solo tabla with no production at all",
        "A steel pan band with autotuned vocals"],
       0, "The dhol leads exactly as it would at a festival — deep dagga "
       "strokes on the beat, sharp tilli cracks between — while the "
       "production underneath (programmed kick, synth stabs) is modern "
       "club machinery. That traditional-meets-technology layering is the "
       "spec's own bullet on modern bhangra.",
       ("dhol-vs-drum-machine", 1,
        "The kick drum IS programmed, but listen above it: the lead drum "
        "alternates two hand-struck sounds, low and high — the "
        "double-headed dhol, not a machine.")),
    mc("p-gen-bhangra", "How are the quick notes between the beats "
       "treated?",
       ["Swung — each pair divides long-short, giving the groove its "
        "bounce", "Perfectly even and mechanical",
        "In groups of seven", "There are no quick notes"],
       0, "The chaal's swing survives the modern production: pairs of "
       "quavers divide long-short throughout. Swing is the first thing "
       "to name in any bhangra answer.", None),
    mc("p-gen-alap", "In this opening section, what holds the music "
       "together underneath the melody?",
       ["A constant drone sustaining the home note(s) throughout",
        "A walking bass line", "Block chords changing every bar",
        "Nothing — the melody is alone"],
       0, "The tanpura's unbroken drone anchors everything: the sitar's "
       "slides and shakes are heard AGAINST that fixed reference. "
       "Drone + ornamented melody + (later) cycle percussion is the "
       "classic three-layer texture of this tradition.",
       ("drone-vs-bass", 1,
        "A walking bass MOVES by step through different pitches; this "
        "layer never moves at all — one sustained sound throughout, "
        "which is a drone.")),
    mc("p-gen-cycle", "Compare this section with the opening. What has "
       "been added, and what does it bring?",
       ["Hand drums keeping a repeating cycle — a fixed rhythmic "
        "framework arrives under the free-flowing melody",
        "A second melody instrument in harmony",
        "A Western drum kit playing a backbeat",
        "Nothing has changed"],
       0, "The tabla enters with its repeating cycle, and the "
       "performance moves from free, unmeasured opening (alap-like) "
       "into measured time. Structure through PERCUSSION arriving is "
       "how this tradition marks its sections.", None),
]

L3_PASSAGE = passage("p-gen-build", "West African percussion ensemble "
                     "&mdash; opening", "gold_gen_african_build.mp3")
L3_GOLD_ADD = [
    mc("p-gen-build", "Describe how this performance begins and grows.",
       ["A bell pattern starts alone, then shaker and drums join layer "
        "by layer, thickening the texture",
        "The full ensemble plays from the first note",
        "A solo singer opens before the drums",
        "It begins loud and gradually thins out"],
       0, "The iron bell opens alone as the timeline; the ensemble "
       "assembles around it layer by layer. Describing texture as a "
       "PROCESS — what enters, in what order, with what effect — is "
       "gold-standard exam writing.", None),
    mc("p-gen-build", "What is the ensemble made of?",
       ["Drums, bell and shaker only — no melody instruments",
        "Drums plus a flute melody", "Drums plus singing",
        "A full band with bass and keyboards"],
       0, "Pure percussion: bell timeline, shaker, layered drums. In "
       "much West African drumming the ENSEMBLE IS the music — melody "
       "and harmony are not required for a complete texture.", None),
]

L4_PASSAGE = passage("p-gen-steelpan", "Steel pan band &mdash; calypso "
                     "groove", "gold_gen_steelpan.mp3")
L4_GOLD_ADD = [
    mc("p-gen-steelpan", "Three jobs are being done by the pans. Which "
       "description matches what you hear?",
       ["High pans carry the tune, middle pans strum offbeat chords, a "
        "bass pan walks underneath",
        "All the pans play the melody together in unison",
        "The pans only play long held chords",
        "One solo pan plays unaccompanied"],
       0, "A steel band is a complete orchestra built from oil drums: "
       "tenor pans on melody, mid-range pans strumming the offbeats "
       "(the 'strumming' section), bass pans walking the harmony. "
       "Naming the ROLES is what earns the marks.", None),
    mc("p-gen-steelpan", "Listen to the accent pattern driving the "
       "groove. How are the quick pulses grouped?",
       ["3+3+2 — two longer groups then a short one snapping the bar "
        "shut", "4+4 — completely straight", "3+2+2", "In threes, like "
        "a waltz"],
       0, "The calypso engine: quavers grouped 3+3+2 against a steady "
       "duple pulse — the same tresillo grouping you met in the "
       "synthesised drill, now inside a full band groove.",
       ("tresillo-vs-straight", 1,
        "There IS a steady pulse underneath, but the accents on top "
        "do not land every four — count them against the pulse and "
        "you get the uneven 3+3+2.")),
]


def main():
    sb = get_client()
    sub = sb.table("subjects").select("id").eq("slug", "music-ocr") \
        .execute().data[0]["id"]
    units = {u["slug"]: u["id"] for u in
             sb.table("units").select("id,slug,subject_id").execute().data
             if u["subject_id"] == sub}
    uid = units["aos3-rhythms-listening"]
    backup, writes = {}, []
    rows = {r["lesson_number"]: r for r in sb.table("lessons")
            .select("id,lesson_number,practice_data").eq("unit_id", uid)
            .execute().data}

    # L1: add passages, REPLACE placeholder gold
    pd = rows[1]["practice_data"]
    have = {p["id"] for p in pd["passages"]}
    if "p-gen-bhangra" not in have:
        pd["passages"].extend(L1_PASSAGES)
        pd["problem_bank"]["gold"] = L1_GOLD
        backup[rows[1]["id"]] = "replaced gold (3 placeholder) + 3 passages"
        writes.append((rows[1]["id"], pd))
        print("L1: +3 passages, gold replaced (3 placeholder -> 4 real)")

    # L3: add build passage + 2 questions, keep 2 of 3 synth gold
    pd = rows[3]["practice_data"]
    have = {p["id"] for p in pd["passages"]}
    if "p-gen-build" not in have:
        pd["passages"].append(L3_PASSAGE)
        kept = [p for p in pd["problem_bank"]["gold"]
                if "COMPARE" not in p["question"]
                and "density" not in p["question"].lower()][:2]
        pd["problem_bank"]["gold"] = kept + L3_GOLD_ADD
        backup[rows[3]["id"]] = "gold now 2 synth + 2 gen; +1 passage"
        writes.append((rows[3]["id"], pd))
        print("L3: +1 passage, gold = 2 synth + 2 generated")

    # L4: add steel pan passage + 2 questions alongside Dengozo's 4
    pd = rows[4]["practice_data"]
    have = {p["id"] for p in pd["passages"]}
    if "p-gen-steelpan" not in have:
        pd["passages"].append(L4_PASSAGE)
        pd["problem_bank"]["gold"] = pd["problem_bank"]["gold"] + L4_GOLD_ADD
        backup[rows[4]["id"]] = "gold 4 Dengozo + 2 steelpan; +1 passage"
        writes.append((rows[4]["id"], pd))
        print("L4: +1 passage, gold = 4 Dengozo + 2 steel pan")

    print("lessons to write:", len(writes))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, pd in writes:
        sb.table("lessons").update({"practice_data": pd}).eq("id", lid) \
            .execute()
    print("applied.")


if __name__ == "__main__":
    main()
