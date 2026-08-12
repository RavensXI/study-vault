# -*- coding: utf-8 -*-
"""Trim, upload and wire the four AoS2 Flow clips into aos-listening L1.

Closes the last AoS2 gap: bronze +1, silver +1, gold +2.

Questions rest on INSTRUMENTATION and construction, not on measured timing.
Beat-spread turned out not to measure programmed-vs-played at all (see
audio_features.py), but instrumentation is both reliably measurable — real kit
and real bass were confirmed on every clip — and audible to a non-specialist,
which is what makes the keys checkable.

The four map onto AQA's four AoS2 strands: rock of the 60s-70s, pop from the
90s, Broadway 1950s-90s, and film/computer gaming music from the 90s.

    python wire_aos2_flow.py [--dry-run|--restore]
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL

DL = r"C:\Users\tshau\Downloads"
DEST = "music-aqa/aos-listening/%s"
BACKUP = os.path.join(HERE, "_aos2_flow_backup.json")

# src file, out name, start, length, tier, strand
CLIPS = [
    ("aos2_rock_60s70s_a.wav", "aos2_rock_live_band", 20, 18, "bronze"),
    ("aos2_pop_90s_now_v2aa.wav", "aos2_pop_programmed", 20, 18, "silver"),
    ("aos2_broadway_a.wav", "aos2_broadway_pit", 20, 18, "gold"),
    ("aos2_gaming_loop_a.wav", "aos2_gaming_layers", 20, 18, "gold"),
]

PLAYER = ('<div style="text-align:center"><p style="font-family:Inter,system-ui,sans-serif;'
          'font-size:.9rem;margin:0 0 .6rem">Listen to the extract, then answer.</p>'
          '<audio controls preload="metadata" src="%s" style="width:100%%;max-width:460px"></audio>'
          '<p style="font-size:.72rem;opacity:.55;margin:.5rem 0 0">Purpose-made study extract. '
          'No commercial recording is used.</p></div>')

Q = {
    "aos2_rock_live_band": (
        "bronze",
        "Listen to the extract. Which combination of instruments do you hear?",
        ["A full orchestra with strings and brass",
         "Electric guitar, bass guitar, drum kit and organ",
         "Synthesisers and a programmed drum machine only",
         "Solo piano with no accompaniment"], 1,
        "This is a rock band line-up: overdriven electric guitar, electric bass, an acoustic drum "
        "kit with room around it, and organ underneath. That combination points to the rock strand "
        "of Area of Study 2 — the music of the 1960s and 1970s."),
    "aos2_pop_programmed": (
        "silver",
        "Listen to the extract. Which features suggest this was made from the 1990s onwards?",
        ["A pit orchestra with lush strings",
         "Overdriven guitar and a Hammond organ",
         "Synthesised bass and pads over a repeating loop, with everything compressed loud and level",
         "A harpsichord playing continuo"], 2,
        "Synthesised bass, synth pads, a short loop running underneath and a heavily compressed mix "
        "are the marks of modern pop production. Compare the rock extract in this lesson, which is "
        "built from instruments played together in a room."),
    "aos2_broadway_pit": (
        "gold",
        "Listen to the extract. Which strand of Area of Study 2 does it belong to, and what tells you?",
        ["Film and computer gaming music — it uses electronic percussion",
         "Broadway — a pit orchestra of strings, brass and woodwind carrying a singable show tune",
         "Rock of the 1960s and 1970s — it has a backbeat",
         "Pop from the 1990s — the beat is programmed"], 1,
        "Lush strings, bright brass and woodwind, with a clear melodic tune and a lift towards the "
        "end, are the sound of a Broadway pit orchestra. Area of Study 2 covers Broadway from the "
        "1950s to the 1990s, and the scoring is what identifies it."),
    "aos2_gaming_layers": (
        "gold",
        "Listen to the extract. One feature marks this out as music written for a video game rather "
        "than for a film. Which?",
        ["It uses an orchestra",
         "It is loud throughout",
         "It builds by adding and removing layers over a repeating pattern, and could run round "
         "again without a join",
         "It has no melody"], 2,
        "Film music is cut to a scene of known length, so it can end. Game music cannot know how "
        "long a scene will last, so it is written to loop seamlessly and to thicken or thin by "
        "layering instruments in and out. Orchestras and loud dynamics appear in both, so neither "
        "settles it."),
}


def main():
    dry = "--dry-run" in sys.argv
    sb = get_client()
    sub = [x for x in sb.table("subjects").select("id,slug,school_id")
           .eq("slug", "music-aqa").execute().data if not x["school_id"]][0]
    unit = [u for u in sb.table("units").select("id,slug").eq("subject_id", sub["id"])
            .execute().data if u["slug"] == "aos-listening"][0]["id"]
    row = sb.table("lessons").select("id,practice_data").eq("unit_id", unit) \
        .eq("lesson_number", 1).single().execute().data

    if "--restore" in sys.argv:
        sb.table("lessons").update({"practice_data": json.load(open(BACKUP, encoding="utf-8"))}) \
            .eq("id", row["id"]).execute()
        print("restored")
        return

    r2 = None if dry else get_r2_client()
    urls = {}
    for src, name, start, dur, _tier in CLIPS:
        p = os.path.join(DL, src)
        assert os.path.exists(p), "missing " + p
        out = os.path.join(os.environ.get("TEMP", "."), name + ".mp3")
        subprocess.run(["ffmpeg", "-y", "-v", "quiet", "-ss", str(start), "-t", str(dur),
                        "-i", p, "-ac", "2", "-ar", "44100", "-b:a", "128k",
                        "-af", "afade=t=in:st=0:d=0.3,afade=t=out:st=%s:d=0.6" % (dur - 0.6),
                        out], check=True)
        data = open(out, "rb").read()
        assert len(data) > 40000, name
        if not dry:
            upload_bytes_to_r2(r2, AUDIO_BUCKET, DEST % (name + ".mp3"), data, "audio/mpeg")
        urls[name] = AUDIO_PUBLIC_URL + "/" + DEST % (name + ".mp3")
        print("  %-24s %5.0f KB  %s" % (name, len(data) / 1024.0, urls[name].rsplit("/", 1)[-1]))

    pd = json.loads(json.dumps(row["practice_data"]))
    before = {t: len(pd["problem_bank"][t]) for t in ("bronze", "silver", "gold")}
    for name, (tier, text, opts, correct, expl) in Q.items():
        if any(q.get("question") == text for q in pd["problem_bank"][tier]):
            continue
        pid = "p-" + name
        pd["passages"].append({"id": pid, "label": "Listening extract", "text": PLAYER % urls[name]})
        assert 0 <= correct < len(opts) and len(set(opts)) == len(opts)
        pd["problem_bank"][tier].append({
            "input_type": "multiple_choice", "passage_id": pid, "question": text,
            "options": opts, "solutions": [correct], "explanation": expl})

    after = {t: len(pd["problem_bank"][t]) for t in ("bronze", "silver", "gold")}
    assert all(after[t] >= 4 for t in after), after
    ids = {p["id"] for p in pd["passages"]}
    for t in after:
        for q in pd["problem_bank"][t]:
            assert q["passage_id"] in ids, q["passage_id"]
    if not dry:
        if not os.path.exists(BACKUP):
            json.dump(row["practice_data"], open(BACKUP, "w", encoding="utf-8"))
        sb.table("lessons").update({"practice_data": pd}).eq("id", row["id"]).execute()
    print("  bronze %d->%d  silver %d->%d  gold %d->%d"
          % (before["bronze"], after["bronze"], before["silver"], after["silver"],
             before["gold"], after["gold"]))
    print(("DRY RUN — " if dry else "") + "done")


if __name__ == "__main__":
    main()
