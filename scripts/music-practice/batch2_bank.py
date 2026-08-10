# -*- coding: utf-8 -*-
"""Batch-2 survivors: the two clips whose idiom held up under repeat unprimed
description, with questions rewritten to match what the audio actually is.

Three of the five batch-2 clips were rejected outright — see REJECTED below.
Nothing here inherits a verification from the first batch-2 run: those were
produced under primed options, and primed options endorsed keyed answers on
clips that later proved to be the wrong genre entirely. Every question below
was re-voted and re-audited on the TRIM that ships.

qids start at 101 so the option-shuffle seeds can never collide with batch 1's.
"""
import os
import random

_TMP = r"C:\Users\tshau\.claude\jobs\4059242c\tmp"
TRIM = os.path.join(_TMP, "flow_batch2", "trimmed")
R2_PREFIX = "music-aqa/aos-listening"
QID_BASE = 100

REJECTED = {
    # Repeat unprimed probes, three per clip, on the trimmed winner:
    "aos4_minimalism_v3": "came back as polka / oompah / cumbia with accordion "
                          "and drum kit - both banned in the prompt. Third "
                          "failed attempt at minimalism (constructed v1, Flow "
                          "v2 new-age, Flow v3 polka).",
    "aos4_hungarian_dance_orch": "light operetta march / circus march. No "
                                 "cimbalom, no modal folk tune, no snap rhythm "
                                 "- the march attractor again.",
    "aos4_american_orch": "slow Romantic string serenade with solo violin and "
                          "pizzicato. None of the brief's open spacing, solo "
                          "trumpet or hymn tune growing to brass.",
}

SECTIONS = [
    ("aos3_folk_fiddle", "aos3", "flow_ab",
     "Take A. Three unprimed probes agree: Celtic jig/reel, fiddle leading, "
     "plucked and strummed accompaniment (mandolin, guitar, upright bass).",
     [("Which instrument plays the melody?",
       # 'Accordion' was endorsed as also-true and had to go: one probe heard
       # an accordion in the accompaniment. Brass appears in no description.
       ["Fiddle", "Trumpet", "Church organ", "Piano"], 0),
      ("What happens when the tune comes round again?",
       ["It is decorated with extra ornaments",
        "It is played much more slowly",
        "It moves to a brass instrument",
        "It is sung"], 0),
      ("Which best describes the accompaniment?",
       ["Plucked and strummed string instruments",
        "A full symphony orchestra",
        "Piano and drum kit",
        "Nothing - the melody is unaccompanied"], 0)]),
    ("aos4_sacred_static", "aos4", "flow_ab",
     "Take A. Sacred choral, slow and static, with a sustained drone underneath "
     "that every probe attributes to an organ - so the authored 'unaccompanied "
     "choir' question was false and was dropped, along with a pulse question "
     "the ensemble consistently answered another way.",
     [("What sounds underneath the voices throughout?",
       ["A sustained drone",
        "A fast drum pulse",
        "Plucked guitar chords",
        "Nothing - the voices sing alone"], 0),
      ("Which best describes how the voices move?",
       ["Slowly, in smooth steps, holding long notes",
        "In fast leaping runs",
        "In short detached bursts",
        "Each voice sings a different fast rhythm"], 0)]),
]


def build_bank():
    bank, qid = [], QID_BASE
    for clip, aos, provenance, note, qs in SECTIONS:
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
                "note": note,
                "path": os.path.join(TRIM, clip + ".mp3"),
                "r2_key": "%s/%s.mp3" % (R2_PREFIX, clip),
                "question": question,
                "options": order,
                "correct": order.index(truth),
                "answer": truth,
            })
    return bank
