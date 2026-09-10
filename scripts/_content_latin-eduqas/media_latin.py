# -*- coding: utf-8 -*-
"""Phase 4 related-media curation for GCSE Latin — all 33 lessons.

The driver's media stage only walks `article_units`; Latin is a mixed-format
subject, so the practice lessons need curation too (the practice template reads
`related_media` off the lesson row exactly as the article template does).

The agent searches for real, currently-existing material and returns candidates
with margin; the zero-cost Python auditor
(`scripts/_audit_related_media_urls.py`) verifies and prunes every URL
afterwards. Never pay a model to verify a URL.

Usage:
    python scripts/_content_latin-eduqas/media_latin.py submit
    python scripts/_content_latin-eduqas/media_latin.py poll
    python scripts/_content_latin-eduqas/media_latin.py insert
"""
import io
import json
import os
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

STEER = """
SUBJECT STEER — GCSE Latin

Good sources for this subject, all real and easy to verify: the Cambridge
School Classics Project and Cambridge Latin Course materials; the Classical
Association and Classics for All; university outreach channels; museum
collections (British Museum, Ashmolean, Getty, the Vindolanda Trust); the BBC's
Roman history documentaries and In Our Time episodes on Roman authors and
history; Historia Civilis, Toldinstone, Invicta and similar reputable ancient
history channels; the Latinitium, Legonium and Found in Antiquity Latin
channels; Perseus Digital Library and the Dickinson College Commentaries;
Wiktionary and Whitaker's Words for morphology; the Bloomsbury and Oxford
Classical Dictionary online reference pages.

Match the lesson: a lesson on Livy's Hannibal wants material on the Second
Punic War and on Livy; a lesson on Roman slavery wants museum and documentary
material on Roman slavery; a vocabulary or accidence lesson wants Latin
learning channels, flashcard tools and morphology reference tools.

Never invent a video id. If you are not confident a specific video exists,
return the CHANNEL page instead — a channel URL is far more likely to survive
the audit than a guessed video id.
"""


def units_all(plan):
    us = plan.get("article_units", []) + plan.get("practice_units", [])
    return sorted(us, key=lambda u: u["sort_order"])


def stage_submit(cfg):
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    media_doc = D.read(os.path.join(cfg["docs_dir"], "RELATED_MEDIA_PIPELINE.md"))
    system = [{"type": "text", "text":
               "You are the related-media curation agent for StudyVault, a GCSE "
               "revision platform. Follow the pipeline doc below for category "
               "structure, ordering and source guidance. Use web_search (a few "
               "searches) to find REAL, currently-existing content. Do NOT "
               "exhaustively fetch and open every candidate — a downstream "
               "Python auditor verifies and prunes every URL, so your job is "
               "breadth of plausible real candidates, not per-URL verification. "
               "Return slightly MORE than the minimum per category so the "
               "auditor has margin after pruning. Do NOT include a 'Lesson "
               "Podcast' item — the platform injects that separately. Never name "
               "an exam board in a title or description.\n\n"
               + media_doc + "\n" + STEER}]
    existing = {}
    mpath = os.path.join(cfg["run_dir"], "related_media.json")
    if os.path.exists(mpath):
        existing = json.load(io.open(mpath, encoding="utf-8"))
    cl = D.client()
    reqs = []
    for u in units_all(plan):
        for l in u["lessons"]:
            cid = D.lesson_key(u["slug"], l["number"])
            if cid in existing:
                continue
            user = ("SUBJECT: GCSE Latin\nUNIT: %s\nLESSON: %s\nLESSON COVERS: %s\n\n"
                    "Find and return the related media as a JSON object "
                    "{\"related_media\": [{\"category\": ..., \"items\": "
                    "[{\"title\", \"url\", \"description\"}]}]} with categories "
                    "in the canonical order. Provide >=2 per category where "
                    "sensible so >=8 items total survive pruning, covering: "
                    "podcasts, videos/channels, at least one of movies/TV/"
                    "documentaries, and study tools. Plain unicode in titles and "
                    "descriptions, no HTML entities. Once you have candidates, "
                    "STOP searching and output ONLY the JSON."
                    % (u["name"], l["title"], l.get("description", "")))
            reqs.append({"custom_id": cid, "params": {
                "model": D.MODEL_CONTENT, "max_tokens": 10000,
                "tools": [{"type": "web_search_20260209", "name": "web_search",
                           "max_uses": 5}],
                "system": system,
                "messages": [{"role": "user", "content": user}],
            }})
    if not reqs:
        print("nothing to curate")
        return
    batch = cl.messages.batches.create(requests=reqs)
    st = D.load_state(cfg)
    st["media_batch_id"] = batch.id
    D.save_state(cfg, st)
    print("media batch submitted: %s (%d lessons)" % (batch.id, len(reqs)))


def stage_insert(cfg):
    st = D.load_state(cfg)
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    media = json.load(io.open(os.path.join(cfg["run_dir"], "related_media.json"),
                              encoding="utf-8"))
    units = D.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id,slug"
                   % st["subject_id"])
    uid = {u["slug"]: u["id"] for u in units}
    n = 0
    for u in units_all(plan):
        for l in u["lessons"]:
            cid = D.lesson_key(u["slug"], l["number"])
            if cid not in media:
                continue
            rm = json.loads(json.dumps(media[cid]))
            pod = next((c for c in rm if c.get("category") == "Podcasts"), None)
            placeholder = {"url": None, "title": "Lesson Podcast",
                           "description": "Audio overview of this lesson."}
            if pod:
                if not any((i.get("title") == "Lesson Podcast")
                           for i in pod.get("items") or []):
                    pod.setdefault("items", []).insert(0, placeholder)
            else:
                rm.insert(0, {"category": "Podcasts", "items": [placeholder]})
            D.supa(cfg, "PATCH", "/rest/v1/lessons?unit_id=eq.%s&lesson_number=eq.%s"
                   % (uid[u["slug"]], l["number"]), {"related_media": rm})
            n += 1
    print("related_media patched onto %d lessons" % n)


def main():
    cfg = D.load_config(CFG_PATH)
    stage = sys.argv[1] if len(sys.argv) > 1 else "submit"
    if stage == "submit":
        stage_submit(cfg)
    elif stage == "poll":
        D.stage_pollmedia(cfg)
    elif stage == "insert":
        stage_insert(cfg)
    else:
        raise SystemExit("unknown stage " + stage)


if __name__ == "__main__":
    main()
