# -*- coding: utf-8 -*-
"""Rebuild three wrong-route lessons in religious-studies-edexcel Paper 3.

Three free-tier lessons shipped as copies of the Catholic route and are parked
at pending_review:

  paper-3-philosophy-ethics-islam        L5  (was a byte-identical copy of the
                                              Christianity L5 row: Catholic
                                              content, zero Islam)
  paper-3-philosophy-ethics-christianity L4  (Catholic-route content)
  paper-3-philosophy-ethics-christianity L5  (Catholic-route content)

This runner reuses driver.py's content / fact-check / apply stages rather than
re-implementing them. It differs from the driver's own `prep` and `insert` in
exactly two ways, both required here:

  * prep adds a per-lesson ROUTE block. Both Paper 3 routes sit in one spec
    extract, so each request has to be told, in the user message, which route it
    is on and what is out of scope for it. That instruction is what stops the
    Islam lesson drifting back into church teaching.
  * insert patches ONLY the generated content fields. hero_image_url,
    hero_image_alt, hero_image_caption, hero_image_position, related_media,
    youtube_video_id, slug, title and lesson_number are left exactly as they
    are — the hero photograph and the podcast entry in related_media are still
    correct for these lessons, and status stays pending_review for Tom.

Stages:

    python run_rs_edexcel_p3.py --config <cfg.json> prep
    python run_rs_edexcel_p3.py --config <cfg.json> submit
    python run_rs_edexcel_p3.py --config <cfg.json> poll
    python run_rs_edexcel_p3.py --config <cfg.json> fix | pollfix
    python run_rs_edexcel_p3.py --config <cfg.json> factcheck | pollfactcheck
    python run_rs_edexcel_p3.py --config <cfg.json> applyfixes | pollapplyfixes
    python run_rs_edexcel_p3.py --config <cfg.json> insert
    python run_rs_edexcel_p3.py --config <cfg.json> costs
"""
import argparse
import importlib.util
import io
import json
import os
import sys

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("drv", os.path.join(HERE, "driver.py"))
drv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(drv)


# ---------------------------------------------------------------- prep

def stage_prep(cfg):
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    system = drv.shared_system_blocks(cfg, plan)
    # Batch requests run in parallel, so cache markers cost more than they save
    # (see driver.stage_prep). Strip them.
    system = [{k: v for k, v in blk.items() if k != "cache_control"} for blk in system]
    requests = []
    for u in plan["article_units"]:
        for l in u["lessons"]:
            user = (
                "UNIT: %s — %s\nUNIT ACCENT COLOUR: %s\n"
                "LESSON %d of %d: %s\n"
                "PLANNED DESCRIPTION (refine to 60-100 chars if needed): %s\n\n"
                "ROUTE — READ THIS FIRST:\n%s\n\n"
                "SPEC REFERENCES: %s\n"
                "SECTION MARKERS (verbatim specification bullets; they scope THIS "
                "lesson's content and nothing else):\n%s\n\n"
                "THIS LESSON MUST COVER (teaching agenda — every bullet needs real "
                "coverage in content_html):\n%s\n\n"
                "This lesson is a REBUILD of a row that shipped with the wrong "
                "religious route. Generate it fresh from the specification sections "
                "above. Do not carry over anything from another route.\n\n"
                "Generate the complete lesson as a JSON object."
            ) % (u["name"], u.get("subtitle", ""), u.get("accent") or "",
                 l["number"], u.get("lesson_count", len(u["lessons"])), l["title"],
                 l.get("description", ""),
                 l["route"],
                 json.dumps(l.get("spec_references", []), ensure_ascii=False),
                 "\n".join("- " + s for s in l.get("section_markers", [])),
                 "\n".join("- " + s for s in l.get("must_cover", [])))
            requests.append({
                "custom_id": drv.lesson_key(u["slug"], l["number"]),
                "params": {
                    "model": drv.MODEL_CONTENT,
                    "max_tokens": 32000,
                    "system": system,
                    "messages": [{"role": "user", "content": user}],
                },
            })
    drv.write_json(os.path.join(cfg["run_dir"], "requests_content.json"), requests)
    total_sys = sum(len(blk["text"]) for blk in system)
    total_user = sum(len(r["params"]["messages"][0]["content"]) for r in requests)
    print("prepped %d content requests. shared system %dk chars, user msgs %dk chars"
          % (len(requests), total_sys // 1000, total_user // 1000))
    for r in requests:
        print("  ", r["custom_id"])


# ---------------------------------------------------------------- content, sequential

def stage_contentseq(cfg):
    """Run the prepped content requests sequentially instead of through the
    Batch API, and validate them exactly as `poll` would.

    A three-lesson rebuild is not worth a batch queue: the 50% batch discount is
    worth cents at this size, while the queue has been observed sitting for the
    better part of an hour. Sequential also lets the shared 20k-token system
    prefix hit the prompt cache on requests 2 and 3, which claws most of the
    difference back. Writes the same state keys as `poll`, so `factcheck` and
    everything after it are unchanged.
    """
    requests = json.load(io.open(os.path.join(cfg["run_dir"], "requests_content.json"),
                                 encoding="utf-8"))
    cl = drv.client()
    st = drv.load_state(cfg)
    use_structured = st.get("use_structured", True)
    raw_dir = os.path.join(cfg["run_dir"], "raw_content")
    os.makedirs(raw_dir, exist_ok=True)
    texts = {}
    for i, r in enumerate(requests):
        params = dict(r["params"])
        # Cache the shared prefix: sequential requests actually hit it.
        sysblocks = [dict(b) for b in params["system"]]
        sysblocks[-1]["cache_control"] = {"type": "ephemeral", "ttl": "1h"}
        params["system"] = sysblocks
        if use_structured:
            params = drv.try_structured(params)
        print("generating %s (%d/%d)..." % (r["custom_id"], i + 1, len(requests)))
        with cl.messages.stream(**params) as stream:
            msg = stream.get_final_message()
        rec = drv.log_usage(cfg, "content", msg.model, r["custom_id"], msg.usage)
        text = "".join(b.text for b in msg.content if b.type == "text")
        io.open(os.path.join(raw_dir, r["custom_id"] + ".txt"), "w",
                encoding="utf-8").write(text)
        texts[r["custom_id"]] = text
        print("   %d chars, cache_read=%d, $%.3f"
              % (len(text), rec["cache_read"], drv.cost_of(rec)))
    ok, failures = drv.validate_lessons(cfg, texts)
    st = drv.load_state(cfg)
    st["content_ok"] = sorted(ok)
    st["content_failures"] = failures
    st["content_errors"] = {}
    drv.save_state(cfg, st)
    print("validated: %d PASS, %d FAIL" % (len(ok), len(failures)))
    for cid, probs in sorted(failures.items()):
        print("  FAIL", cid)
        for p in probs:
            print("     -", p)


def stage_fixseq(cfg):
    """Sequential equivalent of `fix` + `pollfix`: re-run the failures with the
    validator's complaints appended, then re-validate."""
    st = drv.load_state(cfg)
    failures = st.get("content_failures", {})
    if not failures:
        print("nothing to fix")
        return
    requests = json.load(io.open(os.path.join(cfg["run_dir"], "requests_content.json"),
                                 encoding="utf-8"))
    by_id = {r["custom_id"]: r for r in requests}
    cl = drv.client()
    texts = {}
    for cid, probs in sorted(failures.items()):
        base = by_id[cid]
        prior = json.load(io.open(os.path.join(cfg["run_dir"], "lessons", cid + ".json"),
                                  encoding="utf-8")) if os.path.exists(
            os.path.join(cfg["run_dir"], "lessons", cid + ".json")) else None
        user = base["params"]["messages"][0]["content"]
        if prior is not None:
            user += ("\n\nYOUR PREVIOUS ATTEMPT (below) FAILED VALIDATION. Return the "
                     "SAME lesson with ONLY these violations fixed — do not rewrite "
                     "content that already passed:\n%s\n\nPREVIOUS ATTEMPT:\n%s"
                     % ("\n".join("- " + p for p in probs),
                        json.dumps(prior, ensure_ascii=False)))
        else:
            user += ("\n\nYour previous attempt failed validation:\n%s\nRegenerate, "
                     "obeying every rule." % "\n".join("- " + p for p in probs))
        params = {"model": drv.MODEL_CONTENT, "max_tokens": 32000,
                  "system": base["params"]["system"],
                  "messages": [{"role": "user", "content": user}]}
        if st.get("use_structured", True):
            params = drv.try_structured(params)
        print("fixing %s (%d violations)..." % (cid, len(probs)))
        with cl.messages.stream(**params) as stream:
            msg = stream.get_final_message()
        rec = drv.log_usage(cfg, "content-fix", msg.model, cid, msg.usage)
        texts[cid] = "".join(b.text for b in msg.content if b.type == "text")
        print("   $%.3f" % drv.cost_of(rec))
    ok, failures2 = drv.validate_lessons(cfg, texts)
    st = drv.load_state(cfg)
    st["content_ok"] = sorted(set(st.get("content_ok", [])) | set(ok))
    st["content_failures"] = failures2
    drv.save_state(cfg, st)
    print("after fix: %d PASS, %d FAIL" % (len(ok), len(failures2)))
    for cid, probs in sorted(failures2.items()):
        print("  STILL FAILING", cid)
        for p in probs:
            print("     -", p)


def stage_factcheckseq(cfg):
    """Sequential fact-check: same prompt, same source docs, same output file as
    driver.stage_factcheck, run one lesson at a time so there is no batch queue."""
    st = drv.load_state(cfg)
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    lessons_dir = os.path.join(cfg["run_dir"], "lessons")
    rules = drv.assessment_rules_block(cfg)
    scope = cfg.get("scope_statement", "")
    cl = drv.client()
    findings = {}
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
        system = [{"type": "text", "text": drv.FACTCHECK_SYSTEM},
                  {"type": "text",
                   "text": "SOURCE TEXT (primary authority for quotations):\n\n"
                           + drv.read(cfg["factcheck_context_doc"]),
                   "cache_control": {"type": "ephemeral", "ttl": "1h"}}]
        print("fact-checking %s..." % cid)
        with cl.messages.stream(
            model=drv.MODEL_FACTCHECK, max_tokens=8000,
            tools=[{"type": "web_search_20260209", "name": "web_search", "max_uses": 8}],
            system=system, messages=[{"role": "user", "content": user}],
        ) as stream:
            msg = stream.get_final_message()
        rec = drv.log_usage(cfg, "factcheck", drv.MODEL_FACTCHECK, cid, msg.usage)
        text = "".join(b.text for b in msg.content if b.type == "text")
        io.open(os.path.join(cfg["run_dir"], "factcheck_raw_%s.txt" % cid), "w",
                encoding="utf-8").write(text)
        findings[cid] = drv.parse_json_reply(text).get("findings", [])
        print("   %d findings (%s), %d searches, $%.3f"
              % (len(findings[cid]),
                 ", ".join(sorted({f.get("severity", "?") for f in findings[cid]})) or "clean",
                 rec["web_searches"], drv.cost_of(rec)))
    drv.finish_factcheck(cfg, findings)


def stage_applyfixesseq(cfg):
    """Sequential apply-fixes: same surgical-correction prompt as
    driver.stage_applyfixes, run one lesson at a time, then re-validate."""
    st = drv.load_state(cfg)
    report = json.load(io.open(os.path.join(cfg["run_dir"], "factcheck.json"),
                               encoding="utf-8"))
    by_lesson = {}
    for f in report["findings"]:
        if f.get("severity") in ("high", "medium"):
            by_lesson.setdefault(f["lesson"], []).append(f)
    if not by_lesson:
        print("no HIGH/MEDIUM findings — nothing to apply")
        return
    cl = drv.client()
    lessons_dir = os.path.join(cfg["run_dir"], "lessons")
    texts = {}
    for cid, fl in sorted(by_lesson.items()):
        obj = json.load(io.open(os.path.join(lessons_dir, cid + ".json"), encoding="utf-8"))
        user = ("Apply ONLY the corrections below to this GCSE %s lesson JSON. "
                "Change nothing else — no rewrites, no restructuring, no new narration IDs "
                "unless a correction forces one. Keep every data-narration-id sequence intact.\n\n"
                "CORRECTIONS:\n%s\n\nLESSON JSON:\n%s\n\n"
                "Return the complete corrected lesson JSON only, no code fences."
                % (cfg["subject_name"], json.dumps(fl, ensure_ascii=False),
                   json.dumps(obj, ensure_ascii=False)))
        params = {"model": drv.MODEL_CONTENT, "max_tokens": 32000,
                  "messages": [{"role": "user", "content": user}]}
        if st.get("use_structured", True):
            params = drv.try_structured(params)
        print("applying %d corrections to %s..." % (len(fl), cid))
        with cl.messages.stream(**params) as stream:
            msg = stream.get_final_message()
        rec = drv.log_usage(cfg, "applyfixes", msg.model, cid, msg.usage)
        texts[cid] = "".join(b.text for b in msg.content if b.type == "text")
        print("   $%.3f" % drv.cost_of(rec))
    ok, failures = drv.validate_lessons(cfg, texts)
    print("applied fixes validated: %d PASS, %d FAIL" % (len(ok), len(failures)))
    for cid, probs in sorted(failures.items()):
        print("  FAIL", cid)
        for p in probs:
            print("     -", p)


# ---------------------------------------------------------------- insert

# Only these fields are rewritten. Everything else on the row survives.
PATCH_FIELDS = ("description", "content_html", "exam_tip_html", "conclusion_html",
                "practice_questions", "knowledge_checks", "flashcard_questions",
                "glossary_terms")


def stage_insert(cfg):
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    subject = drv.supa(cfg, "GET",
                       "/rest/v1/subjects?slug=eq.%s&school_id=is.null&select=id"
                       % cfg["subject_slug"])
    subject_id = subject[0]["id"]
    units = drv.supa(cfg, "GET",
                     "/rest/v1/units?subject_id=eq.%s&select=id,slug" % subject_id)
    uid = {u["slug"]: u["id"] for u in units}
    lessons_dir = os.path.join(cfg["run_dir"], "lessons")
    n = 0
    for u in plan["article_units"]:
        for l in u["lessons"]:
            cid = drv.lesson_key(u["slug"], l["number"])
            path = os.path.join(lessons_dir, cid + ".json")
            if not os.path.exists(path):
                print("SKIP (no validated JSON):", cid)
                continue
            obj = json.load(io.open(path, encoding="utf-8"))
            patch = {k: obj[k] for k in PATCH_FIELDS}
            # The row keeps its existing hero, so it keeps its existing caption:
            # the caption must describe the photograph that is actually there.
            patch["status"] = "pending_review"
            # Narration is regenerated after this step, so the old manifest must
            # not survive a shortened or lengthened lesson.
            patch["narration_manifest"] = None
            drv.supa(cfg, "PATCH",
                     "/rest/v1/lessons?unit_id=eq.%s&lesson_number=eq.%s"
                     % (uid[u["slug"]], l["number"]), patch)
            print("patched %s (%d fields, status=pending_review, manifest cleared)"
                  % (cid, len(patch)))
            n += 1
    print("inserted %d lessons" % n)


STAGES = dict(drv.STAGES)
STAGES["prep"] = stage_prep
STAGES["insert"] = stage_insert
STAGES["contentseq"] = stage_contentseq
STAGES["fixseq"] = stage_fixseq
STAGES["factcheckseq"] = stage_factcheckseq
STAGES["applyfixesseq"] = stage_applyfixesseq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("stage", choices=sorted(STAGES))
    args = ap.parse_args()
    cfg = drv.load_config(args.config)
    STAGES[args.stage](cfg)


if __name__ == "__main__":
    main()
