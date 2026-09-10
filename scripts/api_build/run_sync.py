# -*- coding: utf-8 -*-
"""Synchronous fallback for the Batch-API stages of driver.py.

DO NOT RUN THIS WITHOUT TOM'S EXPLICIT APPROVAL. The Batch API is half price and
is the standing default; Tom's ruling on 8 September 2026 was that a stalled
batch queue is a reason to wait, not a reason to pay double. This module exists
for the case where he decides otherwise, and for the record of how the fallback
works.

The Batch API offers no completion SLA short of 24 hours. On 8 September 2026
the account's batch queue stalled: seven batches from three jobs, 89 requests,
none completing for nearly three hours. This module runs exactly the same
requests through the Messages API with a small thread pool, so a build can
finish when the queue will not move.

It imports driver.py and reuses its request construction, its cost ledger and
its validator, so output contracts and spend accounting are unchanged. The only
differences are that requests run in parallel here rather than in a batch, and
that usage is ledgered at full price (batch=False).

Stages:
  content     — run requests_content.json, validate, record ok/failures
  fix         — re-run validation failures with their violations attached
  factcheck   — the same Opus verification requests stage_factcheck builds
  applyfixes  — apply HIGH/MEDIUM findings from factcheck.json
  media       — the same related-media requests stage_media builds

Usage:
  python scripts/api_build/run_sync.py --config <cfg.json> content
  python scripts/api_build/run_sync.py --config <cfg.json> fix
  python scripts/api_build/run_sync.py --config <cfg.json> factcheck
  python scripts/api_build/run_sync.py --config <cfg.json> applyfixes
  python scripts/api_build/run_sync.py --config <cfg.json> media
"""
import argparse
import io
import json
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import driver  # noqa: E402

WORKERS = 4
_ledger_lock = threading.Lock()


def _run_one(cfg, stage_name, req):
    """One Messages API call for a batch-shaped request. Returns (cid, text)."""
    cl = driver.client()
    params = dict(req["params"])
    with cl.messages.stream(**params) as stream:
        msg = stream.get_final_message()
    with _ledger_lock:
        rec = driver.log_usage(cfg, stage_name, params["model"], req["custom_id"],
                               msg.usage, batch=False)
    text = "".join(b.text for b in msg.content if b.type == "text")
    print("  %-32s in=%6d out=%6d stop=%-12s $%.3f"
          % (req["custom_id"], rec["input_tokens"], rec["output_tokens"],
             msg.stop_reason, driver.cost_of(rec)), flush=True)
    return req["custom_id"], text


def run_all(cfg, stage_name, reqs, out_subdir):
    outd = os.path.join(cfg["run_dir"], out_subdir)
    os.makedirs(outd, exist_ok=True)
    texts, errors = {}, {}
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futures = [ex.submit(_run_one, cfg, stage_name, r) for r in reqs]
        for f, r in zip(futures, reqs):
            try:
                cid, text = f.result()
                texts[cid] = text
                io.open(os.path.join(outd, cid + ".txt"), "w",
                        encoding="utf-8").write(text)
            except Exception as e:
                errors[r["custom_id"]] = str(e)[:200]
                print("  FAILED %s: %s" % (r["custom_id"], str(e)[:160]), flush=True)
    return texts, errors


# ---------------------------------------------------------------- content

def stage_content(cfg):
    st = driver.load_state(cfg)
    reqs = json.load(io.open(os.path.join(cfg["run_dir"], "requests_content.json"),
                             encoding="utf-8"))
    done = set(st.get("content_ok", []))
    reqs = [r for r in reqs if r["custom_id"] not in done]
    if not reqs:
        print("content: nothing to do")
        return
    reqs = [{"custom_id": r["custom_id"], "params": driver.try_structured(r["params"])}
            for r in reqs]
    print("content: %d requests, %d workers" % (len(reqs), WORKERS))
    texts, errors = run_all(cfg, "content", reqs, "raw_content")
    ok, failures = driver.validate_lessons(cfg, texts)
    st = driver.load_state(cfg)
    st["content_ok"] = sorted(set(st.get("content_ok", []) + ok))
    remaining = {k: v for k, v in st.get("content_failures", {}).items()
                 if k not in st["content_ok"]}
    remaining.update(failures)
    st["content_failures"] = remaining
    st["content_errors"] = errors
    st["use_structured"] = True
    driver.save_state(cfg, st)
    print("validated: %d PASS, %d FAIL" % (len(ok), len(failures)))
    for cid, probs in sorted(failures.items()):
        print("  FAIL", cid)
        for p in probs[:6]:
            print("     -", p)


def stage_fix(cfg):
    st = driver.load_state(cfg)
    failures = st.get("content_failures", {})
    errored = list(st.get("content_errors", {}))
    todo = sorted(set(list(failures) + errored))
    if not todo:
        print("fix: nothing to fix")
        return
    reqs = json.load(io.open(os.path.join(cfg["run_dir"], "requests_content.json"),
                             encoding="utf-8"))
    by_id = {r["custom_id"]: r for r in reqs}
    fix_reqs = []
    for cid in todo:
        base = by_id[cid]
        user = base["params"]["messages"][0]["content"]
        parse_only = cid in failures and all(
            p.startswith("JSON parse error") for p in failures[cid])
        if cid in failures and not parse_only:
            raw_path = os.path.join(cfg["run_dir"], "raw_content", cid + ".txt")
            prev = driver.read(raw_path) if os.path.exists(raw_path) else ""
            user += ("\n\nYOUR PREVIOUS ATTEMPT FAILED VALIDATION. Violations:\n- "
                     + "\n- ".join(failures[cid][:12])
                     + "\n\nPrevious attempt JSON (fix the violations, keep everything "
                       "that was already compliant):\n" + prev[:60000]
                     + "\n\nReturn the corrected complete lesson JSON.")
        p = dict(base["params"])
        p["messages"] = [{"role": "user", "content": user}]
        fix_reqs.append({"custom_id": cid, "params": driver.try_structured(p)})
    print("fix: %d requests" % len(fix_reqs))
    texts, errors = run_all(cfg, "content-fix", fix_reqs, "raw_content")
    ok, failures2 = driver.validate_lessons(cfg, texts)
    st = driver.load_state(cfg)
    st["content_ok"] = sorted(set(st.get("content_ok", []) + ok))
    remaining = {k: v for k, v in st.get("content_failures", {}).items() if k not in ok}
    remaining.update(failures2)
    st["content_failures"] = remaining
    st["content_errors"] = errors
    driver.save_state(cfg, st)
    print("after fix: %d total PASS, %d still failing" % (len(st["content_ok"]),
                                                          len(remaining)))
    for cid, probs in sorted(remaining.items()):
        print("  FAIL", cid, probs[:4])


# ---------------------------------------------------------------- factcheck

def _factcheck_requests(cfg):
    """Rebuild exactly the requests driver.stage_factcheck would batch."""
    st = driver.load_state(cfg)
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    lessons_dir = os.path.join(cfg["run_dir"], "lessons")
    rules = driver.assessment_rules_block(cfg)
    scope = cfg.get("scope_statement", "")
    fc_search = cfg.get("factcheck_search_max", 8)
    tools = ([{"type": "web_search_20260209", "name": "web_search",
               "max_uses": fc_search}] if fc_search else [])
    fc_system = driver.FACTCHECK_SYSTEM + (
        "\n\n" + cfg["factcheck_system_extra"] if cfg.get("factcheck_system_extra") else "")
    system = ([{"type": "text", "text": fc_system},
               {"type": "text",
                "text": "SOURCE TEXT (primary authority for quotations):\n\n"
                        + driver.read(cfg["factcheck_context_doc"]),
                "cache_control": {"type": "ephemeral", "ttl": "1h"}}]
              if cfg.get("factcheck_context_doc") else
              [{"type": "text", "text": fc_system,
                "cache_control": {"type": "ephemeral", "ttl": "1h"}}])
    reqs = []
    for cid in st.get("content_ok", []):
        obj = json.load(io.open(os.path.join(lessons_dir, cid + ".json"), encoding="utf-8"))
        payload = {k: obj.get(k) for k in
                   ("content_html", "exam_tip_html", "conclusion_html",
                    "knowledge_checks", "flashcard_questions", "glossary_terms",
                    "practice_questions")}
        user = ("LESSON: %s\nTARGET BOARD: %s GCSE %s — question tariffs on this board: %s\n"
                "%s\n%s%s\n\nFact-check this lesson. Return the findings JSON."
                % (cid, cfg["exam_board"], cfg["subject_name"],
                   " | ".join(plan.get("question_type_names", [])),
                   ("SCOPE FOR THIS UNIT: " + scope) if scope else "",
                   rules, json.dumps(payload, ensure_ascii=False)))
        reqs.append({"custom_id": cid, "params": {
            "model": driver.MODEL_FACTCHECK, "max_tokens": 8000,
            "tools": tools, "system": system,
            "messages": [{"role": "user", "content": user}]}})
    return reqs


def stage_factcheck(cfg):
    reqs = _factcheck_requests(cfg)
    print("factcheck: %d lessons" % len(reqs))
    texts, errors = run_all(cfg, "factcheck", reqs, "raw_factcheck")
    findings = {}
    for cid, text in texts.items():
        try:
            findings[cid] = driver.parse_json_reply(text).get("findings", [])
        except Exception as e:
            findings[cid] = [{"severity": "high", "field": "content_html",
                              "claim": "(parse failure)", "problem": str(e),
                              "correction": ""}]
    if errors:
        print("factcheck errors (rerun these):", errors)
    driver.finish_factcheck(cfg, findings)


# ---------------------------------------------------------------- applyfixes

def stage_applyfixes(cfg):
    st = driver.load_state(cfg)
    report = json.load(io.open(os.path.join(cfg["run_dir"], "factcheck.json"),
                               encoding="utf-8"))
    by_lesson = {}
    for f in report["findings"]:
        if f.get("severity") in ("high", "medium"):
            by_lesson.setdefault(f["lesson"], []).append(f)
    if not by_lesson:
        print("no HIGH/MEDIUM findings — nothing to apply")
        return
    lessons_dir = os.path.join(cfg["run_dir"], "lessons")
    reqs = []
    for cid, fl in sorted(by_lesson.items()):
        obj = json.load(io.open(os.path.join(lessons_dir, cid + ".json"), encoding="utf-8"))
        user = ("Apply ONLY the corrections below to this GCSE %s lesson JSON. "
                "Change nothing else — no rewrites, no restructuring, no new narration IDs "
                "unless a correction forces one. Keep every data-narration-id sequence intact.\n\n"
                "CORRECTIONS:\n%s\n\nLESSON JSON:\n%s\n\n"
                "Return the complete corrected lesson JSON only, no code fences."
                % (cfg["subject_name"], json.dumps(fl, ensure_ascii=False),
                   json.dumps(obj, ensure_ascii=False)))
        p = {"model": driver.MODEL_CONTENT, "max_tokens": 32000,
             "messages": [{"role": "user", "content": user}]}
        reqs.append({"custom_id": cid, "params": driver.try_structured(p)})
    print("applyfixes: %d lessons" % len(reqs))
    texts, errors = run_all(cfg, "applyfixes", reqs, "raw_applyfix")
    ok, failures = driver.validate_lessons(cfg, texts)
    print("applied fixes validated: %d PASS, %d FAIL" % (len(ok), len(failures)))
    for cid, probs in sorted(failures.items()):
        print("  FAIL", cid, probs[:6])
    if errors:
        print("errored:", errors)


# ---------------------------------------------------------------- media

def stage_media(cfg):
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    media_doc = driver.read(os.path.join(cfg["docs_dir"], "RELATED_MEDIA_PIPELINE.md"))
    system = [{"type": "text", "text":
               "You are the related-media curation agent for StudyVault, a GCSE revision "
               "platform. Follow the pipeline doc below for category structure, ordering, "
               "and source guidance. Use web_search (a few searches) to find REAL, "
               "currently-existing content — established podcasts, real YouTube channels/"
               "videos, real films/documentaries on JustWatch UK, BBC Bitesize hub pages. "
               "Do NOT exhaustively fetch and open every candidate — a downstream Python "
               "auditor verifies and prunes every URL, so your job is breadth of plausible "
               "real candidates, not per-URL verification. Return slightly MORE than the "
               "minimum per category so the auditor has margin after pruning. Do NOT "
               "include a 'Lesson Podcast' item — the platform injects that separately.\n\n"
               + media_doc,
               "cache_control": {"type": "ephemeral", "ttl": "1h"}}]
    mpath = os.path.join(cfg["run_dir"], "related_media.json")
    existing = json.load(io.open(mpath, encoding="utf-8")) if os.path.exists(mpath) else {}
    reqs = []
    for u in plan["article_units"]:
        for l in u["lessons"]:
            cid = driver.lesson_key(u["slug"], l["number"])
            if cid in existing:
                continue
            user = ("SUBJECT: GCSE %s\nUNIT: %s\nLESSON: %s\nLESSON COVERS: %s\n\n"
                    "Find and return the related media as a JSON object "
                    "{\"related_media\": [{\"category\": ..., \"items\": [{\"title\", \"url\", "
                    "\"description\"}]}]} with categories in the canonical order. Provide "
                    ">=2 per category where sensible so >=8 items total survive pruning, "
                    "covering: podcasts, videos/channels, at least one of movies/TV/"
                    "documentaries, and study tools. Plain unicode in titles and "
                    "descriptions, no HTML entities. Once you have candidates, STOP "
                    "searching and output ONLY the JSON."
                    % (cfg["subject_name"], u["name"], l["title"], l.get("description", "")))
            reqs.append({"custom_id": cid, "params": {
                "model": driver.MODEL_CONTENT, "max_tokens": 10000,
                "tools": [{"type": "web_search_20260209", "name": "web_search",
                           "max_uses": 5}],
                "system": system,
                "messages": [{"role": "user", "content": user}]}})
    if not reqs:
        print("media: nothing to do")
        return
    print("media: %d lessons" % len(reqs))
    texts, errors = run_all(cfg, "media", reqs, "raw_media")
    media = dict(existing)
    problems = {}
    for cid, text in sorted(texts.items()):
        try:
            rm = driver.parse_json_reply(text)["related_media"]
            n = sum(len(c["items"]) for c in rm)
            cats = {c["category"] for c in rm}
            probs = []
            if n < 6:
                probs.append("only %d items" % n)
            for need in ("Podcasts", "Videos & Channels", "Study Tools"):
                if need not in cats:
                    probs.append("no " + need)
            if not cats & {"Movies", "TV Shows", "Documentaries"}:
                probs.append("no Movies/TV/Docs")
            media[cid] = rm
            if probs:
                problems[cid] = probs
        except Exception as e:
            problems[cid] = ["parse: %s" % e]
    driver.write_json(mpath, media)
    st = driver.load_state(cfg)
    st["media_problems"] = problems
    driver.save_state(cfg, st)
    print("media collected for %d lessons; coverage problems: %s"
          % (len(media), problems or "none"))
    if errors:
        print("errored:", errors)


STAGES = {"content": stage_content, "fix": stage_fix, "factcheck": stage_factcheck,
          "applyfixes": stage_applyfixes, "media": stage_media}


def main():
    global WORKERS
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--workers", type=int, default=WORKERS)
    ap.add_argument("stage", choices=sorted(STAGES))
    args = ap.parse_args()
    WORKERS = args.workers
    cfg = driver.load_config(args.config)
    STAGES[args.stage](cfg)


if __name__ == "__main__":
    main()
