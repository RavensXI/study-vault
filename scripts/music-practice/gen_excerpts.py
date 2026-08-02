# -*- coding: utf-8 -*-
"""Excerpt generator library for GCSE Music listening drills.

Every excerpt is authored as notation, so every musical fact is true by
construction. Renders via portable FluidSynth + FluidR3_GM, MP3 via ffmpeg.
Outputs excerpts + a facts JSON that downstream question generation and the
Gemini machine-ear verification both consume.

House rules (learned on the 2 Aug prototype):
- No solo-keyboard timbre-identification questions (FluidR3 piano reads as
  harpsichord); keyboard may appear only as accompaniment.
- Cadence excerpts end with maximally unambiguous final bars: plain triads,
  root position, melody on the defining note, clear pause.

Usage: python scripts/music-practice/gen_excerpts.py <out_dir>
"""
import io
import json
import os
import random
import subprocess
import sys

from music21 import chord, instrument, key, meter, note, stream, tempo

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FS = r"C:\Users\tshau\.claude\jobs\4059242c\tmp\fluidsynth\bin\fluidsynth.exe"
SF = r"C:\Users\tshau\.claude\jobs\4059242c\tmp\FluidR3_GM.sf2"

MELODIC = {  # name -> (music21 instrument, family) — no solo keyboards
    "flute": (instrument.Flute, "woodwind"),
    "oboe": (instrument.Oboe, "woodwind"),
    "clarinet": (instrument.Clarinet, "woodwind"),
    "violin": (instrument.Violin, "strings"),
    "cello": (instrument.Violoncello, "strings"),
    "trumpet": (instrument.Trumpet, "brass"),
    "horn": (instrument.Horn, "brass"),
}

MAJORS = ["C", "D", "F", "G", "A", "B-", "E-"]
MINORS = ["a", "d", "e", "g", "c", "b"]


def _scale_notes(k, octave=4, degrees=8):
    sc = key.Key(k).getScale()
    return [sc.pitchFromDegree(d % 7 + 1).transpose(12 * ((d // 7))) for d in range(degrees)]


def _mk_parts(k, ts, bpm, inst_cls):
    p = stream.Part()
    p.insert(0, inst_cls())
    p.append(key.Key(k))
    p.append(meter.TimeSignature(ts))
    p.insert(0, tempo.MetronomeMark(number=bpm))
    return p


def _accomp_part(k, ts):
    p = stream.Part()
    p.insert(0, instrument.StringInstrument())
    p.append(key.Key(k))
    p.append(meter.TimeSignature(ts))
    return p


def _stepwise_melody(k, rng, beats_per_bar, bars, ql=1.0):
    """A singable stepwise line with small leaps, ending on the tonic."""
    kk = key.Key(k)
    sc = kk.getScale()
    deg = 1 + rng.randint(0, 2) * 2  # start on 1, 3 or 5
    out = []
    total = int(beats_per_bar * bars / ql) - 2
    for _ in range(total):
        out.append(note.Note(sc.pitchFromDegree((deg - 1) % 7 + 1).transpose(12), quarterLength=ql))
        deg += rng.choice([-2, -1, -1, 1, 1, 1, 2])
        deg = max(1, min(9, deg))
    out.append(note.Note(sc.pitchFromDegree(2).transpose(12), quarterLength=ql))
    out.append(note.Note(kk.tonic.transpose(12), quarterLength=beats_per_bar - ((len(out)) * ql) % beats_per_bar or ql))
    return out


def _triad(k, degree, octave=3, ql=1.0, seventh=False):
    kk = key.Key(k)
    sc = kk.getScale()
    root = sc.pitchFromDegree(degree)
    third = sc.pitchFromDegree((degree + 1) % 7 + 1)
    fifth = sc.pitchFromDegree((degree + 3) % 7 + 1)
    ps = [root, third, fifth]
    if degree == 5 and kk.mode == "minor":  # raise leading note in V of minor
        ps[1] = ps[1].transpose(1)
    c = chord.Chord(ps, quarterLength=ql)
    c = c.transpose(12 * (octave - 3))
    return c


# ── generators ──────────────────────────────────────────────────────────────

def gen_metre(kind, seed):
    rng = random.Random(seed)
    inst_name = rng.choice(["flute", "violin", "trumpet"])
    inst_cls, family = MELODIC[inst_name]
    k = rng.choice(MAJORS)
    conf = {
        "simple duple (2/4)": ("2/4", 2, 108),
        "simple triple (3/4)": ("3/4", 3, 100),
        "simple quadruple (4/4)": ("4/4", 4, 112),
        "compound duple (6/8)": ("6/8", 3.0, 63),
    }[kind]
    ts, bpb, bpm = conf
    s = stream.Score()
    mel = _mk_parts(k, ts, bpm, inst_cls)
    acc = _accomp_part(k, ts)
    if ts == "6/8":
        for bar in range(6):
            for d in ([1, 2, 3, 5, 4, 3] if bar % 2 == 0 else [3, 4, 5, 6, 5, 4]):
                mel.append(note.Note(key.Key(k).getScale().pitchFromDegree((d - 1) % 7 + 1).transpose(12), quarterLength=0.5))
        for bar in range(6):
            acc.append(_triad(k, [1, 4, 5, 1, 5, 1][bar], ql=1.5))
            acc.append(_triad(k, [1, 4, 5, 1, 5, 1][bar], ql=1.5))
    else:
        # melody: long accented downbeat note then movement — metre-defining
        sc = key.Key(k).getScale()
        degs = [1, 3, 5, 3, 4, 2]
        for bar in range(6):
            d0 = degs[bar]
            if int(bpb) == 2:
                mel.append(note.Note(sc.pitchFromDegree(d0).transpose(12), quarterLength=1.5))
                mel.append(note.Note(sc.pitchFromDegree(d0 % 7 + 1).transpose(12), quarterLength=0.5))
            elif int(bpb) == 3:
                mel.append(note.Note(sc.pitchFromDegree(d0).transpose(12), quarterLength=2.0))
                mel.append(note.Note(sc.pitchFromDegree(d0 % 7 + 1).transpose(12), quarterLength=1.0))
            else:
                mel.append(note.Note(sc.pitchFromDegree(d0).transpose(12), quarterLength=1.5))
                mel.append(note.Note(sc.pitchFromDegree(d0 % 7 + 1).transpose(12), quarterLength=0.5))
                mel.append(note.Note(sc.pitchFromDegree((d0 + 1) % 7 + 1).transpose(12), quarterLength=1.0))
                mel.append(note.Note(sc.pitchFromDegree(d0).transpose(12), quarterLength=1.0))
        # percussive oom-pah: accented low root on the downbeat, marimba chords off
        acc.insert(0, instrument.Marimba())
        for bar in range(6):
            deg = [1, 4, 5, 1, 5, 1][bar]
            root = _triad(k, deg, octave=2, ql=1.0)
            dn = note.Note(root.root(), quarterLength=1.0)
            dn.volume.velocity = 110
            acc.append(dn)
            for _ in range(int(bpb) - 1):
                c = _triad(k, deg, octave=4, ql=1.0)
                c.volume.velocity = 70
                acc.append(c)
    s.insert(0, mel)
    s.insert(0, acc)
    return s, {"metre": kind, "tonality": "major", "instrument": inst_name,
               "instrument_family": family, "tempo_bpm": bpm}


def gen_tonality(kind, seed):
    rng = random.Random(seed)
    inst_name = rng.choice(list(MELODIC))
    inst_cls, family = MELODIC[inst_name]
    s = stream.Score()
    if kind in ("major", "minor"):
        k = rng.choice(MAJORS if kind == "major" else MINORS)
        bpm = 112 if kind == "major" else 76
        mel = _mk_parts(k, "4/4", bpm, inst_cls)
        acc = _accomp_part(k, "4/4")
        kk = key.Key(k)
        sc = kk.getScale()
        degs = [1, 3, 5, 6, 5, 4, 3, 2, 1, 7, 1, 3, 2, 7, 1, 1]
        for i, d in enumerate(degs):
            p = sc.pitchFromDegree((d - 1) % 7 + 1).transpose(12)
            if kind == "minor" and d == 7:
                p = p.transpose(1)  # harmonic minor leading note
            mel.append(note.Note(p, quarterLength=1.5 if i % 4 == 0 else (0.5 if i % 4 == 1 else 1.0)))
        for bar in range(6):
            acc.append(_triad(k, [1, 4, 5, 6, 5, 1][bar], ql=4.0))
        s.insert(0, mel); s.insert(0, acc)
        return s, {"tonality": kind, "metre": "simple quadruple (4/4)",
                   "instrument": inst_name, "instrument_family": family, "tempo_bpm": 104}
    if kind == "pentatonic":
        mel = _mk_parts("C", "4/4", 96, inst_cls)
        pent = ["C5", "D5", "E5", "G5", "A5", "G5", "E5", "D5"]
        for bar in range(4):
            for p in (pent if bar % 2 == 0 else list(reversed(pent))):
                mel.append(note.Note(p, quarterLength=0.5))
        s.insert(0, mel)
        return s, {"tonality": "pentatonic", "metre": "simple quadruple (4/4)",
                   "instrument": inst_name, "instrument_family": family, "tempo_bpm": 96}
    if kind == "chromatic":
        mel = _mk_parts("C", "4/4", 80, inst_cls)
        base = 60 + rng.randint(0, 5)
        direction = 1
        for i in range(24):
            mel.append(note.Note(base + (i % 12) * direction, quarterLength=0.5))
        s.insert(0, mel)
        return s, {"tonality": "chromatic", "metre": "simple quadruple (4/4)",
                   "instrument": inst_name, "instrument_family": family, "tempo_bpm": 80}
    raise ValueError(kind)


def gen_cadence(kind, seed):
    rng = random.Random(seed)
    inst_name = rng.choice(list(MELODIC))
    inst_cls, family = MELODIC[inst_name]
    k = rng.choice(MAJORS)
    kk = key.Key(k)
    s = stream.Score()
    mel = _mk_parts(k, "4/4", 92, inst_cls)
    acc = _accomp_part(k, "4/4")
    for n in _stepwise_melody(k, rng, 4, 4):
        mel.append(n)
    final = {"perfect": (5, 1), "imperfect": (4, 5), "plagal": (4, 1), "interrupted": (5, 6)}[kind]
    for bar, deg in enumerate([1, 6, 2, 1]):
        acc.append(_triad(k, deg, ql=4.0))
    # the cadence itself, ISOLATED: silence, then two whole-bar chords, stop
    pen, fin = final
    mel.append(note.Rest(quarterLength=4.0))
    acc.append(note.Rest(quarterLength=4.0))
    acc.append(_triad(k, pen, ql=4.0))
    acc.append(_triad(k, fin, ql=4.0))
    end_deg = {1: 1, 5: 2, 6: 3}[fin]
    pen_deg = {5: 7, 4: 6}[pen]
    mel.append(note.Note(kk.getScale().pitchFromDegree(pen_deg).transpose(12), quarterLength=4.0))
    mel.append(note.Note(kk.getScale().pitchFromDegree(end_deg).transpose(12), quarterLength=4.0))
    s.insert(0, mel); s.insert(0, acc)
    return s, {"cadence": kind, "tonality": "major", "metre": "simple quadruple (4/4)",
               "instrument": inst_name, "instrument_family": family, "tempo_bpm": 92}


def gen_texture(kind, seed):
    rng = random.Random(seed)
    inst_name = rng.choice(list(MELODIC))
    inst_cls, family = MELODIC[inst_name]
    k = rng.choice(MAJORS)
    s = stream.Score()
    if kind == "monophonic":
        mel = _mk_parts(k, "3/4", 88, inst_cls)
        for n in _stepwise_melody(k, rng, 3, 8):
            mel.append(n)
        s.insert(0, mel)
    elif kind == "melody and accompaniment":
        mel = _mk_parts(k, "4/4", 100, inst_cls)
        acc = _accomp_part(k, "4/4")
        for n in _stepwise_melody(k, rng, 4, 6):
            mel.append(n)
        for bar in range(6):
            acc.append(_triad(k, [1, 4, 5, 1, 4, 1][bar], ql=4.0))
        s.insert(0, mel); s.insert(0, acc)
    elif kind == "imitative polyphony":
        line = _stepwise_melody(k, rng, 3, 6, ql=0.5)
        v1 = _mk_parts(k, "3/4", 76, inst_cls)
        name2 = rng.choice([n for n in MELODIC if MELODIC[n][1] == family and n != inst_name] or [inst_name])
        v2 = _mk_parts(k, "3/4", 76, MELODIC[name2][0])
        for n in line:
            v1.append(note.Note(n.pitch, quarterLength=n.quarterLength))
        v2.append(note.Rest(quarterLength=1.5))
        for n in line:
            v2.append(note.Note(n.pitch.transpose(-12), quarterLength=n.quarterLength))
        s.insert(0, v1); s.insert(0, v2)
    elif kind == "unison":
        v1 = _mk_parts(k, "4/4", 108, inst_cls)
        name2 = rng.choice([n for n in MELODIC if n != inst_name])
        v2 = _mk_parts(k, "4/4", 108, MELODIC[name2][0])
        line = _stepwise_melody(k, rng, 4, 5)
        for n in line:
            v1.append(note.Note(n.pitch, quarterLength=n.quarterLength))
            v2.append(note.Note(n.pitch, quarterLength=n.quarterLength))
        s.insert(0, v1); s.insert(0, v2)
    else:
        raise ValueError(kind)
    return s, {"texture": kind, "tonality": "major", "instrument": inst_name,
               "instrument_family": family}


def gen_device(kind, seed):
    rng = random.Random(seed)
    inst_name = rng.choice(list(MELODIC))
    inst_cls, family = MELODIC[inst_name]
    k = rng.choice(MAJORS)
    kk = key.Key(k)
    sc = kk.getScale()
    s = stream.Score()
    mel = _mk_parts(k, "4/4", 96, inst_cls)
    if kind == "sequence":
        for start in (1, 2, 3, 4):
            for d, ql in [(0, 0.5), (1, 0.5), (2, 0.5), (4, 1.0), (2, 0.5), (0, 1.0)]:
                mel.append(note.Note(sc.pitchFromDegree((start + d - 1) % 7 + 1).transpose(12), quarterLength=ql))
        s.insert(0, mel)
    elif kind == "ostinato":
        bass = _accomp_part(k, "4/4")
        patt = [1, 5, 6, 5]
        for _ in range(6):
            for d in patt:
                bass.append(note.Note(sc.pitchFromDegree(d), quarterLength=1.0))
        for n in _stepwise_melody(k, rng, 4, 6):
            mel.append(n)
        s.insert(0, mel); s.insert(0, bass)
    elif kind == "drone":
        drone = _accomp_part(k, "4/4")
        for _ in range(6):
            drone.append(chord.Chord([kk.tonic.transpose(-12), kk.tonic.transpose(-5)], quarterLength=4.0))
        for n in _stepwise_melody(k, rng, 4, 6):
            mel.append(n)
        s.insert(0, mel); s.insert(0, drone)
    else:
        raise ValueError(kind)
    return s, {"device": kind, "tonality": "major", "instrument": inst_name,
               "instrument_family": family}


def gen_pop(kind, seed):
    """AoS2-flavoured: four-chord loop, syncopated bass, optional drum kit."""
    rng = random.Random(seed)
    k = rng.choice(MAJORS)
    s = stream.Score()
    lead_name = rng.choice(["trumpet", "violin", "flute"])
    mel = _mk_parts(k, "4/4", 116, MELODIC[lead_name][0])
    gtr = stream.Part(); gtr.insert(0, instrument.ElectricGuitar())
    gtr.append(key.Key(k)); gtr.append(meter.TimeSignature("4/4"))
    bass = stream.Part(); bass.insert(0, instrument.ElectricBass())
    bass.append(key.Key(k)); bass.append(meter.TimeSignature("4/4"))
    loop = [1, 5, 6, 4]
    for _ in range(2):
        for deg in loop:
            gtr.append(_triad(k, deg, octave=4, ql=2.0))
            gtr.append(_triad(k, deg, octave=4, ql=2.0))
            root = _triad(k, deg, octave=2).root()
            if kind == "syncopated bass":
                bass.append(note.Note(root, quarterLength=0.75))
                bass.append(note.Note(root, quarterLength=0.75))
                bass.append(note.Note(root, quarterLength=1.0))
                bass.append(note.Note(root.transpose(7), quarterLength=0.5))
                bass.append(note.Note(root, quarterLength=1.0))
            else:  # straight
                for _b in range(4):
                    bass.append(note.Note(root, quarterLength=1.0))
    for n in _stepwise_melody(k, rng, 4, 8):
        mel.append(n)
    s.insert(0, mel); s.insert(0, gtr); s.insert(0, bass)
    return s, {"style": "pop", "bass_rhythm": kind, "tonality": "major",
               "chord_loop": "I-V-vi-IV", "instrument": lead_name,
               "instrument_family": MELODIC[lead_name][1]}


def render(score, out_dir, name):
    mid = os.path.join(out_dir, name + ".mid")
    wav = os.path.join(out_dir, name + ".wav")
    mp3 = os.path.join(out_dir, name + ".mp3")
    score.write("midi", fp=mid)
    subprocess.run([FS, "-ni", "-F", wav, "-r", "44100", SF, mid], capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-i", wav, "-codec:a", "libmp3lame", "-b:a", "112k", mp3],
                   capture_output=True)
    for p in (wav, mid):
        try: os.remove(p)
        except OSError: pass
    return os.path.getsize(mp3)


BANK = []
for kind in ["simple duple (2/4)", "simple triple (3/4)", "simple quadruple (4/4)", "compound duple (6/8)"]:
    for i in range(2):
        BANK.append(("metre", kind, gen_metre))
for kind in ["major", "minor", "major", "minor", "pentatonic", "chromatic"]:
    BANK.append(("tonality", kind, gen_tonality))
for kind in ["perfect", "imperfect", "plagal", "interrupted"]:
    for i in range(2):
        BANK.append(("cadence", kind, gen_cadence))
for kind in ["monophonic", "melody and accompaniment", "imitative polyphony", "unison"]:
    for i in range(2):
        BANK.append(("texture", kind, gen_texture))
for kind in ["sequence", "ostinato", "drone"]:
    for i in range(2):
        BANK.append(("device", kind, gen_device))
for kind in ["syncopated bass", "straight bass"]:
    for i in range(2):
        BANK.append(("pop", kind, gen_pop))


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    facts = []
    for idx, (topic, kind, fn) in enumerate(BANK, 1):
        name = "ex%03d_%s" % (idx, topic)
        score, f = fn(kind, seed=1000 + idx)
        size = render(score, out_dir, name)
        f.update({"id": name, "topic": topic, "kind": kind})
        facts.append(f)
        print("%-28s %-24s %4d KB" % (name, kind, size // 1024), flush=True)
    io.open(os.path.join(out_dir, "facts.json"), "w", encoding="utf-8").write(
        json.dumps(facts, ensure_ascii=False, indent=1))
    print("bank complete: %d excerpts" % len(facts))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\tshau\.claude\jobs\4059242c\tmp\music_bank")
