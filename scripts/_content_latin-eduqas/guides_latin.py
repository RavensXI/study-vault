# -*- coding: utf-8 -*-
"""Phase 5 revision-technique guides for GCSE Latin.

The seven canonical technique pages are pedagogy-fixed; only the worked
examples are subject-specific. Classical Civilisation (OCR) is the nearest
existing subject, so its guide set is adapted rather than written from nothing:
the pedagogy text passes through untouched and the agent replaces any example
that leans on a topic Latin does not teach.

Unlike the driver's own guides stage, this one shows the agent the practice
units too — half of this qualification is language drilling, so a revision
guide that only ever illustrates with literature topics would misrepresent the
course.

Usage:
    python scripts/_content_latin-eduqas/guides_latin.py submit
    python scripts/_content_latin-eduqas/guides_latin.py poll
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts", "api_build"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import driver as D  # noqa: E402

CFG_PATH = os.path.join(HERE, "config_latin-eduqas.json")


def all_units(plan):
    return plan.get("article_units", []) + plan.get("practice_units", [])


def stage_submit(cfg):
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    src = D.supa(cfg, "GET", "/rest/v1/subjects?slug=eq.%s&select=id"
                 % cfg["source_subject_slug"])
    guides = D.supa(cfg, "GET",
                    "/rest/v1/guide_pages?subject_id=eq.%s&select=slug,guide_type,"
                    "title,sort_order,content_html&order=sort_order" % src[0]["id"])
    topics = [u["name"] for u in all_units(plan)]
    lesson_titles = [l["title"] for u in all_units(plan) for l in u["lessons"]]
    cl = D.client()
    reqs, passthrough = [], {}
    for g in guides:
        html = g["content_html"].replace("/guide/%s/" % cfg["source_subject_slug"],
                                         "/guide/%s/" % cfg["slug"])
        if g["slug"] == "index":
            passthrough[g["slug"]] = dict(g, content_html=html)
            continue
        user = (
            "This is a revision-technique guide page. It was written for GCSE "
            "Classical Civilisation and is being adapted for GCSE Latin, which "
            "is a different subject on the same platform.\n\n"
            "Latin's units are:\n%s\n\nIts lesson titles are:\n%s\n\n"
            "Latin is half language and half literature: students learn a "
            "440-word vocabulary list, the accidence and syntax of the language, "
            "how to translate an unseen Latin passage into English, two "
            "prescribed literature themes with Latin texts and picture sources, "
            "a prescribed Latin narrative, and a Roman civilisation topic.\n\n"
            "TASK: the pedagogy text is canonical — do not touch it. ONLY change "
            "the subject worked examples, so that every example uses a Latin "
            "topic from the lists above. At least two examples on the page must "
            "come from the language side of the course (vocabulary, accidence, "
            "syntax or translation), because that is half the qualification. "
            "Match the original examples' depth and format exactly.\n\n"
            "HARD RULES: never name an exam board; never use a specification, "
            "paper, component or section code; never invent a mark tariff or a "
            "timing; British English; this qualification is not tiered. Keep ALL "
            "HTML structure, classes and entity usage identical. Return ONLY the "
            "full HTML, no code fences, no commentary.\n\nGUIDE HTML:\n%s"
        ) % (json.dumps(topics), json.dumps(lesson_titles), html)
        reqs.append({"custom_id": "guide-" + g["slug"], "params": {
            "model": D.MODEL_CONTENT, "max_tokens": 16000,
            "messages": [{"role": "user", "content": user}],
        }})
        passthrough[g["slug"]] = dict(g, content_html=html)
    D.write_json(os.path.join(cfg["run_dir"], "guides_base.json"), passthrough)
    batch = cl.messages.batches.create(requests=reqs)
    st = D.load_state(cfg)
    st["guides_batch_id"] = batch.id
    D.save_state(cfg, st)
    print("guides batch submitted: %s (%d technique pages + index passthrough)"
          % (batch.id, len(reqs)))


def stage_poll(cfg):
    st = D.load_state(cfg)
    out = D.collect_batch(cfg, st["guides_batch_id"], "guides", "raw_guides")
    if out is None:
        return
    texts, errors = out
    base = json.load(io.open(os.path.join(cfg["run_dir"], "guides_base.json"),
                             encoding="utf-8"))
    rows = []
    for slug, g in base.items():
        html = g["content_html"]
        key = "guide-" + slug
        if key in texts:
            t = texts[key].strip()
            if t.startswith("```"):
                t = re.sub(r"^```[a-zA-Z]*\s*", "", t)
                t = re.sub(r"\s*```$", "", t)
            if "<main" in t:
                html = t
        bad = [h for h in D.drift_grep(html)]
        for w in ("Eduqas", "WJEC", "C580QS", "Classical Civilisation", "J199"):
            if w in html:
                bad.append("stale reference: " + w)
        if bad:
            print("  WARNING %s: %s" % (slug, bad[:4]))
        rows.append({"subject_id": st["subject_id"], "slug": slug,
                     "guide_type": g["guide_type"], "title": g["title"],
                     "sort_order": g["sort_order"], "content_html": html})
    existing = D.supa(cfg, "GET", "/rest/v1/guide_pages?subject_id=eq.%s&select=slug"
                      % st["subject_id"])
    if existing:
        print("ABORT: %d guide rows already exist for this subject" % len(existing))
        return
    D.supa(cfg, "POST", "/rest/v1/guide_pages", rows)
    print("inserted %d guide pages (%s)" % (len(rows), ", ".join(r["slug"] for r in rows)))
    if errors:
        print("errored:", errors)


def main():
    cfg = D.load_config(CFG_PATH)
    stage = sys.argv[1] if len(sys.argv) > 1 else "submit"
    (stage_submit if stage == "submit" else stage_poll)(cfg)


if __name__ == "__main__":
    main()
