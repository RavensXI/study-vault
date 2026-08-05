# -*- coding: utf-8 -*-
"""Single source of truth for the AoS2-4 batch-1 excerpt bank.

Thirteen verified excerpts, 29 questions. Both the ear-review page Tom judged
and the wiring script read this module, so the option order he saw is the
option order that ships — a student's key can never drift from the reviewed one.

Provenance per clip:
  flow      — generated in Google Flow, then trimmed; questions re-verified on
              the trim (a trim can cut the feature out, so it re-earns its badge)
  flow_ab   — A/B regeneration; the winner is whichever produced more
              clean-verified questions
  construct — built from notation (music21 -> FluidSynth), so the structural
              answer is true by construction; the machine ear only corroborates
"""
import os
import random

_HERE = os.path.dirname(os.path.abspath(__file__))
_TMP = r"C:\Users\tshau\.claude\jobs\4059242c\tmp"
F1 = os.path.join(_TMP, "flow_batch1", "trimmed")
F2 = os.path.join(_TMP, "flow_batch1b", "trimmed")

# R2 namespace for the shipped clips
R2_PREFIX = "music-aqa/aos-listening"


def _plan_qs(clip, drop=()):
    from trim_flow_batch import PLAN
    return [(q, o, t) for q, o, t in PLAN[clip]["questions"] if q not in drop]


def sections():
    """(clip, folder, aos, provenance, note, [(question, options, truth_index)])"""
    from trim_flow_batch import PLAN
    from compose_batch1c import QUESTIONS as CONSTRUCTED
    from validate_flow_batch import CLIPS
    return [
        ("aos2_broadway_ballad", F1, "aos2", "flow",
         "EAR: Broadway/show-tune idiom, or too pop? (accompaniment-change "
         "question already dropped as ambiguous on this recording)",
         [_plan_qs("aos2_broadway_ballad")[1]]),
        ("aos2_rock_shuffle", F1, "aos2", "flow", "", _plan_qs("aos2_rock_shuffle")),
        ("aos2_film_score", F1, "aos2", "flow", "", _plan_qs("aos2_film_score")),
        ("aos2_game_music", F1, "aos2", "flow", "", _plan_qs("aos2_game_music")),
        ("aos2_pop_dance", F1, "aos2", "flow", "", _plan_qs("aos2_pop_dance")),
        ("aos3_blues", F1, "aos3", "flow",
         "EAR on Q2: machine split on swung vs straight", _plan_qs("aos3_blues")),
        ("aos3_latin", F1, "aos3", "flow", "", _plan_qs("aos3_latin")[:2]),
        ("aos3_latin_coro", F1, "aos3", "flow",
         "Second window (44-84s) of the same track - the coro section",
         [PLAN["aos3_latin"]["questions"][2]]),
        ("aos3_british_folk", F1, "aos3", "flow", "", _plan_qs("aos3_british_folk")),
        ("aos4_pastoral_orchestral", F2, "aos4", "flow_ab",
         "v2A - the solo reads as OBOE; the question says 'solo woodwind', so it holds",
         list(CLIPS["aos4_pastoral_orchestral"]["questions"])),
        ("aos3_caribbean_fusion", F2, "aos3", "flow_ab",
         "v2A - validated as reggae/ska fusion; the spec strand is "
         "'African AND/OR Caribbean'",
         [("How do the guitar parts relate to each other?",
           ["They play interlocking repeated patterns",
            "One strums chords while the other is silent",
            "They play the same melody in unison throughout",
            "They trade long improvised solos"], 0),
          ("Which best describes the percussion?",
           ["Layered patterns with cross-rhythms",
            "A military snare-drum march pattern",
            "Orchestral timpani rolls",
            "No percussion is present"], 0)]),
        ("aos4_minimalism", F2, "aos4", "construct",
         "Additive process true by construction", CONSTRUCTED["aos4_minimalism"]),
        ("aos4_dissonant_modern", F2, "aos4", "construct",
         "Ships as the dissonance FEATURE drill - real Bartok recordings carry "
         "the strand's authentic orchestral sound",
         CONSTRUCTED["aos4_dissonant_modern"]),
    ]


def build_bank():
    """Flat question records with the shipped (shuffled) option order.

    The shuffle is seeded from the question's 1-based position so it is stable
    across rebuilds: authored option sets put the true answer first far too
    often, and an unshuffled bank teaches position, not listening.
    """
    bank, qid = [], 0
    for clip, folder, aos, provenance, note, qs in sections():
        for question, options, truth_i in qs:
            qid += 1
            truth = options[truth_i]
            shuffled = list(options)
            random.Random(qid * 7919).shuffle(shuffled)
            bank.append({
                "qid": qid,
                "clip": clip,
                "aos": aos,
                "provenance": provenance,
                "note": note,
                "path": os.path.join(folder, clip + ".mp3"),
                "r2_key": "%s/%s.mp3" % (R2_PREFIX, clip),
                "question": question,
                "options": shuffled,
                "correct": shuffled.index(truth),
                "answer": truth,
            })
    return bank


if __name__ == "__main__":
    import sys
    sys.path.insert(0, _HERE)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    b = build_bank()
    print("%d questions across %d clips" % (b and len(b), len({r["clip"] for r in b})))
