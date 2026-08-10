# -*- coding: utf-8 -*-
"""Rebalance Listening Skills L1 (tonality drill).

Tom's finding: 9 of 11 answers were 'major', because most questions reused
cadence/pop excerpts that are major by design. Fix: nine purpose-composed
tonality excerpts (2 major, 3 minor, 2 pentatonic incl. the existing one,
2 chromatic incl. existing, 2 whole-tone) and a rebuilt problem bank:
  bronze  major, minor, minor, pentatonic          (bright/dark foundations)
  silver  major, pentatonic, chromatic, minor      (adds the odd ones out)
  gold    whole-tone, chromatic, whole-tone        (the hard discriminations)
Every clip is true by construction — the scale content IS the answer.
Melody + octave doubling only for chromatic/whole-tone (a chordal pad would
smuggle tonality in); maj/min get a root-fifth string pad; pentatonic gets a
folk-style open-fifth drone.
"""
import os
import random
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from music21 import chord, instrument, meter, note, pitch, stream, tempo
from lib.supabase_client import get_client
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL

FS = r"C:\Users\tshau\.claude\jobs\4059242c\tmp\fluidsynth\bin\fluidsynth.exe"
SF = r"C:\Users\tshau\.claude\jobs\4059242c\tmp\FluidR3_GM.sf2"

SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11, 12],
    "minor": [0, 2, 3, 5, 7, 8, 10, 12],
    "pentatonic": [0, 2, 4, 7, 9, 12],
    "chromatic": list(range(13)),
    "whole-tone": [0, 2, 4, 6, 8, 10, 12],
}
INSTR = {"flute": instrument.Flute, "oboe": instrument.Oboe,
         "violin": instrument.Violin, "clarinet": instrument.Clarinet,
         "cello": instrument.Violoncello}

# (excerpt id, tonality, root, melodic instrument, bpm, scale-index melody
#  with rhythm) — melodies hand-shaped: maj/min anchor the root and colour
#  the 3rd; chromatic wanders without an anchor; whole-tone floats.
MEL = [
    ("exT01", "major", "G3", "violin", 104,
     [(0,1),(2,1),(4,1),(2,.5),(4,.5),(5,1),(4,1),(2,1),(4,2),
      (7,1),(6,.5),(5,.5),(4,1),(2,1),(1,1),(2,1),(0,2),
      (4,1),(5,1),(7,1),(5,.5),(4,.5),(2,1),(4,1),(1,1),(0,3)]),
    ("exT02", "minor", "D4", "oboe", 92,
     [(0,1),(2,1),(2,.5),(3,.5),(4,1),(3,1),(2,1),(1,1),(2,2),
      (5,1),(4,.5),(3,.5),(2,1),(3,1),(2,1),(1,1),(0,2),
      (3,1),(4,1),(5,1),(4,.5),(3,.5),(2,1),(1,1),(2,1),(0,3)]),
    ("exT03", "minor", "A3", "cello", 84,
     [(0,2),(2,1),(3,1),(2,1),(0,1),(3,1),(2,1),(1,2),
      (4,1),(5,1),(4,1),(3,1),(2,1),(3,.5),(2,.5),(1,1),(0,3)]),
    ("exT04", "major", "E-4", "clarinet", 112,
     [(0,.5),(1,.5),(2,1),(4,1),(2,1),(4,.5),(5,.5),(7,2),
      (6,1),(5,1),(4,1),(2,1),(4,.5),(2,.5),(1,1),(0,2),
      (2,1),(4,1),(5,1),(4,1),(2,.5),(1,.5),(0,3)]),
    ("exT05", "pentatonic", "F4", "flute", 96,
     [(0,1),(1,1),(2,1),(3,1),(4,1),(3,1),(2,2),
      (1,.5),(2,.5),(3,1),(4,1),(5,1),(4,1),(3,1),(2,1),(0,2),
      (2,1),(3,1),(4,.5),(3,.5),(2,1),(1,1),(0,3)]),
    ("exT06", "minor", "G4", "flute", 100,
     [(0,1),(1,1),(2,1),(4,1),(3,1),(2,1),(1,1),(2,2),
      (4,1),(5,.5),(4,.5),(3,1),(2,1),(1,1),(2,.5),(1,.5),(0,3)]),
    ("exT07", "whole-tone", "C4", "violin", 88,
     [(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,2),
      (5,1),(4,.5),(3,.5),(2,1),(4,1),(1,1),(3,1),(5,2),
      (4,1),(2,1),(3,1),(1,1),(2,3)]),
    ("exT08", "chromatic", "E4", "cello", 80,
     [(0,1),(1,1),(2,.5),(3,.5),(4,1),(3,1),(5,1),(6,1),(7,2),
      (8,1),(7,.5),(6,.5),(9,1),(8,1),(10,1),(11,1),(12,2),
      (11,1),(9,.5),(10,.5),(8,1),(7,1),(6,2)]),
    ("exT09", "whole-tone", "E-4", "oboe", 96,
     [(0,1),(2,1),(1,1),(3,1),(2,1),(4,1),(3,2),
      (5,1),(6,.5),(5,.5),(4,1),(2,1),(3,1),(5,1),(1,2),
      (4,1),(3,1),(2,1),(1,1),(0,3)]),
]


def build(eid, ton, root, inst, bpm, seq):
    scale = SCALES[ton]
    rp = pitch.Pitch(root)
    mel = stream.Part()
    mel.insert(0, INSTR[inst]())
    mel.insert(0, tempo.MetronomeMark(number=bpm))
    mel.insert(0, meter.TimeSignature("4/4"))
    total = 0
    for deg, ql in seq:
        n = note.Note(rp.midi + scale[deg % len(scale)] + 12 * (deg // len(scale)))
        n.quarterLength = ql
        mel.append(n)
        total += ql
    parts = [mel]
    acc = stream.Part()
    acc.insert(0, instrument.Violoncello() if inst != "cello" else instrument.Viola())
    if ton in ("major", "minor"):        # root-fifth pad, no 3rd: no extra colour
        t = 0
        while t < total:
            c = chord.Chord([rp.midi - 12, rp.midi - 5])
            c.quarterLength = min(4, total - t)
            acc.append(c)
            t += 4
    elif ton == "pentatonic":            # folk open-fifth drone
        t = 0
        while t < total:
            c = chord.Chord([rp.midi - 12, rp.midi - 5])
            c.quarterLength = min(4, total - t)
            acc.append(c)
            t += 4
    else:                                 # chromatic / whole-tone: octave double
        for deg, ql in seq:
            n = note.Note(rp.midi - 12 + scale[deg % len(scale)] + 12 * (deg // len(scale)))
            n.quarterLength = ql
            acc.append(n)
    parts.append(acc)
    sc = stream.Score(parts)
    tmp = tempfile.mkdtemp()
    midi, wav, mp3 = (os.path.join(tmp, eid + ext) for ext in (".mid", ".wav", ".mp3"))
    sc.write("midi", fp=midi)
    subprocess.run([FS, "-ni", "-F", wav, "-r", "44100", SF, midi],
                   check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-i", wav, "-codec:a", "libmp3lame",
                    "-b:a", "96k", "-ar", "24000", "-ac", "1", mp3],
                   check=True, capture_output=True)
    with open(mp3, "rb") as f:
        return f.read()


DRY = "--dry-run" in sys.argv
sb = get_client()
s = [x for x in sb.table("subjects").select("id,school_id").eq(
    "slug", "music-aqa").execute().data if not x["school_id"]][0]
u = [x for x in sb.table("units").select("id,slug").eq(
    "subject_id", s["id"]).execute().data if x["slug"] == "listening-skills"][0]
row = sb.table("lessons").select("id,practice_data").eq(
    "unit_id", u["id"]).eq("lesson_number", 1).single().execute().data
pd = row["practice_data"]

# clone the passage/explanation shape from the existing purpose-built clips
tmpl = next(p for p in pd["passages"] if p["id"] == "ex013_tonality")
keep = {p["id"]: p for p in pd["passages"]
        if p["id"] in ("ex013_tonality", "ex014_tonality")}

if not DRY:
    r2 = get_r2_client()
new_passages = []
for eid, ton, root, inst, bpm, seq in MEL:
    key = "music-aqa/listening-skills/%s.mp3" % eid
    if not DRY:
        mp3 = build(eid, ton, root, inst, bpm, seq)
        upload_bytes_to_r2(r2, AUDIO_BUCKET, key, mp3, "audio/mpeg")
        print("uploaded %s (%s, %s, %dKB)" % (eid, ton, inst, len(mp3) // 1024))
    p = dict(tmpl)
    p["id"] = eid + "_tonality"
    p["text"] = tmpl["text"].replace(
        [x for x in tmpl["text"].split('"') if "listening-skills" in x][0],
        "%s/%s" % (AUDIO_PUBLIC_URL, key))
    new_passages.append(p)

ALL_TERMS = ["major", "minor", "pentatonic", "chromatic", "whole-tone"]


def prob(pid, ans, qid):
    others = [t for t in ALL_TERMS if t != ans]
    rng = random.Random(qid * 7919)
    opts = [ans] + rng.sample(others, 3)
    rng.shuffle(opts)
    return {"question": "What is the tonality of this excerpt?",
            "options": opts, "solutions": [opts.index(ans)],
            "input_type": "multiple_choice", "passage_id": pid,
            "explanation": "Verified answer: %s. This excerpt was composed so "
                           "that its scale content makes the tonality "
                           "unambiguous &mdash; check the method panel for what "
                           "to listen for." % ans}


BANK = {
    "bronze": [prob("exT01_tonality", "major", 11),
               prob("exT02_tonality", "minor", 12),
               prob("exT03_tonality", "minor", 13),
               prob("ex013_tonality", "pentatonic", 14)],
    "silver": [prob("exT04_tonality", "major", 15),
               prob("exT05_tonality", "pentatonic", 16),
               prob("ex014_tonality", "chromatic", 17),
               prob("exT06_tonality", "minor", 18)],
    "gold":   [prob("exT07_tonality", "whole-tone", 19),
               prob("exT08_tonality", "chromatic", 20),
               prob("exT09_tonality", "whole-tone", 21)],
}

pd["passages"] = list(keep.values()) + new_passages
pd["problem_bank"] = BANK
from collections import Counter
dist = Counter(p["options"][p["solutions"][0]]
               for tier in BANK.values() for p in tier)
print("new distribution:", dict(dist))
if not DRY:
    sb.table("lessons").update({"practice_data": pd}).eq("id", row["id"]).execute()
    print("problem bank rebuilt: 11 problems")
else:
    print("DRY RUN - nothing written")
