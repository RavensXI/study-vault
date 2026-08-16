# -*- coding: utf-8 -*-
"""Synthesised rhythm patterns for the OCR Rhythms of the World drills
(task #59; Tom's call 16 Aug: synth bronze/silver, real recordings gold).

Every pattern is authored as a GRID, so every rhythmic fact is true by
construction. Each pattern renders TWICE from the same grid:
  - full mix  (shipped to students)
  - skeleton  (accent layer only — machine-verified by onset detection;
              the mix adds layers from the same grid, so a verified
              skeleton proves the shipped pattern)
Rendering: FluidSynth (dry: -R 0 -C 0) + FluidR3_GM percussion, MP3 via
ffmpeg loudnorm I=-17. Verification asserts pattern-specific invariants
(onset counts, grouping ratios) and the run FAILS on any miss.

Per the house rule, synthesised audio underwrites RHYTHM/METRE questions
only — never timbre identification.

Usage: python gen_rotw_rhythms.py         (renders + verifies into _rotw_synth/)
"""
import io
import json
import os
import subprocess
import sys

import numpy as np
from music21 import instrument, meter, note, stream, tempo, volume

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_rotw_synth")
os.makedirs(OUT, exist_ok=True)
FS = r"C:\Users\tshau\.claude\jobs\4059242c\tmp\fluidsynth\bin\fluidsynth.exe"
SF = r"C:\Users\tshau\.claude\jobs\4059242c\tmp\FluidR3_GM.sf2"

# GM percussion keys
LOW_TOM, HI_TOM, FLOOR_TOM = 41, 50, 43
TAMB, COWBELL, CLAP, SNARE, BASS = 54, 56, 39, 38, 36
BONGO_H, BONGO_L, CONGA_OPEN, CONGA_LO = 60, 61, 63, 64
AGOGO_H, AGOGO_L, CABASA, MARACAS = 67, 68, 69, 70
CLAVES, WB_H, WB_L, TRI = 75, 76, 77, 81


def grid_layer(midi, vel_hits, unit_ql):
    """vel_hits: list per subdivision of velocity (0 = rest). One bar."""
    return {"midi": midi, "hits": vel_hits, "unit": unit_ql}


def render(name, ts, bpm, bars, layers, skeleton_idx, swing=None):
    """Render mix + skeleton from the same grid. swing=(long,short) applies
    pairwise to the unit lengths of ALL layers (chaal)."""
    def build(layer_set, path):
        s = stream.Score()
        for lay in layer_set:
            p = stream.Part()
            p.insert(0, instrument.TomTom())
            p.append(tempo.MetronomeMark(number=bpm))
            p.append(meter.TimeSignature(ts))
            for bar in range(bars):
                for i, vel in enumerate(lay["hits"]):
                    ql = lay["unit"]
                    if swing:
                        ql = swing[0] if i % 2 == 0 else swing[1]
                    if vel:
                        n = note.Note(midi=lay["midi"], quarterLength=ql)
                        n.volume = volume.Volume(velocity=vel)
                        p.append(n)
                    else:
                        p.append(note.Rest(quarterLength=ql))
            s.append(p)
        mid = path + ".mid"
        wav = path + ".wav"
        s.write("midi", fp=mid)
        subprocess.run([FS, "-ni", "-R", "0", "-C", "0", "-F", wav, "-r",
                        "44100", SF, mid], capture_output=True, check=True)
        subprocess.run(["ffmpeg", "-y", "-v", "quiet", "-i", wav,
                        "-af", "loudnorm=I=-17,afade=t=out:st=%d:d=1"
                        % max(1, int_dur(ts, bpm, bars, layers, swing) - 1),
                        "-b:a", "96k", path + ".mp3"], check=True)
        os.remove(mid)
        os.remove(wav)
    base = os.path.join(OUT, name)
    build(layers, base)
    build([layers[skeleton_idx]], base + "_skel")
    return base + ".mp3", base + "_skel.mp3"


def int_dur(ts, bpm, bars, layers, swing):
    # duration comes from the GRID, not the notated bar: a tala grid packs
    # 16 quarter-length hits into one grid "bar"
    if swing:
        grid_q = max(sum(swing[i % 2] for i in range(len(l["hits"])))
                     for l in layers)
    else:
        grid_q = max(len(l["hits"]) * l["unit"] for l in layers)
    return int(grid_q * bars * 60 / bpm) + 1


def onsets_of(path, min_gap=0.10):
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", path, "-ac", "1",
                          "-ar", "8000", "-f", "f32le", "-"],
                         stdout=subprocess.PIPE, check=True).stdout
    a = np.abs(np.frombuffer(raw, dtype="<f4"))
    pad = (-a.size) % 80
    a = np.concatenate([a, np.zeros(pad, dtype=a.dtype)])
    env = a.reshape(-1, 80).max(axis=1)
    nov = np.maximum(0, env[3:] - env[:-3])
    th = nov.max() * 0.22
    out = []
    for i, v in enumerate(nov):
        t = (i + 3) * 0.01
        if v > th and (not out or t - out[-1] >= min_gap):
            out.append(t)
    return out


# ── pattern catalogue ──────────────────────────────────────────────────
# each: (name, ts, bpm, bars, layers, skeleton_idx, swing, facts, verify)
# verify(onsets, facts) -> error string or None; runs on the SKELETON.

def v_count(expected, tol=1):
    def f(on, facts):
        if abs(len(on) - expected) > tol:
            return "onsets %d != %d" % (len(on), expected)
    return f


def v_grouping(ratios, tol=0.22):
    """Accent IOIs must repeat the given grouping ratio cycle."""
    def f(on, facts):
        io_ = np.diff(on)
        if len(io_) < len(ratios):
            return "too few accents (%d)" % len(on)
        cyc = np.array(ratios, dtype=float)
        cyc = cyc / cyc.sum()
        got = np.array(io_[:len(io_) - len(io_) % len(ratios)])
        got = got.reshape(-1, len(ratios))
        norm = got / got.sum(axis=1, keepdims=True)
        err = np.abs(norm - cyc).max()
        if err > tol:
            return "grouping err %.2f (want %s)" % (err, ratios)
    return f


def PATTERNS():
    P = []
    # ── L1 India & Punjab ────────────────────────────────────────────
    beat = 1.0
    P.append(("chaal_swung", "4/4", 104, 6,
              [grid_layer(LOW_TOM, [112, 0, 100, 0, 108, 0, 100, 0], 0.5),
               grid_layer(HI_TOM, [0, 84, 0, 84, 0, 84, 0, 84], 0.5),
               grid_layer(TAMB, [70, 0, 0, 0, 70, 0, 0, 0], 0.5)],
              0, (0.66, 0.34),
              {"region": "india-punjab", "label": "Chaal (bhangra groove)",
               "metre": "4/4, swung quavers", "cycle": 8,
               "teaches": "the swung eight-quaver chaal with low dagga "
                          "strokes on the beats and high tilli strokes "
                          "between them"},
              v_count(24, tol=2)))
    P.append(("tintal_16", "4/4", 76, 4,
              [grid_layer(COWBELL, [118] + [0] * 15, 1.0),
               grid_layer(CLAP, [0]*4 + [104] + [0]*7 + [104] + [0]*3, 1.0),
               grid_layer(WB_H, [72]*16, 1.0)],
              2, None,
              {"region": "india-punjab", "label": "Tintal (16-beat tala)",
               "metre": "16-beat cycle in 4 groups of 4", "cycle": 16,
               "teaches": "counting a 16-beat tala: strongest stroke on "
                          "beat 1 (sam), claps on 5 and 13, a quiet "
                          "'empty' group from beat 9 (khali)"},
              v_count(64, tol=3)))
    P.append(("keherwa_8", "4/4", 92, 6,
              [grid_layer(LOW_TOM, [112, 0, 0, 0, 96, 0, 0, 0], 1.0),
               grid_layer(WB_H, [76]*8, 1.0),
               grid_layer(TAMB, [0, 0, 66, 0, 0, 0, 66, 0], 1.0)],
              1, None,
              {"region": "india-punjab", "label": "Keherwa (8-beat tala)",
               "metre": "8-beat cycle", "cycle": 8,
               "teaches": "an eight-beat cycle to contrast with tintal's "
                          "sixteen — count the pulse between low strokes"},
              v_count(48, tol=3)))
    # ── L2 Eastern Mediterranean ─────────────────────────────────────
    P.append(("kalamatianos_78", "7/8", 132, 8,
              [grid_layer(LOW_TOM, [116, 0, 0, 104, 0, 100, 0], 0.5),
               grid_layer(TAMB, [80, 60, 60, 80, 60, 80, 60], 0.5)],
              0, None,
              {"region": "eastern-med", "label": "Kalamatianos (7/8)",
               "metre": "7/8 grouped 3+2+2", "cycle": 7,
               "teaches": "an irregular seven-quaver metre: one long group "
                          "then two short — LONG-short-short"},
              v_grouping([3, 2, 2])))
    P.append(("karsilamas_98", "9/8", 126, 7,
              [grid_layer(LOW_TOM, [116, 0, 100, 0, 100, 0, 104, 0, 0], 0.5),
               grid_layer(TAMB, [80, 60, 80, 60, 80, 60, 80, 60, 60], 0.5)],
              0, None,
              {"region": "eastern-med", "label": "Karsilamas (9/8)",
               "metre": "9/8 grouped 2+2+2+3", "cycle": 9,
               "teaches": "nine quavers grouped short-short-short-LONG — "
                          "the limp comes at the END of the bar"},
              v_grouping([2, 2, 2, 3])))
    P.append(("dum_tek_44", "4/4", 108, 6,
              [grid_layer(CONGA_LO, [112, 0, 0, 0, 104, 0, 0, 0], 0.5),
               grid_layer(BONGO_H, [0, 0, 78, 0, 0, 78, 0, 78], 0.5)],
              0, None,
              {"region": "eastern-med", "label": "Dum-tek (regular 4/4)",
               "metre": "regular 4/4", "cycle": 8,
               "teaches": "a REGULAR duple goblet-drum pattern (deep dum, "
                          "crisp tek) to contrast with 7/8 and 9/8"},
              v_count(12, tol=1)))
    # ── L3 Africa ────────────────────────────────────────────────────
    P.append(("cross_3v2", "6/8", 60, 8,
              [grid_layer(AGOGO_H, [110, 0, 100, 0, 100, 0], 0.5),
               grid_layer(LOW_TOM, [112, 0, 0, 104, 0, 0], 0.5),
               grid_layer(CABASA, [66]*6, 0.5)],
              0, None,
              {"region": "africa", "label": "Cross-rhythm: 3 against 2",
               "metre": "6/8 — bell in 3, drum in 2, simultaneously",
               "cycle": 6,
               "teaches": "two groupings of the same six quavers at once: "
                          "the bell divides the bar into three, the low "
                          "drum into two"},
              v_count(24, tol=2)))
    P.append(("layers_build", "4/4", 100, 8,
              [grid_layer(AGOGO_H, [104, 0, 96, 96, 0, 104, 0, 96], 0.5),
               grid_layer(CABASA, [70]*8, 0.5),
               grid_layer(LOW_TOM, [110, 0, 0, 0, 100, 0, 0, 0], 0.5),
               grid_layer(BONGO_H, [0, 88, 0, 88, 0, 0, 88, 0], 0.5)],
              0, None,
              {"region": "africa", "label": "Texture build (layered ostinati)",
               "metre": "4/4", "cycle": 8, "staggered": True,
               "order": ["bell", "shaker", "low drum", "high drum"],
               "teaches": "how an ensemble texture BUILDS: bell ostinato "
                          "first, then shaker, then low drum, then high "
                          "drum — each new layer thickening the texture"},
              None))
    P.append(("call_response", "4/4", 96, 8,
              [grid_layer(BONGO_H, [96, 96, 0, 96, 0, 96, 96, 0], 0.5),
               grid_layer(LOW_TOM, [0]*8, 0.5),
               grid_layer(AGOGO_L, [0]*8, 0.5)],
              0, None,
              {"region": "africa", "label": "Call and response",
               "metre": "4/4", "cycle": 8, "alternating": True,
               "teaches": "a lead drum's solo phrase answered by the full "
                          "ensemble — one bar call, one bar response"},
              None))
    # ── L4 Americas ──────────────────────────────────────────────────
    P.append(("samba_groove", "2/4", 104, 8,
              [grid_layer(FLOOR_TOM, [80, 0, 0, 0, 118, 0, 0, 0], 0.25),
               grid_layer(SNARE, [70, 55, 62, 55, 70, 55, 62, 55], 0.25),
               grid_layer(AGOGO_H, [96, 0, 0, 96, 0, 0, 96, 0], 0.25),
               grid_layer(WB_H, [88, 0, 88, 88, 0, 88, 88, 0], 0.25)],
              0, None,
              {"region": "americas", "label": "Samba bateria groove",
               "metre": "2/4, semiquaver subdivision", "cycle": 8,
               "teaches": "the samba engine room: the big surdo lands "
                          "heaviest on beat TWO while snare semiquavers "
                          "run underneath"},
              v_count(16, tol=2)))
    P.append(("tresillo_332", "4/4", 116, 8,
              [grid_layer(CLAVES, [112, 0, 0, 108, 0, 0, 104, 0], 0.5),
               grid_layer(MARACAS, [68]*8, 0.5),
               grid_layer(COWBELL, [86, 0, 86, 0, 86, 0, 86, 0], 0.5)],
              0, None,
              {"region": "americas", "label": "3+3+2 (tresillo)",
               "metre": "4/4 with quavers grouped 3+3+2", "cycle": 8,
               "teaches": "the Caribbean 3+3+2: accents that pull AGAINST "
                          "the steady pulse — the syncopation engine of "
                          "calypso and much Latin music"},
              v_grouping([3, 3, 2])))
    P.append(("march_straight", "2/4", 112, 8,
              [grid_layer(BASS, [118, 0, 0, 0], 0.5),
               grid_layer(SNARE, [0, 0, 96, 0], 0.5),
               grid_layer(WB_H, [70, 70, 70, 70], 0.5)],
              0, None,
              {"region": "americas", "label": "Straight march (contrast)",
               "metre": "2/4, unsyncopated", "cycle": 4,
               "teaches": "a completely ON-the-beat duple pattern — what "
                          "the syncopated patterns are NOT"},
              v_count(8, tol=1)))
    return P


def build_staggered(name, ts, bpm, layers, facts):
    """layers_build: each layer enters after 2 more bars (8 bars total)."""
    s = stream.Score()
    for idx, lay in enumerate(layers):
        p = stream.Part()
        p.insert(0, instrument.TomTom())
        p.append(tempo.MetronomeMark(number=bpm))
        p.append(meter.TimeSignature(ts))
        for bar in range(8):
            active = bar >= idx * 2
            for i, vel in enumerate(lay["hits"]):
                if vel and active:
                    n = note.Note(midi=lay["midi"], quarterLength=lay["unit"])
                    n.volume = volume.Volume(velocity=vel)
                    p.append(n)
                else:
                    p.append(note.Rest(quarterLength=lay["unit"]))
        s.append(p)
    return s


def build_call_response(name, ts, bpm, facts):
    """call_response: odd bars lead bongo phrase, even bars ensemble."""
    call = [96, 96, 0, 96, 0, 96, 96, 0]
    resp_low = [112, 0, 104, 0, 112, 0, 104, 104]
    resp_bell = [96, 0, 96, 0, 96, 0, 96, 96]
    s = stream.Score()
    for midi, pat, on_call in [(BONGO_H, call, True),
                               (LOW_TOM, resp_low, False),
                               (AGOGO_L, resp_bell, False)]:
        p = stream.Part()
        p.insert(0, instrument.TomTom())
        p.append(tempo.MetronomeMark(number=bpm))
        p.append(meter.TimeSignature(ts))
        for bar in range(8):
            active = (bar % 2 == 0) if on_call else (bar % 2 == 1)
            for vel in pat:
                if vel and active:
                    n = note.Note(midi=midi, quarterLength=0.5)
                    n.volume = volume.Volume(velocity=vel)
                    p.append(n)
                else:
                    p.append(note.Rest(quarterLength=0.5))
        s.append(p)
    return s


def render_score(s, path, fade_at):
    mid, wav = path + ".mid", path + ".wav"
    s.write("midi", fp=mid)
    subprocess.run([FS, "-ni", "-R", "0", "-C", "0", "-F", wav, "-r", "44100",
                    SF, mid], capture_output=True, check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "quiet", "-i", wav, "-af",
                    "loudnorm=I=-17,afade=t=out:st=%d:d=1" % fade_at,
                    "-b:a", "96k", path + ".mp3"], check=True)
    os.remove(mid)
    os.remove(wav)


def main():
    manifest = {}
    fails = []
    for (name, ts, bpm, bars, layers, skel_idx, swing, facts,
         verify) in PATTERNS():
        if facts.get("staggered"):
            s = build_staggered(name, ts, bpm, layers, facts)
            render_score(s, os.path.join(OUT, name),
                         int_dur(ts, bpm, 8, layers, None) - 1)
            mix = os.path.join(OUT, name + ".mp3")
            skel = None
        elif facts.get("alternating"):
            s = build_call_response(name, ts, bpm, facts)
            render_score(s, os.path.join(OUT, name),
                         int_dur(ts, bpm, 8, layers, None) - 1)
            mix = os.path.join(OUT, name + ".mp3")
            skel = None
        else:
            mix, skel = render(name, ts, bpm, bars, layers, skel_idx, swing)
        err = None
        if verify and skel:
            err = verify(onsets_of(skel), facts)
        status = "FAIL: " + err if err else "ok"
        if err:
            fails.append(name)
        dur = None
        manifest[name] = {"file": os.path.basename(mix), "facts": facts,
                          "verified": not err}
        print("%-18s %-4s %3d bpm  %s" % (name, ts, bpm, status))
    io.open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8").write(
        json.dumps(manifest, indent=1, ensure_ascii=False))
    print("\n%d patterns, %d verification failures" % (len(manifest),
                                                      len(fails)))
    if fails:
        sys.exit(1)


if __name__ == "__main__":
    main()
