# -*- coding: utf-8 -*-
"""Trim validated Flow excerpts to their teaching windows and re-verify the
surviving questions on the trimmed audio (a trim can cut off the feature a
question depends on, so trimmed clips re-earn their verification).

Window strategy: clips whose questions hinge on a transition (accompaniment
change, voice joining, phrase-repeat-with-countermelody) get a machine-
timestamped window spanning the transition; steady-state clips get an early
window once the full texture is in.

Usage: python scripts/music-practice/trim_flow_batch.py <folder>
"""
import base64
import io
import json
import os
import random
import re
import subprocess
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import works_verify as wv

# Surviving questions per clip (post-validation curation, 3 Aug):
# dropped: broadway Q3 (no real rubato), rock Q1 (straight not swung),
# film Q3 (theme-carrier mis-keyed), pop Q2 (pads not stabs),
# african_fusion/minimalism/pastoral/dissonant (clips regenerating).
# blues Q2 (swing) kept but marked EAR — Tom's ear is the tiebreak.
PLAN = {
    "aos2_broadway_ballad": {
        "transition": "the moment the orchestra joins the piano accompaniment",
        "questions": [
            ("How does the accompaniment change during this excerpt?",
             ["It stays piano-only throughout", "It starts with piano only, then the orchestra joins",
              "The full orchestra plays from the very start", "The voice is unaccompanied throughout"], 1),
            ("Which best describes the voice?",
             ["Solo female voice", "Solo male voice", "A duet", "A full choir"], 0),
        ]},
    "aos2_rock_shuffle": {
        "transition": "the moment the male vocal enters after the instrumental introduction",
        "questions": [
            ("Which best describes the electric guitar part?",
             ["Clean fingerpicked arpeggios", "An overdriven repeated riff",
              "Sustained jazz chords", "Acoustic slide playing"], 1),
            ("When does the singing begin?",
             ["From the very first bar", "After an instrumental introduction",
              "There is no singing in this excerpt", "Only in the final seconds"], 1),
        ]},
    "aos2_film_score": {
        "transition": None,
        "questions": [
            ("What device does the string section use?",
             ["A repeated rhythmic pattern (ostinato)", "One single sustained note held throughout",
              "Fast scales running up and down constantly", "They do not play in this excerpt"], 0),
            ("How does the excerpt develop?",
             ["Layers are added gradually, building up", "It stays at the same level throughout",
              "It gets steadily quieter and thinner", "It alternates suddenly between loud and silent"], 0),
        ]},
    "aos2_game_music": {
        "transition": "the moment the opening phrase returns with a countermelody added",
        "questions": [
            ("Which best describes the sound sources?",
             ["Acoustic orchestral instruments", "Synthesised electronic sounds",
              "Solo acoustic piano", "A jazz big band"], 1),
            ("What happens when the opening phrase returns?",
             ["It repeats exactly, unchanged", "A countermelody is added over it",
              "It is replaced by completely new music", "It returns much slower"], 1),
        ]},
    "aos2_pop_dance": {
        "transition": None,
        "questions": [
            ("Which best describes the kick drum pattern?",
             ["A kick on every beat (four-on-the-floor)", "Kicks only on beats 2 and 4",
              "A swung shuffle pattern", "No drums are present"], 0),
            ("Which best describes the vocal writing?",
             ["A short catchy hook that repeats", "One long continuous melody that never repeats",
              "Spoken word throughout", "Wordless humming only"], 0),
        ]},
    "aos3_blues": {
        "transition": None,
        "questions": [
            ("What happens after each sung phrase?",
             ["A short guitar lick answers it (call and response)", "A drum solo",
              "The full band stops completely", "A female backing choir repeats the words"], 0),
            ("Which best describes the rhythmic feel?",  # EAR: Tom tiebreak
             ["Swung / shuffle feel", "Straight machine-like rhythm",
              "A fast waltz", "Free rhythm with no pulse"], 0),
            ("Which best describes the harmony?",
             ["A repeating blues chord pattern", "Constantly changing keys with no repetition",
              "A single drone chord throughout", "Atonal with no chords"], 0),
        ]},
    "aos3_latin": {
        "transition": None,
        "questions": [
            ("Which best describes the piano part?",
             ["A repeated syncopated pattern (montuno)", "Slow sustained chords",
              "A classical flowing melody", "There is no piano"], 0),
            ("How does the brass section play?",
             ["Short punchy stabs", "One long sustained chorale",
              "A gentle background pad", "There is no brass"], 0),
            ("Which best describes the vocals?",
             ["A lead voice answered by a group (call and response)", "A solo voice with no response",
              "A full choir singing in harmony throughout", "There are no vocals"], 0),
        ]},
    "aos3_british_folk": {
        "transition": "the moment the voice joins, doubling the instrumental melody",
        "questions": [
            ("What sounds underneath the melody through the excerpt?",
             ["A sustained drone", "Electronic dance drums",
              "A brass fanfare", "Nothing - the melody is unaccompanied"], 0),
            ("Which instruments open the excerpt?",
             ["Fiddle and acoustic guitar", "Electric guitar and synthesiser",
              "Brass band", "Solo piano"], 0),
            ("What changes during the excerpt?",
             ["A voice joins, doubling the melody", "All the instruments stop one by one",
              "A drum kit takes over completely", "The melody never changes in any way"], 0),
        ]},
}

WINDOW = 40  # seconds


def probe_transition(b64, what):
    times = []
    for t in range(2):
        try:
            text = wv.gem({"contents": [{"parts": [
                {"inline_data": {"mime_type": "audio/mp3", "data": b64}},
                {"text": "At what time in this clip does the following happen: %s? "
                         "Reply EXACTLY: TIME: M:SS - one sentence why" % what}]}]})
            m = re.search(r"TIME:\s*(\d+):(\d{2})", text)
            if m:
                times.append(int(m.group(1)) * 60 + int(m.group(2)))
        except Exception as e:
            print("  probe error:", str(e)[:80])
        time.sleep(3)
    return times


def main(folder):
    rng = random.Random(23)
    out_dir = os.path.join(folder, "trimmed")
    os.makedirs(out_dir, exist_ok=True)
    results = {}
    for name, spec in PLAN.items():
        src = os.path.join(folder, name + ".mp3")
        if not os.path.exists(src):
            print("MISSING:", src)
            continue
        print("\n=== %s ===" % name)
        b64_full = base64.b64encode(open(src, "rb").read()).decode()

        if spec["transition"]:
            times = probe_transition(b64_full, spec["transition"])
            if times:
                t = sorted(times)[len(times) // 2]
                start = max(0, t - 15)
                print("  transition ~%ds (probes: %s) -> window %d-%ds" % (t, times, start, start + WINDOW))
            else:
                start = 5
                print("  transition probe failed -> default window 5-%ds" % (5 + WINDOW))
        else:
            start = 8  # skip any intro swell; full texture usually in by then
            print("  steady-state -> window %d-%ds" % (start, start + WINDOW))

        dst = os.path.join(out_dir, name + ".mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start),
                        "-t", str(WINDOW), "-i", src, "-codec:a", "libmp3lame",
                        "-b:a", "112k", "-af", "afade=t=in:d=0.5,afade=t=out:st=%d:d=1" % (WINDOW - 1),
                        dst], check=True)
        b64 = base64.b64encode(open(dst, "rb").read()).decode()

        qres = []
        for question, options, truth_i in spec["questions"]:
            truth = options[truth_i]
            votes = []
            for t in range(2):
                topts = list(options)
                rng.shuffle(topts)
                letter, why = wv.ask(b64, question, topts)
                gi = (ord(letter) - 65) if len(letter) == 1 else -1
                votes.append(topts[gi] if 0 <= gi < len(topts) else "?")
                time.sleep(3)
            ok = votes.count(truth) == 2
            qres.append({"q": question, "truth": truth, "votes": votes, "trim_verified": ok})
            print("  %s %s" % ("PASS" if ok else "RECHECK", question[:64]))
        results[name] = {"window": [start, start + WINDOW], "questions": qres}

    io.open(os.path.join(out_dir, "_trim_results.json"), "w", encoding="utf-8").write(
        json.dumps(results, ensure_ascii=False, indent=1))
    total = sum(len(r["questions"]) for r in results.values())
    ok = sum(1 for r in results.values() for q in r["questions"] if q["trim_verified"])
    print("\n==== TRIM SUMMARY: %d/%d questions pass on trimmed audio ====" % (ok, total))


if __name__ == "__main__":
    main(sys.argv[1])
