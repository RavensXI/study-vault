# -*- coding: utf-8 -*-
"""Batch 1c: the three excerpt classes Flow could not produce (proved by A/B
regeneration - it drifts Latin/new-age/film), built in the notation pipeline
where their defining features are structural and true by construction:

  aos3_african_fusion  - two interlocking clean-guitar ostinatos (3-beat vs
                         4-beat polymetre), balafon-style marimba pattern,
                         melodic bass. (Balafon IS West African tuned
                         percussion - more authentic than a drum kit here.)
  aos4_minimalism      - marimba + piano repeating a short cell, one note
                         ADDED every 8 bars (additive process), constant pulse.
  aos4_dissonant_modern- angular wide-leap fragments passed flute->violin->
                         trombone, semitone cluster stabs at irregular
                         intervals, pp/ff extremes, timpani.

Each renders then gets the standard 3-vote machine-ear verification.

Usage: python scripts/music-practice/compose_batch1c.py
"""
import base64
import io
import json
import os
import random
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from music21 import chord, instrument, note, stream, tempo, meter

import gen_excerpts as gx
import works_verify as wv

OUT = r"C:\Users\tshau\.claude\jobs\4059242c\tmp\flow_batch1b\trimmed"


def _inst(cls, program=None):
    i = cls()
    if program is not None:
        i.midiProgram = program
    return i


def build_fusion():
    # v2 timbre fix: v1's clean e-guitar + uniform velocity read as CHIPTUNE.
    # Steel acoustic + kalimba + humanised velocities read organic.
    s = stream.Score()
    rng = random.Random(17)
    g1 = stream.Part(); g1.insert(0, _inst(instrument.AcousticGuitar, 25))
    g1.insert(0, tempo.MetronomeMark(number=104)); g1.insert(0, meter.TimeSignature("4/4"))
    for _ in range(18):
        for p, d in [("E4", 0.5), ("G4", 0.5), ("A4", 0.5), ("E4", 0.5), ("G4", 0.5), ("A4", 0.5)]:
            g1.append(note.Note(p, quarterLength=d))
    g2 = stream.Part(); g2.insert(0, _inst(instrument.AcousticGuitar, 25))
    for _ in range(14):
        for p, d in [("C5", 0.5), ("B4", 0.5), ("A4", 0.5), ("C5", 0.5),
                     ("D5", 0.75), ("C5", 0.75), ("A4", 0.5)]:
            g2.append(note.Note(p, quarterLength=d))
    kal = stream.Part(); kal.insert(0, _inst(instrument.Kalimba, 108))
    for _ in range(27):
        for p, d in [("A3", 0.25), ("E4", 0.25), ("A4", 0.25), ("E4", 0.25),
                     ("G3", 0.25), ("D4", 0.25), ("G4", 0.25), ("D4", 0.25)]:
            kal.append(note.Note(p, quarterLength=d))
    bass = stream.Part(); bass.insert(0, _inst(instrument.AcousticBass, 32))
    for _ in range(9):
        for p, d in [("A1", 1.0), ("C2", 0.5), ("E2", 0.5), ("G1", 1.0), ("A1", 0.5), ("C2", 0.5),
                     ("A1", 1.0), ("E2", 1.0), ("G1", 1.0), ("A1", 1.0)]:
            bass.append(note.Note(p, quarterLength=d))
    for p in (g1, g2, kal, bass):
        s.insert(0, p)
    for n in s.recurse().notes:
        n.volume.velocity = rng.randint(76, 102)
    return s


def build_minimalism():
    # v2 timbre fix: slower, piano carries the low octave with gentle varied
    # touch (acoustic read), marimba stays mid-register; still strict additive.
    s = stream.Score()
    rng = random.Random(29)
    cell = [("E4", 0.25), ("G4", 0.25), ("B4", 0.25), ("A4", 0.25)]
    add1 = cell + [("D5", 0.25)]
    add2 = add1 + [("C5", 0.25)]
    mar = stream.Part(); mar.insert(0, _inst(instrument.Marimba))
    mar.insert(0, tempo.MetronomeMark(number=120)); mar.insert(0, meter.TimeSignature("4/4"))
    for phase in (cell, add1, add2):
        beats = 0.0
        while beats < 32.0:                      # 8 bars per phase
            for p, d in phase:
                mar.append(note.Note(p, quarterLength=d)); beats += d
    pno = stream.Part(); pno.insert(0, _inst(instrument.Piano))
    pno.append(note.Rest(quarterLength=0.5))     # quaver offset: interlocking shimmer
    for phase in (cell, add1, add2):
        beats = 0.0
        while beats < 32.0:
            for p, d in phase:
                pno.append(note.Note(p, quarterLength=d).transpose(-24)); beats += d
    s.insert(0, mar); s.insert(0, pno)
    for n in s.recurse().notes:
        n.volume.velocity = rng.randint(68, 92)
    return s


def build_dissonant():
    # v3: v1 read as cartoon (fast triplets+timpani), v2 as industrial drone
    # (GM strings' slow attack = organ pad; flute leaps = siren). v3 removes
    # every sustained sound: xylophone + violin + low trombone fragments,
    # SHORT marcato string clusters, hammered low piano clusters. Nothing
    # rings longer than a crotchet - stab-world, not drone-world.
    s = stream.Score()
    rng = random.Random(9)
    frag = [("C5", "F#5", "D6"), ("B3", "C5", "E6"), ("F5", "B3", "C#6")]  # wide compound leaps
    xy = stream.Part(); xy.insert(0, _inst(instrument.Xylophone))
    xy.insert(0, tempo.MetronomeMark(number=88)); xy.insert(0, meter.TimeSignature("4/4"))
    vn = stream.Part(); vn.insert(0, _inst(instrument.Violin))
    tb = stream.Part(); tb.insert(0, _inst(instrument.Trombone))
    st = stream.Part(); st.insert(0, _inst(instrument.StringInstrument, 48))
    pn = stream.Part(); pn.insert(0, _inst(instrument.Piano))
    parts = [xy, vn, tb]
    t = 0.0
    total = 56.0
    while t < total:
        p = parts[int(t / 4) % 3]
        f = frag[rng.randrange(3)]
        for other in parts:
            if other is not p:
                other.append(note.Rest(quarterLength=4.0))
        used = 0.0
        for pitch in f:
            base = pitch if p is not tb else note.Note(pitch).transpose(-24).nameWithOctave
            n = note.Note(base, quarterLength=rng.choice([0.5, 0.75, 0.25]))
            n.volume.velocity = 48 if rng.random() < 0.5 else 120   # pp vs ff extremes
            p.append(n)
            used += n.quarterLength
            gap = rng.choice([0.25, 0.5, 0.75])                     # jagged silences inside lines
            p.append(note.Rest(quarterLength=gap))
            used += gap
        if used < 4.0:
            p.append(note.Rest(quarterLength=4.0 - used))
        # irregular SHORT cluster stabs: hammered low piano + marcato strings
        gap = rng.choice([0.75, 1.25, 2.25])
        for part, pitches, dur in ((pn, ["C2", "C#2", "D2", "D#2", "E2"], 0.5),
                                   (st, ["C3", "C#3", "D3", "D#3"], 0.25)):
            part.append(note.Rest(quarterLength=gap))
            cl = chord.Chord(pitches, quarterLength=dur)
            cl.volume.velocity = 122
            part.append(cl)
            rest = 4.0 - gap - dur
            if rest > 0:
                part.append(note.Rest(quarterLength=rest))
        t += 4.0
    for part in (xy, vn, tb, st, pn):
        s.insert(0, part)
    return s


QUESTIONS = {
    "aos3_african_fusion": [
        ("How do the guitar parts relate to each other?",
         ["They play interlocking repeated patterns", "One strums chords while the other is silent",
          "They play the same melody in unison throughout", "They trade long improvised solos"], 0),
        ("Which best describes the bass part?",
         ["A prominent melodic line", "A single repeated note throughout",
          "There is no bass", "Long sustained drones only"], 0),
    ],
    "aos4_minimalism": [
        ("How does the music develop?",
         ["Short repeated patterns gradually change and gain notes", "Contrasting sections alternate abruptly",
          "One long melody never repeats", "It develops through loud drum fills"], 0),
        ("Which best describes the pulse?",
         ["Steady and constant throughout", "Constantly speeding up and slowing down",
          "Free with no sense of beat", "Interrupted by silences"], 0),
        ("Which instruments are most prominent?",
         ["Tuned percussion and piano", "Distorted electric guitars",
          "A church organ", "A solo cello"], 0),
    ],
    "aos4_dissonant_modern": [
        ("Which best describes the melodic writing?",
         ["Angular fragments with wide leaps passed between instruments", "One long smooth romantic melody",
          "A repeated singable folk tune", "No melodic material at all"], 0),
        ("Which best describes the harmony?",
         ["Harsh dissonant clusters", "Simple major-key chords",
          "A single drone throughout", "Sweet romantic harmony"], 0),
        ("Which best describes the dynamics?",
         ["Extreme sudden contrasts", "Quiet and unchanging throughout",
          "One long single crescendo", "Loud and unchanging throughout"], 0),
    ],
}


def main():
    os.makedirs(OUT, exist_ok=True)
    builders = {"aos3_african_fusion": build_fusion, "aos4_minimalism": build_minimalism,
                "aos4_dissonant_modern": build_dissonant}
    if len(sys.argv) > 1:      # optional: only rebuild the named excerpts
        builders = {k: v for k, v in builders.items() if k in sys.argv[1:]}
    rng = random.Random(41)
    results = {}
    for name, build in builders.items():
        print("\n=== %s (constructed) ===" % name)
        gx.render(build(), OUT, name)
        path = os.path.join(OUT, name + ".mp3")
        print("  rendered %d KB" % (os.path.getsize(path) // 1024))
        b64 = base64.b64encode(open(path, "rb").read()).decode()
        desc = wv.gem({"contents": [{"parts": [
            {"inline_data": {"mime_type": "audio/mp3", "data": b64}},
            {"text": "Describe this music: style it evokes, instruments, and three notable "
                     "features. Three sentences maximum."}]}]})
        print("  DESC:", " ".join(desc.split())[:200])
        time.sleep(3)
        qres = []
        for question, options, truth_i in QUESTIONS[name]:
            truth = options[truth_i]
            votes = []
            for _ in range(3):
                topts = list(options)
                rng.shuffle(topts)
                letter, why = wv.ask(b64, question, topts)
                gi = (ord(letter) - 65) if len(letter) == 1 else -1
                votes.append(topts[gi] if 0 <= gi < len(topts) else "?")
                time.sleep(3)
            n = votes.count(truth)
            status = "verified" if n >= 2 else "flagged"
            qres.append({"q": question, "truth": truth, "votes": votes, "status": status})
            print("  %-8s %s" % (status.upper(), question[:60]))
        results[name] = {"description": " ".join(desc.split()), "questions": qres}
    io.open(os.path.join(OUT, "_batch1c_results.json"), "w", encoding="utf-8").write(
        json.dumps(results, ensure_ascii=False, indent=1))
    ver = sum(1 for r in results.values() for q in r["questions"] if q["status"] == "verified")
    total = sum(len(r["questions"]) for r in results.values())
    print("\n==== CONSTRUCTED: %d/%d questions verified ====" % (ver, total))


if __name__ == "__main__":
    main()
