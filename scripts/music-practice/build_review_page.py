# -*- coding: utf-8 -*-
"""Render an ear-review page for a batch of excerpts.

Tom judges audio the machine cannot: whether a clip convinces as its idiom, and
whether any distractor is arguably true. He needs the questions exactly as a
student meets them, so options render in the SAME deterministic shuffle that
ships - a review of a different option order reviews nothing.

    from build_review_page import render
    render(sections, out_path, title)      # sections: (clip, mp3, note, qs)

Run directly to build the batch-2 page from _batch2_results.json.
"""
import base64
import html
import io
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CSS = """
body{font-family:Inter,system-ui,sans-serif;background:#faf8f5;color:#2d2a26;
max-width:52rem;margin:2rem auto;padding:0 1rem;}
section{background:#fff;border-radius:16px;padding:1.25rem 1.5rem;margin-bottom:1.25rem;
box-shadow:0 2px 10px rgba(0,0,0,0.06);}
h2{margin:0 0 .5rem;font-size:1.05rem;} audio{width:100%;margin:.5rem 0 .75rem;}
ol{margin:0;padding-left:1.2rem;} .qq{margin-bottom:1rem;line-height:1.45;}
.opts{list-style:lower-alpha;margin:.4rem 0;padding-left:1.5rem;}
.opts li{margin-bottom:.15rem;padding:.1rem .4rem;border-radius:6px;}
.opts.shown .truth{background:#dcfce7;font-weight:600;}
button{background:#2d2a26;color:#faf8f5;border:0;border-radius:10px;
padding:.3rem .9rem;font-family:inherit;font-size:.8rem;cursor:pointer;}
.note{color:#b45309;font-size:.9rem;}
.machine{color:#57534e;font-size:.85rem;background:#f5f5f4;border-radius:10px;
padding:.5rem .7rem;margin:.35rem 0 .6rem;}
"""


def shuffled(options, truth_i, qid):
    """Deterministic per-question shuffle. Authored option sets put the true
    answer first far too often, and an unshuffled bank teaches position."""
    truth = options[truth_i]
    order = list(options)
    random.Random(qid * 7919).shuffle(order)
    return order, truth


def render(sections, out_path, title, start_qid=0):
    blocks, n_q, qid = [], 0, start_qid
    for clip, mp3, note, qs in sections:
        if not os.path.exists(mp3):
            print("MISSING:", mp3)
            continue
        b64 = base64.b64encode(open(mp3, "rb").read()).decode()
        items = []
        for entry in qs:
            question, options, truth_i = entry[0], entry[1], entry[2]
            machine = entry[3] if len(entry) > 3 else ""
            n_q += 1
            qid += 1
            order, truth = shuffled(options, truth_i, qid)
            opts = "".join('<li class="opt%s">%s</li>'
                           % (" truth" if o == truth else "", html.escape(o))
                           for o in order)
            items.append(
                '<li class="qq"><strong>%s</strong>%s<ul class="opts" id="q%d">%s</ul>'
                '<button onclick="document.getElementById(\'q%d\').classList.add(\'shown\')">'
                'Reveal</button></li>'
                % (html.escape(question),
                   '<div class="machine">%s</div>' % html.escape(machine) if machine else "",
                   qid, opts, qid))
        blocks.append('<section><h2>%s</h2>%s<audio controls preload="none" '
                      'src="data:audio/mp3;base64,%s"></audio><ol>%s</ol></section>'
                      % (html.escape(clip),
                         '<p class="note">%s</p>' % html.escape(note) if note else "",
                         b64, "".join(items)))
    doc = ('<!doctype html><html><head><meta charset="utf-8"><title>%s</title>'
           '<style>%s</style></head><body><h1>%s</h1>'
           '<p>Options appear exactly as a student meets them. Reveal highlights the '
           'keyed answer &mdash; judge whether every distractor is plausible but '
           'clearly wrong.</p>%s</body></html>'
           % (html.escape(title), CSS, html.escape(title), "".join(blocks)))
    io.open(out_path, "w", encoding="utf-8").write(doc)
    print("written %s  %d KB, %d questions" % (out_path, os.path.getsize(out_path) // 1024, n_q))
    return n_q


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    from run_flow_batch2 import CLIPS, OUT
    data = json.load(io.open(os.path.join(OUT, "_batch2_results.json"), encoding="utf-8"))
    results, winners = data["results"], data["winners"]
    sections = []
    for base, spec in CLIPS.items():
        if base not in winners:
            continue
        r = results["%s_%s" % (base, winners[base])]
        qs = []
        for question, options, truth_i in spec["questions"]:
            rec = next((q for q in r["questions"] if q["q"] == question), None)
            if not rec or rec["status"] != "verified" or not rec.get("trim_verified"):
                continue
            note = "machine: %s" % rec["status"]
            if rec["distractor_flags"]:
                note += " | distractor flagged as also-true: %s" % "; ".join(rec["distractor_flags"])
            qs.append((question, options, truth_i, note))
        if not qs:
            continue
        sections.append((base, os.path.join(OUT, "trimmed", base + ".mp3"),
                         "take %s | %s" % (winners[base], r["description"][:180]), qs))
    render(sections, os.path.join(OUT, "flow_batch2_ear_review.html"),
           "Flow batch 2 - ear review")


if __name__ == "__main__":
    main()
