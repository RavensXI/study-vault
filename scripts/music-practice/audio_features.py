# -*- coding: utf-8 -*-
"""Pass 3 — measured features, so a clip is screened before anyone listens.

The other passes ask a model what it hears. This one measures, which is a
genuinely independent opinion: a claim backed by one source has no reviewer, and
that is how wrong answer keys have reached students before.

What it measures, and how far to trust each:

  tempo            reliable
  beat spread      reliable — the ms scatter of onsets around the beat grid.
                   Tight (<120ms) means programmed/quantised, which dates a
                   track to 1980 onwards. Wide means a band that breathes.
  percussive ratio reliable as "is there a real kit here" — librosa's harmonic/
                   percussive separation. Near zero means no drums at all, which
                   is exactly how the synthetic "pop" clips failed.
  low-end energy   reliable as "is there a bass"
  key / major-minor DECENT, NOT AUTHORITATIVE. Krumhansl-Schmuckler correlation
                   on the chroma profile is roughly right on clean tonal
                   material and wrong often enough that it must never be the
                   sole basis for a tonality answer key. Use it to CONTRADICT a
                   claim, not to establish one.

Deliberately NOT attempted: naming instruments. The models that claim to do it
are trained on small tag sets and are not accurate enough to underwrite an exam
answer. Percussive ratio and low-end energy answer the question AoS2 actually
asks — is this a real band or a machine.

    python audio_features.py <file-or-folder>
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np

SR = 22050

# Krumhansl-Kessler profiles
_MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
_MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def analyse(path):
    import librosa
    y, sr = librosa.load(path, sr=SR, mono=True)
    out = {"file": os.path.basename(path), "seconds": round(len(y) / sr, 1)}
    if len(y) < sr * 3:
        out["error"] = "too short to analyse"
        return out

    # tempo + beat grid
    onset = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset, sr=sr)
    out["bpm"] = round(float(np.atleast_1d(tempo)[0]), 1)

    # how tightly do onsets sit on that grid?
    ot = librosa.onset.onset_detect(onset_envelope=onset, sr=sr, units="time")
    bt = librosa.frames_to_time(beats, sr=sr)
    if len(bt) > 2 and len(ot) > 4:
        period = float(np.median(np.diff(bt)))
        off = [((t - bt[0]) % period) / period for t in ot]
        ang = np.angle(np.mean(np.exp(2j * np.pi * np.array(off))))
        dev = ((np.array(off) - ang / (2 * np.pi) + 0.5) % 1.0) - 0.5
        out["beat_spread_ms"] = round(float(np.std(dev) * period * 1000), 1)
        out["feel"] = ("programmed / quantised" if out["beat_spread_ms"] < 120
                       else "played — the beat breathes")

    # real kit? real bass?
    h, p = librosa.effects.hpss(y)
    pe, he = float(np.mean(p ** 2)), float(np.mean(h ** 2))
    out["percussive_ratio"] = round(pe / (pe + he + 1e-12), 3)
    out["has_drums"] = out["percussive_ratio"] > 0.18
    S = np.abs(librosa.stft(y, n_fft=2048))
    f = librosa.fft_frequencies(sr=sr, n_fft=2048)
    low = S[(f >= 30) & (f <= 140)].mean()
    out["low_end_ratio"] = round(float(low / (S.mean() + 1e-12)), 2)
    out["has_bass"] = out["low_end_ratio"] > 1.0

    # key — indicative only
    ch = librosa.feature.chroma_cqt(y=h, sr=sr).mean(axis=1)
    ch = ch / (ch.sum() + 1e-12)
    best = None
    for i in range(12):
        r = np.roll(ch, -i)
        for name, prof in (("major", _MAJ), ("minor", _MIN)):
            c = float(np.corrcoef(r, prof)[0, 1])
            if best is None or c > best[0]:
                best = (c, _NAMES[i], name)
    out["key_guess"] = "%s %s" % (best[1], best[2])
    out["key_confidence"] = round(best[0], 2)
    out["key_note"] = "indicative only — never the sole basis for a tonality key"
    return out


def screen(rows, brief=None):
    """brief: {'feel': 'programmed'|'played', 'drums': True, 'bass': True}"""
    for r in rows:
        flags = []
        if r.get("error"):
            flags.append(r["error"])
        if brief:
            if brief.get("drums") and not r.get("has_drums"):
                flags.append("BRIEF ASKED FOR DRUMS — none detected")
            if brief.get("bass") and not r.get("has_bass"):
                flags.append("BRIEF ASKED FOR BASS — little low end")
            want = brief.get("feel")
            if want and r.get("feel"):
                if want == "programmed" and "breathes" in r["feel"]:
                    flags.append("BRIEF ASKED FOR PROGRAMMED — beat breathes (%sms)"
                                 % r.get("beat_spread_ms"))
                if want == "played" and "quantised" in r["feel"]:
                    flags.append("BRIEF ASKED FOR A LIVE BAND — beat is grid-locked (%sms)"
                                 % r.get("beat_spread_ms"))
        r["flags"] = flags
    return rows


def main(target):
    files = ([target] if os.path.isfile(target)
             else [os.path.join(target, f) for f in sorted(os.listdir(target))
                   if f.lower().endswith((".mp3", ".wav", ".flac", ".m4a"))])
    rows = [analyse(f) for f in files]
    screen(rows)
    for r in rows:
        print("%-30s %6s bpm  spread %-7s  perc %-5s bass %-5s  %-16s %s"
              % (r["file"][:30], r.get("bpm", "-"),
                 str(r.get("beat_spread_ms", "-")) + "ms", r.get("percussive_ratio", "-"),
                 r.get("low_end_ratio", "-"), r.get("key_guess", "-"),
                 "; ".join(r.get("flags") or [])))
    return rows


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
