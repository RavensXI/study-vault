# -*- coding: utf-8 -*-
"""Teaching demos + method-panel guides for the Listening Skills unit.

Tom's review finding (6 Aug): the tonality drill quizzes pentatonic /
chromatic / whole-tone / minor without ever teaching them. Fix: five
constructed demo melodies (true by construction — the notes ARE the
tonality) embedded in a method-panel guide, plus text guides for L2's
families and L3's textures/devices/cadences covering every option word
the problems use.

Demos: same instrument (flute), same C centre, same tempo — tonality is the
only variable. Rendered via FluidSynth + FluidR3_GM like the drill excerpts.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from music21 import instrument, meter, note, stream, tempo
from lib.supabase_client import get_client
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL

FS = r"C:\Users\tshau\.claude\jobs\4059242c\tmp\fluidsynth\bin\fluidsynth.exe"
SF = r"C:\Users\tshau\.claude\jobs\4059242c\tmp\FluidR3_GM.sf2"

# (name, [(pitch, quarterLength)...]) — one 4-bar phrase each, C-centred
DEMOS = {
    "major":      [("C4",1),("D4",1),("E4",1),("F4",1),("G4",1),("A4",1),("G4",2),
                   ("E4",1),("F4",1),("E4",1),("D4",1),("C4",4)],
    "minor":      [("C4",1),("D4",1),("E-4",1),("F4",1),("G4",1),("A-4",1),("G4",2),
                   ("E-4",1),("F4",1),("E-4",1),("D4",1),("C4",4)],
    "pentatonic": [("C4",1),("D4",1),("E4",1),("G4",1),("A4",1),("G4",1),("E4",2),
                   ("D4",1),("E4",1),("G4",1),("A4",1),("G4",4)],
    "chromatic":  [("C4",1),("C#4",1),("D4",1),("E-4",1),("E4",1),("F4",1),("F#4",2),
                   ("G4",1),("A-4",1),("A4",1),("B-4",1),("B4",4)],
    "wholetone":  [("C4",1),("D4",1),("E4",1),("F#4",1),("G#4",1),("A#4",1),("C5",2),
                   ("A#4",1),("G#4",1),("F#4",1),("E4",1),("D4",4)],
}


def render(name, notes_seq):
    part = stream.Part()
    part.insert(0, instrument.Flute())
    part.insert(0, tempo.MetronomeMark(number=96))
    part.insert(0, meter.TimeSignature("4/4"))
    for p, ql in notes_seq:
        n = note.Note(p)
        n.quarterLength = ql
        part.append(n)
    sc = stream.Score([part])
    tmp = tempfile.mkdtemp()
    midi = os.path.join(tmp, name + ".mid")
    wav = os.path.join(tmp, name + ".wav")
    mp3 = os.path.join(tmp, name + ".mp3")
    sc.write("midi", fp=midi)
    subprocess.run([FS, "-ni", "-F", wav, "-r", "44100", SF, midi],
                   check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-i", wav, "-codec:a", "libmp3lame",
                    "-b:a", "96k", "-ar", "24000", "-ac", "1", mp3],
                   check=True, capture_output=True)
    with open(mp3, "rb") as f:
        return f.read()


AUD = ('<div class="ls-demo"><strong>%s</strong> &mdash; %s'
       '<br><audio controls preload="none" src="%s/music-aqa/listening-skills/demo_%s.mp3"></audio></div>')

L1_GUIDE = (
    "<p><strong>The five tonalities, with the same tune in each</strong> &mdash; "
    "same instrument, same speed, same home note. The scale is the only thing "
    "that changes, so the difference you hear IS the tonality.</p>"
    + AUD % ("Major", "bright, open, settled &mdash; the &lsquo;do-re-mi&rsquo; sound; it feels finished when it lands home.", AUDIO_PUBLIC_URL, "major")
    + AUD % ("Minor", "the same tune darkened &mdash; the third note of the scale is lowered, which is the sadness you hear.", AUDIO_PUBLIC_URL, "minor")
    + AUD % ("Pentatonic", "only five notes, no semitone clashes &mdash; folk-song open sound; nothing ever rubs.", AUDIO_PUBLIC_URL, "pentatonic")
    + AUD % ("Chromatic", "creeping by semitones &mdash; every step is the smallest possible; slippery, unsettled, no home.", AUDIO_PUBLIC_URL, "chromatic")
    + AUD % ("Whole-tone", "every step a whole tone &mdash; floating and dreamlike; with no semitones there is no pull to a home note.", AUDIO_PUBLIC_URL, "wholetone")
    + "<p>Drill tactic: first decide <em>settled or unsettled</em>. Settled &rarr; major, minor or pentatonic (bright / dark / open-folk). Unsettled &rarr; chromatic (creeping) or whole-tone (floating).</p>"
)

L2_GUIDE = (
    "<p><strong>The four families and their sound signatures:</strong></p>"
    "<p><strong>Strings</strong> &mdash; warm and singing; can be smooth (bowed, <em>arco</em>) or plucked (<em>pizzicato</em>); the sound can swell after a note starts.</p>"
    "<p><strong>Woodwind</strong> &mdash; breathy (flute), reedy and slightly nasal (oboe), smooth and hollow in the low register (clarinet); notes speak instantly.</p>"
    "<p><strong>Brass</strong> &mdash; metallic bloom and power; bright blaze (trumpet), rounded and golden (horn); loud playing gets a brassy edge.</p>"
    "<p><strong>Percussion</strong> &mdash; struck sounds; pitched (timpani&rsquo;s deep boom) or unpitched (snare, cymbals); attack first, ring after.</p>"
    "<p>Drill tactic: how does each note <em>start</em>? Breath = woodwind, bow-bite = strings, metallic bloom = brass, a hit = percussion.</p>"
)

L3_GUIDE = (
    "<p><strong>Texture</strong> &mdash; how many layers, doing what. <em>Monophonic</em>: one line alone. <em>Unison</em>: everyone playing the same line together. "
    "<em>Melody and accompaniment</em>: one tune on top, chords underneath. <em>Imitative polyphony</em> (or <em>imitation</em>): the same idea entering in one voice after another, overlapping.</p>"
    "<p><strong>Devices</strong> &mdash; <em>ostinato</em>: a short pattern repeated over and over. <em>Sequence</em>: the same phrase repeated a step higher or lower. "
    "<em>Drone</em>: one long held or repeated note underneath everything. <em>Imitation</em>: an idea copied between parts moments apart.</p>"
    "<p><strong>Cadences</strong> &mdash; the two-chord punctuation at a phrase end. <em>Perfect</em> (V&ndash;I): a full stop &mdash; finished. <em>Plagal</em> (IV&ndash;I): the softer &lsquo;Amen&rsquo; ending. "
    "<em>Imperfect</em> (ends on V): a comma &mdash; music left hanging. <em>Interrupted</em> (V&ndash;vi): the surprise &mdash; you expect home and get somewhere darker.</p>"
    "<p><strong>Metre</strong> &mdash; <em>simple time in 2 or 4</em>: beats divide in twos (marching). <em>Simple triple, in 3</em>: waltz-time. "
    "<em>Compound time (6/8)</em>: beats divide in threes &mdash; a lilting, skipping feel (jigs).</p>"
)

DRY = "--dry-run" in sys.argv
sb = get_client()
s = [x for x in sb.table("subjects").select("id,school_id").eq(
    "slug", "music-aqa").execute().data if not x["school_id"]][0]
u = [x for x in sb.table("units").select("id,slug").eq(
    "subject_id", s["id"]).execute().data if x["slug"] == "listening-skills"][0]

if not DRY:
    r2 = get_r2_client()
    for name, seq in DEMOS.items():
        mp3 = render(name, seq)
        key = "music-aqa/listening-skills/demo_%s.mp3" % name
        upload_bytes_to_r2(r2, AUDIO_BUCKET, key, mp3, "audio/mpeg")
        print("uploaded %s (%dKB)" % (key, len(mp3) // 1024))

GUIDES = {1: ("What the five tonalities sound like", L1_GUIDE),
          2: ("The four families' sound signatures", L2_GUIDE),
          3: ("Every term the questions use, defined", L3_GUIDE)}
for num, (title, content) in GUIDES.items():
    l = sb.table("lessons").select("id,practice_data").eq(
        "unit_id", u["id"]).eq("lesson_number", num).single().execute().data
    pd = l["practice_data"]
    mc = pd.get("method_card") or {}
    mc["content"] = content
    pd["method_card"] = mc
    if not DRY:
        sb.table("lessons").update({"practice_data": pd}).eq("id", l["id"]).execute()
    print("method guide %s L%d: %s (%d chars)" % ("set" if not DRY else "würde",
                                                  num, title, len(content)))
print("done")
