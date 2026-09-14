# -*- coding: utf-8 -*-
"""Edexcel GCSE Statistics (1ST0) — port from AQA Statistics (8382), 14 Sep 2026.

Mixed-format subject: the two article units (planning the enquiry; interpreting
results) go through driver.py's content stages; the three practice units keep
the AQA guided banks (walks, diagrams, verified solutions) and are ADAPTED to
the Edexcel specification lesson by lesson — tier, spec references, wording,
any Edexcel-only item added, any AQA-only item removed — rather than rebuilt.

Stages (in order):
    plan          Opus plan, mixed format, each practice lesson names its AQA source
    plancheck     driver's drift check
    activate      subject + ALL units + lesson shells; settings.practice_units set
    prep | submit | poll | fix | pollfix | factcheck | pollfactcheck |
    unitcheck | applyfixes | pollapplyfixes | media | pollmedia | insertmedia |
    insert                                              (article units, driver)
    practiceprep | practicesubmit | practicepoll | practiceinsert
    heroes | narrate | costs

    python run_stats_edexcel.py --config <cfg.json> <stage>
"""
import argparse
import importlib.util
import io
import json
import os
import re
import subprocess
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
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts"))
_spec = importlib.util.spec_from_file_location("drv", os.path.join(HERE, "driver.py"))
drv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(drv)

import anthropic  # noqa: E402


def _plan(cfg):
    return json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))


# ---------------------------------------------------------------- plan (mixed)

def stage_plan(cfg):
    planning_doc = drv.read(os.path.join(cfg["docs_dir"], "PLANNING_PROMPT.md"))
    system = drv.extract_prompt_section(planning_doc, "## System prompt", "## User message template")
    spec_md = drv.read(cfg["spec_md"])
    aqa_plan = json.load(io.open(cfg["source_plan"], encoding="utf-8"))
    catalog = json.load(io.open(cfg["source_catalog"], encoding="utf-8"))
    existing_plan = {
        "subject": aqa_plan.get("subject"),
        "article_units": [{"slug": u["slug"], "name": u["name"], "subtitle": u.get("subtitle"),
                           "lesson_count": u.get("lesson_count"),
                           "lesson_titles": [l["title"] for l in u.get("lessons", [])]}
                          for u in aqa_plan.get("article_units", [])],
        "practice_units": [{"slug": u["slug"], "name": u["name"], "subtitle": u.get("subtitle"),
                            "lesson_count": u.get("lesson_count"),
                            "lessons": [{"number": l["number"], "title": l["title"],
                                         "spec_references": l.get("spec_references"),
                                         "section_markers": l.get("section_markers")}
                                        for l in u.get("lessons", [])]}
                           for u in aqa_plan.get("practice_units", [])],
        "question_type_names": aqa_plan.get("question_type_names"),
        "practice_input_types": aqa_plan.get("practice_input_types"),
        "teaching_brief": aqa_plan.get("teaching_brief"),
    }
    user = (
        "SUBJECT: %s\nEXAM BOARD: %s\nSPEC CODE: %s\nSCHOOL_ID: null\n"
        "TARGET AUDIENCE: free-tier\n\n<spec>\n%s\n</spec>\n\n"
        "<existing_board_plan>\n%s\n</existing_board_plan>\n\n"
        "<existing_board_lessons>\n%s\n</existing_board_lessons>\n\n"
        "Additional constraints for this build:\n"
        "- Subject slug MUST be %s (board-suffixed, matching %s).\n"
        "- source_subject_slug in every content_transfer block MUST be %s.\n"
        "- This is a MIXED-format subject, mirroring the AQA build: the enquiry-planning and "
        "interpreting-results material is article-format; the diagram, numerical-measures and "
        "probability/distribution material is practice-format. Keep the same split unless the "
        "Edexcel specification forces a change, and say why if it does.\n"
        "- PRACTICE LESSONS ARE PORTED, NOT REBUILT. The AQA practice banks are fully guided and "
        "verified, so every practice lesson in your plan MUST carry \"port_from\": {\"unit_slug\", "
        "\"number\"} naming the AQA lesson whose bank it inherits, plus \"port_changes\": a plain "
        "list of what must change for Edexcel (tier — Edexcel Foundation/Higher per the spec's "
        "tiering column; spec_references in Edexcel's numbering; renamed or added techniques; "
        "anything AQA-only to drop). Where Edexcel assesses a technique AQA does not, add a "
        "practice lesson with \"port_from\": null and a full brief, and say so in gaps. Where "
        "AQA has a technique Edexcel does not assess, leave that lesson out and list it in "
        "unique_to_source.\n"
        "- Every lesson (both formats) carries \"tier\": \"foundation\" | \"higher\" | \"both\" "
        "from the Edexcel specification's own tier marking.\n"
        "- Question type names must be Edexcel's (mark tariffs and command words as the spec "
        "and its sample assessment describe them), not AQA's.\n"
        "Generate the plan JSON."
    ) % (cfg["subject_name"], cfg["exam_board"], cfg["spec_code"], spec_md,
         json.dumps(existing_plan, ensure_ascii=False),
         json.dumps(catalog["lessons"], ensure_ascii=False),
         cfg["slug"], cfg["source_subject_slug"], cfg["source_subject_slug"])
    print("planning call: system %dk chars, user %dk chars" % (len(system) // 1000, len(user) // 1000))
    cl = drv.client()
    with cl.messages.stream(
        model=drv.MODEL_PLAN, max_tokens=40000, thinking={"type": "adaptive"},
        system=[{"type": "text", "text": system}],
        messages=[{"role": "user", "content": [{"type": "text", "text": user}]}],
    ) as stream:
        msg = stream.get_final_message()
    text = "".join(b.text for b in msg.content if b.type == "text")
    io.open(os.path.join(cfg["run_dir"], "plan_raw.txt"), "w", encoding="utf-8").write(text)
    rec = drv.log_usage(cfg, "plan", drv.MODEL_PLAN, "plan", msg.usage)
    print("plan usage: in=%d out=%d stop=%s ($%.3f)" % (rec["input_tokens"], rec["output_tokens"], msg.stop_reason, drv.cost_of(rec)))
    plan = drv.parse_json_reply(text)
    drv.write_json(os.path.join(cfg["run_dir"], "plan.json"), plan)
    a = sum(len(u.get("lessons", [])) for u in plan.get("article_units", []))
    p = sum(len(u.get("lessons", [])) for u in plan.get("practice_units", []))
    print("plan saved: %d article units / %d lessons, %d practice units / %d lessons, gaps: %s"
          % (len(plan.get("article_units", [])), a, len(plan.get("practice_units", [])), p, plan.get("gaps") or "none"))
    for u in plan.get("practice_units", []):
        for l in u["lessons"]:
            print("  practice %s L%d %s <- %s | %s" % (u["slug"], l["number"], l["title"][:45], json.dumps(l.get("port_from")), "; ".join(l.get("port_changes") or [])[:120]))


# ---------------------------------------------------------------- activate (both lists)

def stage_activate(cfg):
    plan = _plan(cfg)
    slug = cfg["slug"]
    if drv.supa(cfg, "GET", "/rest/v1/subjects?slug=eq.%s&select=id" % slug):
        print("ABORT: subject exists — never wipe existing rows"); sys.exit(1)
    units = plan["article_units"] + plan.get("practice_units", [])
    quotes = plan.get("quote_ticker_quotes", [])
    accents = [u["accent"] for u in units] or ["#0369a1"]
    esc = lambda t: t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    items = "".join('<span class="quote-item" style="--q-color: %s;">%s <em>&mdash; %s</em></span>'
                    % (accents[i % len(accents)], esc(q["quote"]), esc(q["author"])) for i, q in enumerate(quotes))
    ticker = '<div class="quote-ticker"><div class="quote-ticker-track">%s%s</div></div>' % (items, items)
    row = {"slug": slug, "name": cfg["subject_name"], "exam_board": cfg["exam_board"],
           "spec_code": cfg["spec_code"], "school_id": None, "status": "live",
           "settings": {"quote_ticker_html": ticker, "mixed_format": True,
                        "practice_units": [u["slug"] for u in plan.get("practice_units", [])],
                        "unit_image_positions": {}}}
    created = drv.supa(cfg, "POST", "/rest/v1/subjects", [row], prefer="return=representation")
    subject_id = created[0]["id"]; print("subject created:", subject_id)
    shells = 0
    for u in sorted(units, key=lambda x: x["sort_order"]):
        unit_row = {"subject_id": subject_id, "slug": u["slug"], "name": u["name"], "subtitle": u.get("subtitle"),
                    "body_class": u.get("body_class"), "accent": u["accent"], "accent_light": u["accent_light"],
                    "accent_badge": u["accent_badge"], "lesson_count": len(u["lessons"]), "sort_order": u["sort_order"]}
        uc = drv.supa(cfg, "POST", "/rest/v1/units", [unit_row], prefer="return=representation")
        rows = [{"unit_id": uc[0]["id"], "lesson_number": l["number"], "title": l["title"],
                 "slug": drv.slugify(l["title"]), "status": "pending_review",
                 "tier": l.get("tier") or "both"} for l in u["lessons"]]
        drv.supa(cfg, "POST", "/rest/v1/lessons", rows); shells += len(rows)
        print("  unit %-38s %d shells" % (u["slug"], len(rows)))
    st = drv.load_state(cfg); st["subject_id"] = subject_id; drv.save_state(cfg, st)
    print("activation complete: %d units, %d shells" % (len(units), shells))


# ---------------------------------------------------------------- practice port

PRACTICE_RULES = """You are adapting a fully built, verified GCSE Statistics practice lesson from the AQA specification (8382) to the Pearson Edexcel specification (1ST0). The AQA bank is the product of a long build: guided walks, method card, tier guides, rendered diagrams (SVG in problem displays), worked examples and solutions that were machine-verified. PRESERVE IT.

Hard rules:
1. Return the COMPLETE practice_data object with the same top-level keys and the same shapes. Do not restructure, do not drop keys, do not rename fields.
2. Do NOT change any problem's numbers, answer, solution, diagram (SVG), tolerance or guided_steps unless a listed port change requires it. A changed answer without a listed reason is an error.
3. Apply ONLY the port changes listed for this lesson: re-tier problems where Edexcel's Foundation/Higher split differs (problem "tier" fields and tier_guides), replace AQA spec references and AQA paper/tariff wording with Edexcel's, rename techniques where Edexcel uses a different name, ADD problems for Edexcel-only content (fully guided, same shape as neighbouring problems, correct arithmetic you have checked), and REMOVE problems for AQA-only content.
4. exam_context and method_card text must describe the Edexcel exam (two papers, Foundation and Higher, tariffs and command words from the specification extract). Never name AQA in student-facing text.
5. Plain unicode in every text field: no HTML entities. No board names other than "Edexcel" where the AQA text named "AQA" in a way that must stay board-specific; prefer "the exam board".
6. Output ONLY the JSON object, no code fences, no commentary."""


def _practice_lessons(plan):
    for u in plan.get("practice_units", []):
        for l in u["lessons"]:
            yield u, l


def stage_practiceprep(cfg):
    plan = _plan(cfg)
    spec_md = drv.read(cfg["spec_md"])
    src_id = cfg["source_subject_id"]
    src_units = {u["slug"]: u["id"] for u in drv.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id,slug" % src_id)}
    reqs = []
    for u, l in _practice_lessons(plan):
        pf = l.get("port_from")
        cid = drv.lesson_key(u["slug"], l["number"])
        if not pf:
            print("NO SOURCE (needs a fresh build):", cid); continue
        rows = drv.supa(cfg, "GET", "/rest/v1/lessons?unit_id=eq.%s&lesson_number=eq.%s&select=practice_data,title,description,tier"
                        % (src_units[pf["unit_slug"]], pf["number"]))
        if not rows or not rows[0].get("practice_data"):
            print("SOURCE HAS NO practice_data:", cid, pf); continue
        src = rows[0]
        user = ("TARGET LESSON: %s — unit %s, lesson %d of %d, tier %s\nDESCRIPTION: %s\n"
                "EDEXCEL SPEC REFERENCES: %s\nSECTION MARKERS: %s\n\n"
                "PORT CHANGES TO APPLY (the only changes allowed):\n%s\n\n"
                "SOURCE (AQA) LESSON: %s (tier %s)\n\nSOURCE practice_data JSON:\n%s\n\n"
                "Return the adapted practice_data JSON object."
                % (l["title"], u["name"], l["number"], len(u["lessons"]), l.get("tier"), l.get("description", ""),
                   json.dumps(l.get("spec_references", []), ensure_ascii=False),
                   json.dumps(l.get("section_markers", []), ensure_ascii=False),
                   "\n".join("- " + c for c in (l.get("port_changes") or ["none: keep the bank as it is; only replace AQA references and paper wording"])),
                   src["title"], src.get("tier"), json.dumps(src["practice_data"], ensure_ascii=False)))
        system = [{"type": "text", "text": PRACTICE_RULES},
                  {"type": "text", "text": "EDEXCEL SPECIFICATION (authority for tiers, references, tariffs, command words):\n<spec>\n" + spec_md + "\n</spec>"}]
        reqs.append({"custom_id": cid, "params": {"model": drv.MODEL_CONTENT, "max_tokens": 40000,
                                                   "system": system, "messages": [{"role": "user", "content": user}]}})
    drv.write_json(os.path.join(cfg["run_dir"], "requests_practice.json"), reqs)
    print("prepped %d practice port requests" % len(reqs))


def stage_practicesubmit(cfg):
    reqs = json.load(io.open(os.path.join(cfg["run_dir"], "requests_practice.json"), encoding="utf-8"))
    cl = drv.client(); st = drv.load_state(cfg)
    batch = cl.messages.batches.create(requests=reqs)
    st["practice_batch_id"] = batch.id; drv.save_state(cfg, st)
    print("practice batch submitted:", batch.id, "requests:", len(reqs))


REQUIRED_PD = ("guided", "method_card", "tier_guides", "topic_links", "exam_context", "problem_bank", "worked_examples")


def _lenient_json(text):
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    i, j = t.find("{"), t.rfind("}")
    t = t[i:j + 1]
    try:
        return json.loads(t)
    except Exception:
        # single backslashes that are not JSON escapes (LaTeX, regex) -> escaped
        t2 = re.sub(r"\\(?![\"\\/bfnrtu])", r"\\\\", t)
        return json.loads(t2)


def _check_pd(pd, src_pd):
    probs = []
    for k in REQUIRED_PD:
        if k not in pd: probs.append("missing key " + k)
    pb = pd.get("problem_bank")
    if not isinstance(pb, dict) or not all(t in pb for t in ("bronze", "silver", "gold")):
        probs.append("problem_bank must hold bronze/silver/gold")
    else:
        n = sum(len(v) for v in pb.values()); n0 = sum(len(v) for v in (src_pd.get("problem_bank") or {}).values())
        if n < max(12, n0 - 6): probs.append("problem count %d vs source %d" % (n, n0))
        for t, lst in pb.items():
            for i, p in enumerate(lst):
                if not isinstance(p, dict) or "display" not in p and "question" not in p and "prompt" not in p:
                    probs.append("%s[%d] lacks a display/question" % (t, i)); break
    blob = json.dumps(pd, ensure_ascii=False)
    src_ents = set(re.findall(r"&[a-z]+;|&#\d+;", json.dumps(src_pd, ensure_ascii=False)))
    new_ents = set(re.findall(r"&[a-z]+;|&#\d+;", blob)) - src_ents
    if new_ents: probs.append("new HTML entities %s" % sorted(new_ents)[:5])
    if re.search(r"\bAQA\b", blob): probs.append("AQA named in student text")
    return probs


def stage_practicepoll(cfg):
    st = drv.load_state(cfg)
    out = drv.collect_batch(cfg, st["practice_batch_id"], "practice", "raw_practice")
    if out is None: return
    texts, errors = out
    plan = _plan(cfg)
    src_id = cfg["source_subject_id"]
    src_units = {u["slug"]: u["id"] for u in drv.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id,slug" % src_id)}
    pdir = os.path.join(cfg["run_dir"], "practice"); os.makedirs(pdir, exist_ok=True)
    os.makedirs(os.path.join(cfg["run_dir"], "raw_practice"), exist_ok=True)
    ok, fail = [], {}
    by_cid = {drv.lesson_key(u["slug"], l["number"]): l for u, l in _practice_lessons(plan)}
    for cid, text in sorted(texts.items()):
        io.open(os.path.join(cfg["run_dir"], "raw_practice", cid + ".txt"), "w", encoding="utf-8").write(text)
        try:
            pd = _lenient_json(text)
        except Exception as e:
            fail[cid] = ["parse: %s" % str(e)[:80]]; continue
        pf = by_cid[cid]["port_from"]
        src = drv.supa(cfg, "GET", "/rest/v1/lessons?unit_id=eq.%s&lesson_number=eq.%s&select=practice_data" % (src_units[pf["unit_slug"]], pf["number"]))[0]["practice_data"]
        probs = _check_pd(pd, src)
        drv.write_json(os.path.join(pdir, cid + ".json"), pd)
        (fail.__setitem__(cid, probs) if probs else ok.append(cid))
    st = drv.load_state(cfg)
    st["practice_ok"] = sorted(set(st.get("practice_ok", [])) | set(ok))
    prev = st.get("practice_failures", {}); prev.update(fail)
    st["practice_failures"] = {k: v for k, v in prev.items() if k not in st["practice_ok"]}
    drv.save_state(cfg, st)
    print("practice validated: %d PASS, %d FAIL" % (len(ok), len(fail)))
    for cid, p in fail.items(): print("  FAIL", cid, p[:4])
    if errors: print("errored:", errors)


def stage_practiceretry(cfg):
    """Resubmit the failed practice ports with thinking disabled (the budget was
    being spent on thinking before the JSON) and a larger output budget."""
    st = drv.load_state(cfg)
    reqs = json.load(io.open(os.path.join(cfg["run_dir"], "requests_practice.json"), encoding="utf-8"))
    failed = set(st.get("practice_failures", {}))
    out = []
    for r in reqs:
        if r["custom_id"] not in failed: continue
        p = dict(r["params"]); p["max_tokens"] = int(os.environ.get("PRACTICE_MAX_TOKENS", "64000")); p["thinking"] = {"type": "disabled"}
        p["messages"] = [{"role": "user", "content": r["params"]["messages"][0]["content"]
                          + "\n\nOutput the JSON COMPACT (no indentation or line breaks between tokens) "
                            "and complete: it must end with the closing brace of the object."}]
        out.append({"custom_id": r["custom_id"], "params": p})
    cl = drv.client(); batch = cl.messages.batches.create(requests=out)
    st["practice_batch_id"] = batch.id; drv.save_state(cfg, st)
    print("practice retry batch submitted:", batch.id, "requests:", sorted(r["custom_id"] for r in out))


def stage_practiceinsert(cfg):
    st = drv.load_state(cfg); plan = _plan(cfg)
    units = {u["slug"]: u["id"] for u in drv.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id,slug" % st["subject_id"])}
    pdir = os.path.join(cfg["run_dir"], "practice"); n = 0
    for u, l in _practice_lessons(plan):
        cid = drv.lesson_key(u["slug"], l["number"])
        if cid not in st.get("practice_ok", []): print("SKIP", cid); continue
        pd = json.load(io.open(os.path.join(pdir, cid + ".json"), encoding="utf-8"))
        drv.supa(cfg, "PATCH", "/rest/v1/lessons?unit_id=eq.%s&lesson_number=eq.%s" % (units[u["slug"]], l["number"]),
                 {"practice_data": pd, "description": l.get("description"), "tier": l.get("tier") or "both", "status": "pending_review"})
        n += 1
    print("practice_data written to %d lessons" % n)


# ---------------------------------------------------------------- heroes / narrate

def stage_heroes(cfg):
    from lib.hero_pipeline import HeroFinder
    st = drv.load_state(cfg)
    units = drv.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id,slug,name&order=sort_order" % st["subject_id"])
    # the AQA sister subject's heroes are the natural reuse pool, still vision-gated
    pool = []
    for u in drv.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id" % cfg["source_subject_id"]):
        for r in drv.supa(cfg, "GET", "/rest/v1/lessons?unit_id=eq.%s&select=title,hero_image_url,hero_image_caption&hero_image_url=not.is.null" % u["id"]):
            pool.append({"url": r["hero_image_url"], "title": r["title"], "caption": r.get("hero_image_caption") or ""})
    finder = HeroFinder(); done = fail = 0
    for u in units:
        for l in drv.supa(cfg, "GET", "/rest/v1/lessons?unit_id=eq.%s&select=id,lesson_number,title,description,hero_image_url&order=lesson_number" % u["id"]):
            if (l.get("hero_image_url") or "").strip(): finder.used.add(l["hero_image_url"]); continue
            res = finder.find(subject_slug=cfg["slug"], subject_name=cfg["subject_name"], unit_slug=u["slug"], unit_name=u["name"],
                              lesson_number=l["lesson_number"], title=l["title"], description=l.get("description") or "", reuse_pool=pool)
            if not res: print("  NO HERO", u["slug"], l["lesson_number"]); fail += 1; continue
            drv.supa(cfg, "PATCH", "/rest/v1/lessons?id=eq.%s" % l["id"], {"hero_image_url": res["url"], "hero_image_alt": res["shows"], "hero_image_caption": res["caption"], "hero_image_position": "center"})
            print("  %s L%02d -> %s" % (u["slug"], l["lesson_number"], res["caption"][:80])); done += 1
    print("heroes: %d assigned, %d failed, %d vision calls" % (done, fail, finder.vision_calls))


def stage_narrate(cfg):
    st = drv.load_state(cfg); plan = _plan(cfg)
    units = {u["slug"]: u["id"] for u in drv.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id,slug" % st["subject_id"])}
    for u in plan["article_units"]:
        for r in drv.supa(cfg, "GET", "/rest/v1/lessons?unit_id=eq.%s&select=id,lesson_number&content_html=not.is.null&order=lesson_number" % units[u["slug"]]):
            print("narrating", u["slug"], r["lesson_number"])
            subprocess.run([sys.executable, os.path.join(REPO, "scripts", "_narrate_single_lesson.py"), r["id"]], check=True)


def _with_all_units(stage):
    """The driver's media stages walk plan["article_units"]; every lesson here
    (practice too) gets curated media, so run them over the merged list."""
    def run(cfg):
        path = os.path.join(cfg["run_dir"], "plan.json")
        plan = json.load(io.open(path, encoding="utf-8"))
        merged = dict(plan); merged["article_units"] = plan["article_units"] + plan.get("practice_units", [])
        drv.write_json(path, merged)
        try:
            stage(cfg)
        finally:
            drv.write_json(path, plan)
    return run


STAGES = dict(drv.STAGES)
STAGES["mediaall"] = _with_all_units(drv.stage_media)
STAGES["insertmediaall"] = _with_all_units(drv.stage_insertmedia)
STAGES.update({"plan": stage_plan, "activate": stage_activate, "practiceprep": stage_practiceprep,
               "practicesubmit": stage_practicesubmit, "practicepoll": stage_practicepoll,
               "practiceinsert": stage_practiceinsert, "practiceretry": stage_practiceretry, "heroes": stage_heroes, "narrate": stage_narrate})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("stage", choices=sorted(STAGES))
    args = ap.parse_args()
    STAGES[args.stage](drv.load_config(args.config))


if __name__ == "__main__":
    main()
