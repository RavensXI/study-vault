# -*- coding: utf-8 -*-
"""Rebalance Listening Skills L2 (instrument families drill).

Tom's finding + audit: 7 of 10 answers were 'strings', and brass and
percussion were NEVER correct — every excerpt was recycled from the
metre/texture/device drills, which are string- and flute-led. Eleven
purpose-composed excerpts: woodwind 3, strings 3, brass 3, percussion 2.
  bronze  solo melodies with unmistakable timbre (flute, trumpet, cello, xylophone)
  silver  melody over a quiet pad from a DIFFERENT family (oboe, violin, horn, timpani)
  gold    the confusable registers (low clarinet, mid viola, mid horn)
True by construction: the instrument on the moving line IS the answer.
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

MAJOR = [0, 2, 4, 5, 7, 9, 11, 12]
MINOR = [0, 2, 3, 5, 7, 8, 10, 12]

MEL_A = [(0,1),(2,1),(4,1),(2,.5),(4,.5),(5,1),(4,1),(2,1),(4,2),
         (7,1),(6,.5),(5,.5),(4,1),(2,1),(1,1),(2,1),(0,2),
         (4,1),(5,1),(7,1),(5,.5),(4,.5),(2,1),(4,1),(1,1),(0,3)]
MEL_B = [(0,1),(2,1),(2,.5),(3,.5),(4,1),(3,1),(2,1),(1,1),(2,2),
         (5,1),(4,.5),(3,.5),(2,1),(3,1),(2,1),(1,1),(0,2),
         (3,1),(4,1),(5,1),(4,.5),(3,.5),(2,1),(1,1),(2,1),(0,3)]
MEL_C = [(0,.5),(1,.5),(2,1),(4,1),(2,1),(4,.5),(5,.5),(7,2),
         (6,1),(5,1),(4,1),(2,1),(4,.5),(2,.5),(1,1),(0,2),
         (2,1),(4,1),(5,1),(4,1),(2,.5),(1,.5),(0,3)]
TIMP = [(0,1),(0,.5),(0,.5),(4,1),(0,1),(4,.5),(4,.5),(0,2),
        (0,.5),(0,.5),(4,1),(0,1),(4,1),(0,1),(0,3)]   # tonic-dominant strokes

I = {"flute": instrument.Flute, "oboe": instrument.Oboe,
     "clarinet": instrument.Clarinet, "violin": instrument.Violin,
     "viola": instrument.Viola, "cello": instrument.Violoncello,
     "trumpet": instrument.Trumpet, "horn": instrument.Horn,
     "xylophone": instrument.Xylophone, "timpani": instrument.Timpani}
PAD = {"strings": instrument.Violoncello, "woodwind": instrument.Clarinet,
       "brass": instrument.Horn, None: None}

# (id, family, melody instrument, root, scale, bpm, melody, pad family or None)
EX = [
    ("exF01", "woodwind",   "flute",     "G4",  MAJOR, 104, MEL_A, None),
    ("exF02", "brass",      "trumpet",   "C4",  MAJOR, 108, MEL_C, None),
    ("exF03", "strings",    "cello",     "C3",  MINOR,  84, MEL_B, None),
    ("exF04", "percussion", "xylophone", "C5",  MAJOR, 112, MEL_C, None),
    ("exF05", "woodwind",   "oboe",      "D4",  MINOR,  92, MEL_B, "strings"),
    ("exF06", "strings",    "violin",    "A3",  MAJOR,  96, MEL_A, "brass"),
    ("exF07", "brass",      "horn",      "F3",  MAJOR,  88, MEL_B, "strings"),
    ("exF08", "percussion", "timpani",   "C2",  MAJOR,  92, TIMP,  "strings"),
    ("exF09", "woodwind",   "clarinet",  "E3",  MINOR,  80, MEL_B, "strings"),
    ("exF10", "strings",    "viola",     "C3",  MAJOR,  90, MEL_A, "woodwind"),
    ("exF11", "brass",      "horn",      "C3",  MINOR,  84, MEL_A, "woodwind"),
]


def build(eid, fam, inst, root, scale, bpm, seq, padfam):
    rp = pitch.Pitch(root)
    mel = stream.Part()
    mel.insert(0, I[inst]())
    mel.insert(0, tempo.MetronomeMark(number=bpm))
    mel.insert(0, meter.TimeSignature("4/4"))
    total = 0
    for deg, ql in seq:
        n = note.Note(rp.midi + scale[deg % len(scale)] + 12 * (deg // len(scale)))
        n.quarterLength = ql
        n.volume.velocity = 96
        mel.append(n)
        total += ql
    parts = [mel]
    if padfam:
        acc = stream.Part()
        acc.insert(0, PAD[padfam]())
        t = 0
        base = rp.midi - 12 if rp.midi > 48 else rp.midi + 12
        while t < total:
            c = chord.Chord([base, base + 7])
            c.quarterLength = min(4, total - t)
            for cn in c.notes:
                cn.volume.velocity = 52          # pad well under the melody
            acc.append(c)
            t += 4
        parts.append(acc)
    sc = stream.Score(parts)
    tmp = tempfile.mkdtemp()
    midi, wav, mp3 = (os.path.join(tmp, eid + e) for e in (".mid", ".wav", ".mp3"))
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
    "unit_id", u["id"]).eq("lesson_number", 2).single().execute().data
pd = row["practice_data"]
tmpl = pd["passages"][0]

if not DRY:
    r2 = get_r2_client()
new_passages = []
for eid, fam, inst, root, scale, bpm, seq, padfam in EX:
    key = "music-aqa/listening-skills/%s.mp3" % eid
    if not DRY:
        mp3 = build(eid, fam, inst, root, scale, bpm, seq, padfam)
        upload_bytes_to_r2(r2, AUDIO_BUCKET, key, mp3, "audio/mpeg")
        print("uploaded %s (%s: %s%s, %dKB)" % (eid, fam, inst,
              " + %s pad" % padfam if padfam else " solo", len(mp3) // 1024))
    p = dict(tmpl)
    p["id"] = eid + "_family"
    p["text"] = tmpl["text"].replace(
        [x for x in tmpl["text"].split('"') if ".mp3" in x][0],
        "%s/%s" % (AUDIO_PUBLIC_URL, key))
    new_passages.append(p)

FAMS = ["woodwind", "strings", "brass", "percussion"]


def prob(pid, ans, qid):
    rng = random.Random(qid * 7919)
    opts = list(FAMS)
    rng.shuffle(opts)
    return {"question": "Which instrument family plays the main melody?",
            "options": opts, "solutions": [opts.index(ans)],
            "input_type": "multiple_choice", "passage_id": pid,
            "explanation": "Verified answer: %s. This excerpt was composed so "
                           "the moving melodic line belongs unambiguously to "
                           "the %s family &mdash; the method panel describes "
                           "each family&rsquo;s sound signature." % (ans, ans)}


BANK = {
    "bronze": [prob("exF01_family", "woodwind", 31),
               prob("exF02_family", "brass", 32),
               prob("exF03_family", "strings", 33),
               prob("exF04_family", "percussion", 34)],
    "silver": [prob("exF05_family", "woodwind", 35),
               prob("exF06_family", "strings", 36),
               prob("exF07_family", "brass", 37),
               prob("exF08_family", "percussion", 38)],
    "gold":   [prob("exF09_family", "woodwind", 39),
               prob("exF10_family", "strings", 40),
               prob("exF11_family", "brass", 41)],
}
pd["passages"] = new_passages
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
