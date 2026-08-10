# -*- coding: utf-8 -*-
"""Public-domain excerpt bank for AoS4 — real recordings, not generated audio.

Licence position (Tom's ruling, 5 Aug 2026): PUBLIC DOMAIN ONLY. CC BY-SA items
that the research turned up (Bartók Romanian Folk Dances, Nielsen Wind Quintet)
are excluded, because a trimmed excerpt is a derivative and share-alike would
follow it into a commercial product.

Every recording here is a US federal government work — "The President's Own" US
Marine Band and the US Army Band — so the RECORDING carries no copyright, and
each composer died before 1956 so the COMPOSITION is out of UK copyright too.
Both halves clear, which is what hosting requires.

TRUST MODEL differs from the generated clips. Identity and performing forces are
true by PROVENANCE: these are documented recordings by named ensembles, so "a
wind and percussion band" is a fact about the source. The 3-vote ensemble
verified every question below, but the distractor audit became unreliable on
this material — it endorsed "Baroque dance" for Rhapsody in Blue and "a gentle
waltz" for a march. Those endorsements are recorded in AUDIT_FLAGS and were
overruled on documented musical grounds, not quietly dropped. They are shown to
Tom in the review page.
"""
import os
import random

_TMP = r"C:\Users\tshau\.claude\jobs\4059242c\tmp"
PD_DIR = os.path.join(_TMP, "pd_audio")
R2_PREFIX = "music-aqa/aos-listening"
QID_BASE = 200

SOURCES = {
    "gershwin_rhapsody": {
        "file": "gershwin_rhapsody_w0.mp3",
        "credit": "Gershwin, <em>Rhapsody in Blue</em> (1924) — “The President’s Own” "
                  "United States Marine Band. Public domain (US federal government work).",
        "commons": "https://commons.wikimedia.org/wiki/File:US_Marine_Band_Rhapsody_in_Blue.oga",
    },
    "prokofiev_march": {
        "file": "prokofiev_march_w4.mp3",
        "credit": "Prokofiev, <em>March, Op. 99</em> (1943–44) — “The President’s Own” "
                  "United States Marine Band. Public domain (US federal government work).",
        "commons": "https://commons.wikimedia.org/wiki/File:PROKOFIEV_March,_Opus_99_-_%22The_President%27s_Own%22_U.S._Marine_Band.opus",
    },
    "respighi_catacomb": {
        "file": "respighi_catacomb_w10.mp3",
        "credit": "Respighi, <em>Pines of Rome</em> (1924), II. Pines Near a Catacomb — "
                  "United States Army Band. Public domain (US federal government work).",
        "commons": "https://commons.wikimedia.org/wiki/File:The_Pines_of_Rome_-_II._The_Pines_Near_a_Catacomb_-_United_States_Army_Band.mp3",
    },
}

# machine endorsements we overruled, shown to Tom rather than hidden
AUDIT_FLAGS = {
    ("gershwin_rhapsody", "Which instrument plays the opening solo?"): ["Trumpet", "Violin"],
    ("gershwin_rhapsody", "How does that opening solo line move?"):
        ["It descends in slow even steps", "It leaps about in short detached notes"],
    ("gershwin_rhapsody", "Which style has most clearly influenced this music?"): ["Baroque dance"],
    ("prokofiev_march", "Which best describes the rhythm?"):
        ["A swung jazz shuffle", "A gentle waltz"],
    ("prokofiev_march", "Which best describes the dynamics?"): ["One long fade to silence"],
    ("respighi_catacomb", "Which best describes the melodic writing?"): ["Short detached fragments"],
}

SECTIONS = [
    ("gershwin_rhapsody", "aos4", "public_domain",
     [("Which instrument plays the opening solo?",
       ["Clarinet", "Trumpet", "Violin", "Organ"], 0),
      ("How does that opening solo line move?",
       ["It slides smoothly upwards",
        "It repeats one note over and over",
        "It descends in slow even steps",
        "It leaps about in short detached notes"], 0),
      ("Which style has most clearly influenced this music?",
       ["Jazz and blues", "Baroque dance", "Minimalism", "Gregorian chant"], 0)]),
    ("prokofiev_march", "aos4", "public_domain",
     [("Which performing forces do you hear?",
       ["A wind and percussion band", "A string quartet", "A solo piano",
        "An unaccompanied choir"], 0),
      ("Which best describes the rhythm?",
       ["A steady march", "A slow free rhythm with no pulse",
        "A swung jazz shuffle", "A gentle waltz"], 0),
      ("Which best describes the dynamics?",
       ["Mostly loud and bold", "Very quiet throughout",
        "One long fade to silence", "Alternating silence and single notes"], 0)]),
    ("respighi_catacomb", "aos4", "public_domain",
     [("Which best describes the tempo?",
       ["Very slow", "Fast and driving", "A brisk march tempo",
        "Constantly speeding up and slowing down"], 0),
      ("What happens to the dynamics across the excerpt?",
       ["It begins very quietly and grows louder",
        "It is loud and unchanging",
        "It alternates suddenly between loud and silent",
        "It fades away to nothing from the start"], 0),
      ("Which best describes the melodic writing?",
       ["Long sustained lines", "Short detached fragments",
        "Fast running scales", "A single repeated note"], 0)]),
]


def build_bank():
    bank, qid = [], QID_BASE
    for clip, aos, provenance, qs in SECTIONS:
        src = SOURCES[clip]
        for question, options, truth_i in qs:
            qid += 1
            truth = options[truth_i]
            order = list(options)
            random.Random(qid * 7919).shuffle(order)
            bank.append({
                "qid": qid,
                "clip": clip,
                "aos": aos,
                "provenance": provenance,
                "credit": src["credit"],
                "commons": src["commons"],
                "note": "Real recording — identity and forces true by provenance.",
                "path": os.path.join(PD_DIR, src["file"]),
                "r2_key": "%s/%s.mp3" % (R2_PREFIX, clip),
                "question": question,
                "options": order,
                "correct": order.index(truth),
                "answer": truth,
                "audit_flags": AUDIT_FLAGS.get((clip, question), []),
            })
    return bank
