# -*- coding: utf-8 -*-
"""Batch 2: validate the A/B takes, pick a winner per clip, trim, re-verify.

Order matters and is deliberate:

  0. IDIOM GATE - unprimed free-text probes ("describe this", "list every
     instrument you hear"). No options are ever shown, because a primed probe
     agrees with whatever instrument you put in front of it - that is how
     "fiddle and acoustic guitar" survived batch 1 on a clip Tom heard as
     guitar plus cello. A take that fails the gate cannot win, however well it
     scores on the multiple-choice pass.
  1. 3-vote MCQ ensemble, options shuffled each vote.
  2. DISTRACTOR AUDIT - each wrong option judged TRUE/FALSE of the audio on its
     own; anything even arguably true is flagged and the option gets rewritten.
  3. Trim the winner to a 40s teaching window and RE-VERIFY on the trim, since
     trimming can cut the tested feature out.

Usage: python scripts/music-practice/run_flow_batch2.py
"""
import base64
import glob
import io
import json
import os
import random
import subprocess
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import works_verify as wv

DOWNLOADS = os.path.join(os.environ["USERPROFILE"], "Downloads")
OUT = r"C:\Users\tshau\.claude\jobs\4059242c\tmp\flow_batch2"
WINDOW = 40

DESCRIBE = ("Describe this music: genre/era it evokes, instruments and voices you hear, "
            "and three notable musical features. Three sentences maximum.")
INSTRUMENTS = ("List every instrument or voice you can hear in this recording, most "
               "prominent first. For each, say how confident you are.")

CLIPS = {
    "aos4_minimalism_v3": {
        "takes": {"a": "aos4_minimalism_v3a", "b": "aos4_minimalism_v3b"},
        # batch 1 drifted to new-age ambient; those words in a free description
        # are the drift signature, so they veto the take
        "expect_any": ["marimba", "vibraphone", "tuned percussion", "piano", "clarinet", "xylophone"],
        "reject_any": ["ambient", "new age", "new-age", "meditat", "synth pad", "pad ", "drone"],
        "questions": [
            ("How does the music develop?",
             ["Short repeated patterns gradually change and gain notes",
              "One long melody never repeats",
              "Contrasting sections alternate abruptly",
              "It develops through loud drum fills"], 0),
            ("Which best describes the pulse?",
             ["Steady and constant throughout",
              "Free with no sense of beat",
              "Constantly speeding up and slowing down",
              "Interrupted by silences"], 0),
            ("Which instruments are most prominent?",
             ["Tuned percussion and piano",
              "Distorted electric guitars",
              "A solo cello",
              "A church organ"], 0),
        ],
    },
    "aos4_hungarian_dance_orch": {
        "takes": {"a": "aos4_hungarian_dance_orcha", "b": "aos4_hungarian_dance_orchb"},
        "expect_any": ["clarinet", "cimbalom", "dulcimer", "orchestra", "strings"],
        "reject_any": ["drum kit", "synth", "electric guitar", "vocal"],
        "questions": [
            ("Which instrument states the tune first?",
             ["Clarinet", "Trumpet", "Piano", "Solo violin"], 0),
            ("What happens to the tune during the excerpt?",
             ["The full strings take it over",
              "It is never repeated",
              "A singer takes over",
              "It fades into silence"], 0),
            ("Which best describes the rhythm?",
             ["Accented dance rhythms with sharp short-long snap figures",
              "A slow free rhythm with no pulse",
              "A steady swung jazz shuffle",
              "A waltz that stays gentle throughout"], 0),
        ],
    },
    "aos4_american_orch": {
        "takes": {"a": "aos4_american_orch_a", "b": "aos4_american_orch_b"},
        "expect_any": ["trumpet", "brass", "strings", "orchestra", "woodwind"],
        "reject_any": ["drum kit", "synth", "electric guitar", "vocal"],
        "questions": [
            ("How does the texture begin?",
             ["Bare and widely spaced",
              "Dense and heavily layered",
              "Solo piano alone",
              "Full orchestra at full volume"], 0),
            ("What happens to the main tune?",
             ["It is passed between instrument families and grows louder",
              "It is played once and never returns",
              "It is sung by a choir",
              "It stays in the same instrument throughout"], 0),
            ("Which best describes the dynamics?",
             ["A gradual growth from quiet to loud",
              "Loud and unchanging",
              "Quiet and unchanging",
              "Sudden alternation with no direction"], 0),
        ],
    },
    "aos4_sacred_static": {
        "takes": {"a": "aos4_sacred_static_a", "b": "aos4_sacred_static_b"},
        "expect_any": ["choir", "voices", "vocal", "chant", "a cappella", "unaccompanied"],
        "reject_any": ["drum", "guitar", "orchestra", "piano"],
        "questions": [
            ("What sounds underneath the voices throughout?",
             ["A held bass drone",
              "A pipe organ",
              "A drum pulse",
              "Nothing, the texture is a single line"], 0),
            ("Which best describes the pulse?",
             ["No strong sense of beat",
              "A fast dance beat",
              "A steady march",
              "A swung shuffle"], 0),
            ("Which best describes the performing forces?",
             ["Unaccompanied choir",
              "Solo singer with organ",
              "Choir with full orchestra",
              "Instrumental ensemble with no voices"], 0),
        ],
    },
    "aos3_folk_fiddle": {
        "takes": {"a": "aos3_folk_fiddle_a", "b": "aos3_folk_fiddle_b"},
        # the whole point of this clip is a defensible instrument question, so
        # an unprimed probe MUST volunteer the fiddle
        "expect_any": ["fiddle", "violin"],
        "reject_any": ["drum kit", "synth", "electric"],
        "questions": [
            ("Which instrument plays the melody?",
             ["Fiddle", "Flute", "Accordion", "Acoustic guitar"], 0),
            ("What happens the second time the tune is played?",
             ["It is decorated with extra ornaments",
              "It is played much more slowly",
              "It moves to a different instrument",
              "It is played in unison by everyone"], 0),
            ("What accompanies the melody?",
             ["Strummed guitar and hand percussion",
              "Piano and double bass",
              "Full orchestra",
              "Nothing, it is unaccompanied"], 0),
        ],
    },
}


def free_text(b64, prompt):
    return " ".join(wv.gem({"contents": [{"parts": [
        {"inline_data": {"mime_type": "audio/mp3", "data": b64}},
        {"text": prompt}]}]}).split())


NEGATORS = ("no ", "not ", "without ", "none ", "absent", "lack")


def mentions(text, word):
    """True only if `word` appears OUTSIDE a negation.

    Learned the hard way: a take was disqualified because the drift word
    "vocal" matched inside "no discernible vocals" — the description was
    agreeing with the brief, not violating it.
    """
    low = text.lower()
    start = 0
    while True:
        i = low.find(word, start)
        if i < 0:
            return False
        window = low[max(0, i - 24):i]
        if not any(n in window for n in NEGATORS):
            return True
        start = i + len(word)


def idiom_gate(b64, spec, rounds=3):
    """Repeat unprimed probes. ONE description is not evidence — in batch 2 two
    probes on the same take returned 'North African folk' and 'xylophone'.
    Only a feature the majority of independent probes volunteers counts."""
    texts = []
    for i in range(rounds):
        texts.append(free_text(b64, DESCRIBE if i == 0 else
                               "In two sentences: what style or genre is this, and which "
                               "instruments play it? Be specific and concrete."))
        time.sleep(3)
    texts.append(free_text(b64, INSTRUMENTS))
    time.sleep(3)
    need = len(texts) / 2.0
    hits = [w for w in spec["expect_any"]
            if sum(1 for t in texts if mentions(t, w)) > need]
    vetoes = [w for w in spec["reject_any"]
              if sum(1 for t in texts if mentions(t, w)) > need]
    return texts, hits, vetoes, bool(hits) and not vetoes


def validate(name, path, spec, rng):
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    print("\n=== %s ===" % name)

    texts, hits, vetoes, gate = idiom_gate(b64, spec)
    for i, t in enumerate(texts):
        print("  PROBE%d: %s" % (i + 1, t[:200]))
    desc, instr = texts[0], texts[-1]
    print("  GATE : %s  (majority-reported: %s | drift words: %s)"
          % ("PASS" if gate else "FAIL", hits or "none", vetoes or "none"))

    qres = []
    for question, options, truth_i in spec["questions"]:
        truth = options[truth_i]
        votes = []
        for _ in range(3):
            topts = list(options)
            rng.shuffle(topts)
            letter, _why = wv.ask(b64, question, topts)
            gi = (ord(letter) - 65) if len(letter) == 1 else -1
            votes.append(topts[gi] if 0 <= gi < len(topts) else "?")
            time.sleep(3)
        n_truth = votes.count(truth)
        top, top_n = Counter(votes).most_common(1)[0]
        status = ("verified" if n_truth >= 2
                  else "flagged-consistent" if top_n >= 2 and top != truth
                  else "flagged-ambiguous")
        flags = []
        if status == "verified":
            for opt in options:
                if opt == truth:
                    continue
                verdict = wv.gem({"contents": [{"parts": [
                    {"inline_data": {"mime_type": "audio/mp3", "data": b64}},
                    {"text": "Consider this statement about the audio: \"%s\" (in answer to: %s)\n"
                             "Is the statement TRUE or FALSE of this audio? A statement that is even "
                             "partially or arguably true counts as TRUE. Reply EXACTLY: VERDICT: TRUE "
                             "or VERDICT: FALSE - one sentence why" % (opt, question)}]}]})
                if "VERDICT: TRUE" in verdict.upper().replace("**", ""):
                    flags.append(opt)
                time.sleep(3)
        qres.append({"q": question, "truth": truth, "votes": votes, "status": status,
                     "distractor_flags": flags})
        print("  %-9s %s%s" % (status.upper().replace("FLAGGED-", "FLAG:"), question[:58],
                               "  [%d flag]" % len(flags) if flags else ""))
    return {"description": desc, "instruments": instr, "gate": gate,
            "gate_hits": hits, "gate_vetoes": vetoes, "questions": qres}


def main():
    os.makedirs(os.path.join(OUT, "trimmed"), exist_ok=True)
    rng = random.Random(53)
    results, files = {}, {}

    for base, spec in CLIPS.items():
        for suffix, stem in spec["takes"].items():
            matches = glob.glob(os.path.join(DOWNLOADS, stem + ".*"))
            if not matches:
                print("MISSING:", stem)
                continue
            mp3 = os.path.join(OUT, "%s_%s.mp3" % (base, suffix))
            if not os.path.exists(mp3):
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", matches[0],
                                "-codec:a", "libmp3lame", "-b:a", "112k", mp3], check=True)
            files[(base, suffix)] = mp3

    for (base, suffix), path in sorted(files.items()):
        results["%s_%s" % (base, suffix)] = validate(
            "%s_%s" % (base, suffix), path, CLIPS[base], rng)

    winners = {}
    for base, spec in CLIPS.items():
        scores = {}
        for suffix in spec["takes"]:
            r = results.get("%s_%s" % (base, suffix))
            if not r:
                continue
            clean = sum(1 for q in r["questions"]
                        if q["status"] == "verified" and not q["distractor_flags"])
            # a take that failed the unprimed gate is not eligible, however
            # well it scored under primed options
            scores[suffix] = clean if r["gate"] else -1
        # A take with zero clean-verified questions is not a winner, it is a
        # clip with no usable questions. Batch 2 "won" the Hungarian dance on
        # 0 vs 0 and the clip turned out to be a circus march.
        if not scores or max(scores.values()) < 1:
            print("\nNO WINNER %s - no take cleared the gate with a clean question (%s)"
                  % (base, scores))
            continue
        best = max(sorted(scores), key=lambda s: scores[s])
        winners[base] = best
        print("\nWINNER %s: take %s (clean-verified: %s)" % (base, best, scores))

        src = files[(base, best)]
        dst = os.path.join(OUT, "trimmed", base + ".mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "8", "-t", str(WINDOW),
                        "-i", src, "-codec:a", "libmp3lame", "-b:a", "112k",
                        "-af", "afade=t=in:d=0.5,afade=t=out:st=%d:d=1" % (WINDOW - 1),
                        dst], check=True)
        b64 = base64.b64encode(open(dst, "rb").read()).decode()
        # the trim re-earns the idiom too, not just the questions: a 40s window
        # can land on the one section that sounds like something else
        _t, thits, tvetoes, tgate = idiom_gate(b64, spec, rounds=2)
        results["%s_%s" % (base, best)]["trim_gate"] = tgate
        print("  TRIM GATE %s (majority-reported: %s | drift: %s)"
              % ("PASS" if tgate else "FAIL", thits or "none", tvetoes or "none"))
        for q in results["%s_%s" % (base, best)]["questions"]:
            if q["status"] != "verified":
                continue
            options = next(o for qq, o, _t in spec["questions"] if qq == q["q"])
            votes = []
            for _ in range(2):
                topts = list(options)
                rng.shuffle(topts)
                letter, _why = wv.ask(b64, q["q"], topts)
                gi = (ord(letter) - 65) if len(letter) == 1 else -1
                votes.append(topts[gi] if 0 <= gi < len(topts) else "?")
                time.sleep(3)
            q["trim_verified"] = votes.count(q["truth"]) == 2
            print("  TRIM %s %s" % ("PASS" if q["trim_verified"] else "RECHECK", q["q"][:56]))

    io.open(os.path.join(OUT, "_batch2_results.json"), "w", encoding="utf-8").write(
        json.dumps({"results": results, "winners": winners}, ensure_ascii=False, indent=1))
    print("\n==== DONE. winners: %s ====" % winners)


if __name__ == "__main__":
    main()
