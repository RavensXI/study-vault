# -*- coding: utf-8 -*-
"""Three-pass validation of Flow-generated listening excerpts (AoS2-4).

Pass 0 — unprimed open-ended description (does the clip match its brief?).
Pass 1 — 3-vote shuffled MCQ ensemble per candidate question (>=2 for truth).
Pass 2 — distractor audit on verified questions: each distractor judged
         TRUE/FALSE of the audio; any TRUE distractor is flagged for rewrite
         (plausible-but-ALSO-correct options are unfair, not just implausible
         ones).

Generated audio is claim-class, not construction-class: nothing ships without
passing all three passes plus Tom's ear.

Usage: python scripts/music-practice/validate_flow_batch.py <folder-of-mp3s>
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

import works_verify as wv

# Per clip: brief (for pass 0 judgement) + questions [(question, options, truth_index)]
CLIPS = {
    "aos2_broadway_ballad": {
        "brief": "Broadway show-tune ballad, solo female voice, piano-only rubato opening then orchestra enters at a steady tempo, big crescendo",
        "questions": [
            ("How does the accompaniment change during this excerpt?",
             ["It stays piano-only throughout", "It starts with piano only, then the orchestra joins",
              "The full orchestra plays from the very start", "The voice is unaccompanied throughout"], 1),
            ("Which best describes the voice?",
             ["Solo female voice", "Solo male voice", "A duet", "A full choir"], 0),
            ("Which best describes the tempo of the opening?",
             ["Strict and metronomic from the start", "Free and flexible (rubato), becoming steady later",
              "Very fast throughout", "Gradually slowing down throughout"], 1),
        ]},
    "aos2_rock_shuffle": {
        "brief": "1970s rock, swung shuffle groove, overdriven guitar riff, bass doubling, male vocal after instrumental intro",
        "questions": [
            ("Which best describes the rhythmic feel?",
             ["Straight, even quavers", "A swung shuffle", "A waltz in three", "Free rhythm with no steady beat"], 1),
            ("Which best describes the electric guitar part?",
             ["Clean fingerpicked arpeggios", "An overdriven repeated riff",
              "Sustained jazz chords", "Acoustic slide playing"], 1),
            ("When does the singing begin?",
             ["From the very first bar", "After an instrumental introduction",
              "There is no singing in this excerpt", "Only in the final seconds"], 1),
        ]},
    "aos2_film_score": {
        "brief": "epic orchestral film score, low staccato string ostinato, heroic horn theme, layered build",
        "questions": [
            ("What device does the string section use?",
             ["A repeated rhythmic pattern (ostinato)", "A single sustained drone note",
              "A walking bass line", "Silence between long chords"], 0),
            ("How does the excerpt develop?",
             ["Layers are added gradually, building up", "It stays at the same level throughout",
              "It gets steadily quieter and thinner", "It alternates suddenly between loud and silent"], 0),
            ("Which instruments carry the main theme?",
             ["Horns / brass", "Solo violin", "Choir", "Solo piano"], 0),
        ]},
    "aos2_game_music": {
        "brief": "chiptune-influenced game music, square-wave synth melody, arpeggiated accompaniment, loop repeats with added countermelody, programmed drums",
        "questions": [
            ("Which best describes the sound sources?",
             ["Acoustic orchestral instruments", "Synthesised electronic sounds",
              "Solo acoustic piano", "A jazz big band"], 1),
            ("What happens when the opening phrase returns?",
             ["It repeats exactly, unchanged", "A countermelody is added over it",
              "It is replaced by completely new music", "It returns much slower"], 1),
        ]},
    "aos2_pop_dance": {
        "brief": "90s-present dance-pop, four-on-the-floor kick, off-beat synth stabs, repeated female vocal hook, claps on 2 and 4",
        "questions": [
            ("Which best describes the kick drum pattern?",
             ["A kick on every beat (four-on-the-floor)", "Kicks only on beats 2 and 4",
              "A swung shuffle pattern", "No drums are present"], 0),
            ("How are the synth chords played?",
             ["Short stabs on the off-beats", "Long sustained chords on every downbeat",
              "A flowing arpeggio pattern only", "There are no synth chords"], 0),
            ("Which best describes the vocal writing?",
             ["A short catchy hook that repeats", "One long continuous melody that never repeats",
              "Spoken word throughout", "Wordless humming only"], 0),
        ]},
    "aos3_blues": {
        "brief": "1940s Chicago blues, slow 12-bar, swung, walking bass, male vocal with bends, guitar licks answering each sung phrase",
        "questions": [
            ("What happens after each sung phrase?",
             ["A short guitar lick answers it (call and response)", "A drum solo",
              "The full band stops completely", "A female backing choir repeats the words"], 0),
            ("Which best describes the rhythmic feel?",
             ["Swung / shuffle feel", "Straight machine-like rhythm",
              "A fast waltz", "Free rhythm with no pulse"], 0),
            ("Which best describes the harmony?",
             ["A repeating blues chord pattern", "Constantly changing keys with no repetition",
              "A single drone chord throughout", "Atonal with no chords"], 0),
        ]},
    "aos3_african_fusion": {
        "brief": "African fusion, two interlocking clean guitar ostinatos, cross-rhythm percussion, prominent melodic bass, major/joyful",
        "questions": [
            ("How do the guitar parts relate to each other?",
             ["They play interlocking repeated patterns", "One strums chords while the other is silent",
              "They play the same melody in unison throughout", "They trade long improvised solos"], 0),
            ("Which best describes the percussion?",
             ["Layered patterns with cross-rhythms", "A single bass drum on every beat",
              "Orchestral timpani rolls", "No percussion is present"], 0),
        ]},
    "aos3_latin": {
        "brief": "salsa, clave, syncopated piano montuno, brass stabs, congas/timbales, lead vocal with group response",
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
        "brief": "British folk, fiddle modal melody over fingerpicked acoustic guitar, sustained drone, female voice doubles melody in verse 2",
        "questions": [
            ("What sounds underneath the melody through the excerpt?",
             ["A sustained drone", "A walking jazz bass line",
              "Electronic dance drums", "Nothing - the melody is unaccompanied"], 0),
            ("Which instruments open the excerpt?",
             ["Fiddle and acoustic guitar", "Electric guitar and synthesiser",
              "Brass band", "Solo piano"], 0),
            ("What changes later in the excerpt?",
             ["A voice joins, doubling the melody", "The music changes into a fast dance",
              "Everything drops out except drums", "The key changes to minor and stays there"], 0),
        ]},
    "aos4_minimalism": {
        "brief": "minimalism, marimba+piano repeating short cells, additive change, strings fade in, steady pulse",
        "questions": [
            ("How does the music develop?",
             ["Short repeated patterns gradually change and gain layers", "Contrasting sections alternate abruptly",
              "One long melody never repeats", "It develops through loud drum fills"], 0),
            ("Which best describes the pulse?",
             ["Steady and constant throughout", "Constantly speeding up and slowing down",
              "Free with no sense of beat", "Interrupted by silences"], 0),
            ("Which instruments are most prominent?",
             ["Tuned percussion and piano", "Distorted electric guitars",
              "A church organ", "A solo cello"], 0),
        ]},
    "aos4_pastoral_orchestral": {
        "brief": "20th-c American pastoral orchestral, widely spaced quiet strings with open 4ths/5ths, solo clarinet melody, gentle brass entry, slow",
        "questions": [
            ("Which best describes the string writing?",
             ["Widely spaced, open, quiet chords", "Fast aggressive rhythmic chopping",
              "A dense romantic wall of sound", "Pizzicato throughout"], 0),
            ("Which best describes the main melody?",
             ["A simple solo woodwind line", "A loud full-brass fanfare",
              "A virtuosic violin solo", "A sung soprano line"], 0),
            ("Which best describes the overall character?",
             ["Slow, spacious and calm", "Fast, dense and aggressive",
              "A lively dance", "A funeral march with heavy drums"], 0),
        ]},
    "aos4_dissonant_modern": {
        "brief": "dissonant modernist orchestral, angular fragments passed around, harsh chords, irregular accents, extreme dynamic contrasts, percussion interjections",
        "questions": [
            ("Which best describes the melodic writing?",
             ["Angular fragments passed between instruments", "One long smooth romantic melody",
              "A repeated singable folk tune", "No melodic material at all"], 0),
            ("Which best describes the dynamics?",
             ["Extreme sudden contrasts", "Quiet and unchanging throughout",
              "One long single crescendo", "Loud and unchanging throughout"], 0),
            ("Which best describes the harmony?",
             ["Harsh and dissonant", "Simple major-key chords",
              "A single drone throughout", "Sweet romantic harmony"], 0),
        ]},
}


def main(folder):
    rng = random.Random(11)
    results = {}
    for name, spec in CLIPS.items():
        path = os.path.join(folder, name + ".mp3")
        if not os.path.exists(path):
            print("MISSING:", path)
            continue
        b64 = base64.b64encode(open(path, "rb").read()).decode()
        print("\n=== %s ===" % name)

        # Pass 0: unprimed description
        desc = wv.gem({"contents": [{"parts": [
            {"inline_data": {"mime_type": "audio/mp3", "data": b64}},
            {"text": "Describe this music: genre/era it evokes, instruments and voices you hear, "
                     "and three notable musical features. Three sentences maximum."}]}]})
        desc = " ".join(desc.split())
        print("  DESC:", desc[:220])
        time.sleep(3)

        qres = []
        for qi, (question, options, truth_i) in enumerate(spec["questions"]):
            truth = options[truth_i]
            votes = []
            for t in range(3):
                topts = list(options)
                rng.shuffle(topts)
                letter, why = wv.ask(b64, question, topts)
                gi = (ord(letter) - 65) if len(letter) == 1 else -1
                votes.append(topts[gi] if 0 <= gi < len(topts) else "?")
                time.sleep(3)
            n_truth = votes.count(truth)
            top, top_n = Counter(votes).most_common(1)[0]
            status = ("verified" if n_truth >= 2
                      else "flagged-consistent" if top_n >= 2 and top != truth
                      else "flagged-ambiguous")
            entry = {"q": question, "truth": truth, "votes": votes, "status": status, "distractor_flags": []}

            # Pass 2: distractor audit (verified questions only)
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
                        entry["distractor_flags"].append({"option": opt, "why": " ".join(verdict.split())[:160]})
                    time.sleep(3)
            qres.append(entry)
            flags = len(entry["distractor_flags"])
            print("  Q%d %-9s %s%s" % (qi + 1, status.upper().replace("FLAGGED-", "FLAG:"),
                                       question[:60], ("  [%d distractor flag(s)]" % flags) if flags else ""))
            for f in entry["distractor_flags"]:
                print("      DISTRACTOR-ALSO-TRUE: %r - %s" % (f["option"][:50], f["why"][:90]))
        results[name] = {"description": desc, "questions": qres}

    out = os.path.join(folder, "_validation_results.json")
    io.open(out, "w", encoding="utf-8").write(json.dumps(results, ensure_ascii=False, indent=1))
    total = sum(len(r["questions"]) for r in results.values())
    ver = sum(1 for r in results.values() for q in r["questions"] if q["status"] == "verified")
    clean = sum(1 for r in results.values() for q in r["questions"]
                if q["status"] == "verified" and not q["distractor_flags"])
    print("\n==== SUMMARY: %d questions | %d verified | %d verified with clean distractors ====" % (total, ver, clean))
    print("results:", out)


if __name__ == "__main__":
    main(sys.argv[1])
