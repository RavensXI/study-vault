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
    s = stream.Score()
    # guitar 1: 3-quarter-beat ostinato (E-G-A), guitar 2: 4-beat ostinato -
    # patterns realign every 12 beats: polymetric interlock by construction.
    g1 = stream.Part(); g1.insert(0, _inst(instrument.ElectricGuitar, 27))
    g1.insert(0, tempo.MetronomeMark(number=116)); g1.insert(0, meter.TimeSignature("4/4"))
    for _ in range(20):
        for p, d in [("E4", 0.5), ("G4", 0.5), ("A4", 0.5), ("E4", 0.5), ("G4", 0.5), ("A4", 0.5)]:
            g1.append(note.Note(p, quarterLength=d))
    g2 = stream.Part(); g2.insert(0, _inst(instrument.ElectricGuitar, 27))
    for _ in range(15):
        for p, d in [("C5", 0.5), ("B4", 0.5), ("A4", 0.5), ("C5", 0.5),
                     ("D5", 0.75), ("C5", 0.75), ("A4", 0.5)]:
            g2.append(note.Note(p, quarterLength=d))
    mar = stream.Part(); mar.insert(0, _inst(instrument.Marimba))
    for _ in range(30):
        for p, d in [("A2", 0.25), ("E3", 0.25), ("A3", 0.25), ("E3", 0.25),
                     ("G2", 0.25), ("D3", 0.25), ("G3", 0.25), ("D3", 0.25)]:
            mar.append(note.Note(p, quarterLength=d))
    bass = stream.Part(); bass.insert(0, _inst(instrument.ElectricBass))
    for _ in range(10):
        for p, d in [("A1", 1.0), ("C2", 0.5), ("E2", 0.5), ("G1", 1.0), ("A1", 0.5), ("C2", 0.5),
                     ("A1", 1.0), ("E2", 1.0), ("G1", 1.0), ("A1", 1.0)]:
            bass.append(note.Note(p, quarterLength=d))
    for p in (g1, g2, mar, bass):
        s.insert(0, p)
    for n in s.recurse().notes:
        n.volume.velocity = 96
    return s


def build_minimalism():
    s = stream.Score()
    cell = [("E4", 0.25), ("G4", 0.25), ("B4", 0.25), ("A4", 0.25)]
    add1 = cell + [("D5", 0.25)]
    add2 = add1 + [("C5", 0.25)]
    mar = stream.Part(); mar.insert(0, _inst(instrument.Marimba))
    mar.insert(0, tempo.MetronomeMark(number=138)); mar.insert(0, meter.TimeSignature("4/4"))
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
                pno.append(note.Note(p, quarterLength=d).transpose(-12)); beats += d
    s.insert(0, mar); s.insert(0, pno)
    for n in s.recurse().notes:
        n.volume.velocity = 84
    return s


def build_dissonant():
    s = stream.Score()
    rng = random.Random(9)
    frag = [("C5", "F#5", "D5"), ("B4", "C6", "E5"), ("F5", "B5", "C#5")]  # tritone/7th/9th leaps
    fl = stream.Part(); fl.insert(0, _inst(instrument.Flute))
    fl.insert(0, tempo.MetronomeMark(number=96)); fl.insert(0, meter.TimeSignature("4/4"))
    vn = stream.Part(); vn.insert(0, _inst(instrument.Violin))
    tb = stream.Part(); tb.insert(0, _inst(instrument.Trombone))
    st = stream.Part(); st.insert(0, _inst(instrument.StringInstrument, 48))
    tp = stream.Part(); tp.insert(0, _inst(instrument.Timpani))
    parts = [fl, vn, tb]
    t = 0.0
    total = 64.0
    while t < total:
        p = parts[int(t / 4) % 3]
        f = frag[rng.randrange(3)]
        for other in parts:
            if other is not p:
                other.append(note.Rest(quarterLength=2.0))
        for pitch in f:
            n = note.Note(pitch, quarterLength=2.0 / 3)
            n.volume.velocity = 52 if rng.random() < 0.6 else 116   # pp vs ff extremes
            p.append(n)
        # irregular cluster stabs: strings+timpani semitone clusters
        gap = rng.choice([0.5, 1.0, 1.5])
        st.append(note.Rest(quarterLength=gap))
        cl = chord.Chord(["C4", "C#4", "D4", "D#4", "E4"], quarterLength=0.5)
        cl.volume.velocity = 120
        st.append(cl)
        st.append(note.Rest(quarterLength=2.0 - gap - 0.5 if gap + 0.5 < 2.0 else 0.001))
        tp.append(note.Rest(quarterLength=gap))
        hit = note.Note("C2", quarterLength=0.5); hit.volume.velocity = 118
        tp.append(hit)
        tp.append(note.Rest(quarterLength=2.0 - gap - 0.5 if gap + 0.5 < 2.0 else 0.001))
        t += 2.0
    for part in (fl, vn, tb, st, tp):
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
