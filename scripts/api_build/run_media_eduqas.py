# -*- coding: utf-8 -*-
"""Eduqas GCSE Media Studies (C680QS) — article build ported from AQA Media
(8572) for the framework, plus SET-PRODUCT lessons the AQA build never had.

Set products are year-bound in this specification (Component 1 newspapers
change from 2028; the print advert, radio and television products changed
for 2027), so every lesson in the plan carries "cohort_years": null (all
students) or a list such as [2027] or [2028, 2029]. The `gate` stage writes
those into subjects.settings.exam_year_lessons, which the site reads (a key
may be a year or a list of years since 14 Sep 2026).

Stages: plan | activate | prep | submit | poll | fix | pollfix | factcheck |
pollfactcheck | unitcheck | applyfixes | pollapplyfixes | insert | media |
pollmedia | insertmedia | heroes | narrate | gate | costs

    python run_media_eduqas.py --config <cfg.json> <stage>
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
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts"))
_spec = importlib.util.spec_from_file_location("drv", os.path.join(HERE, "driver.py"))
drv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(drv)
_s2 = importlib.util.spec_from_file_location("stats", os.path.join(HERE, "run_stats_edexcel.py"))
stats = importlib.util.module_from_spec(_s2)
_s2.loader.exec_module(stats)


def _plan(cfg):
    return json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))


def stage_plan(cfg):
    planning_doc = drv.read(os.path.join(cfg["docs_dir"], "PLANNING_PROMPT.md"))
    system = drv.extract_prompt_section(planning_doc, "## System prompt", "## User message template")
    spec_md = drv.read(cfg["spec_md"])
    aqa_plan = json.load(io.open(cfg["source_plan"], encoding="utf-8"))
    catalog = json.load(io.open(cfg["source_catalog"], encoding="utf-8"))
    existing_plan = {
        "subject": aqa_plan.get("subject"),
        "units": [{"slug": u["slug"], "name": u["name"], "subtitle": u.get("subtitle"), "lesson_count": u.get("lesson_count"),
                   "lesson_titles": [l["title"] for l in u.get("lessons", [])]} for u in aqa_plan.get("article_units", [])],
        "question_type_names": aqa_plan.get("question_type_names"),
        "teaching_brief": aqa_plan.get("teaching_brief"),
    }
    user = (
        "SUBJECT: %s\nEXAM BOARD: %s\nSPEC CODE: %s\nSCHOOL_ID: null\nTARGET AUDIENCE: free-tier\n\n"
        "<spec>\n%s\n</spec>\n\n<existing_board_plan>\n%s\n</existing_board_plan>\n\n"
        "<existing_board_lessons>\n%s\n</existing_board_lessons>\n\n"
        "Additional constraints for this build:\n"
        "- Subject slug MUST be %s (board-suffixed, matching %s).\n"
        "- source_subject_slug in every content_transfer block MUST be %s.\n"
        "- This is an article-format subject.\n"
        "- STRUCTURE: units follow the specification's components and sections, not AQA's four framework units. "
        "Suggested: (1) the theoretical framework in brief (media language, representation, industries, audiences — "
        "port from the AQA lessons, compressed to what Eduqas assesses, no more than 6 lessons); (2) Component 1 "
        "Section A set products — one lesson per set product or matched pair (magazine covers Vogue/GQ; film posters "
        "The Man with the Golden Gun/No Time to Die; newspaper front pages; print advertisements Quality Street/NHS 111); "
        "(3) Component 1 Section B industries and audiences — The Sun, Desert Island Discs, No Time to Die (industry), "
        "Fortnite; (4) Component 2 Section A television — Trigger Point, Man Like Mobeen, Modern Family, and the extract "
        "question; (5) Component 2 Section B music — a lesson for each contemporary option pair (Lizzo/Taylor Swift; "
        "Stormzy/Justin Bieber, with their websites) and one for the 1980s/1990s options (Duran Duran Rio / TLC Waterfalls); "
        "(6) exam technique for Components 1 and 2. Component 3 is NEA: one short lesson on what it asks, no more.\n"
        "- SET PRODUCTS ARE YEAR-BOUND. Read the 'Set products for assessment in ...' tables. Every lesson carries "
        "\"cohort_years\": null when it applies to every current student, or a list of exam years when it applies only to "
        "some. The summer 2026 series has been sat, so the 2025-2026-only products (This Girl Can, The Archers, Luther) are "
        "NOT built. Build the 2027 newspaper front pages (The Guardian 18 January 2022, The Sun 1 January 2021) as a lesson "
        "with cohort_years [2027], and the 2028-onwards front pages (The Guardian 6 May 2025, The Sun 22 March 2025) as a "
        "separate lesson with cohort_years [2028, 2029]. Products set for 2027 onwards with no later change carry null.\n"
        "- Every set-product lesson's must_cover names the product exactly as the specification prints it, with its "
        "date, and teaches it through the framework areas the specification says that section assesses.\n"
        "- Question type names must be this board's (tariffs and command words from the specification's assessment "
        "sections), not AQA's.\n"
        "- The board is never named in student-facing text; lessons say 'the exam board'.\n"
        "Generate the plan JSON."
    ) % (cfg["subject_name"], cfg["exam_board"], cfg["spec_code"], spec_md,
         json.dumps(existing_plan, ensure_ascii=False), json.dumps(catalog["lessons"], ensure_ascii=False),
         cfg["slug"], cfg["source_subject_slug"], cfg["source_subject_slug"])
    print("planning call: system %dk chars, user %dk chars" % (len(system) // 1000, len(user) // 1000))
    cl = drv.client()
    with cl.messages.stream(model=drv.MODEL_PLAN, max_tokens=40000, thinking={"type": "adaptive"},
                            system=[{"type": "text", "text": system}],
                            messages=[{"role": "user", "content": [{"type": "text", "text": user}]}]) as stream:
        msg = stream.get_final_message()
    text = "".join(b.text for b in msg.content if b.type == "text")
    io.open(os.path.join(cfg["run_dir"], "plan_raw.txt"), "w", encoding="utf-8").write(text)
    rec = drv.log_usage(cfg, "plan", drv.MODEL_PLAN, "plan", msg.usage)
    print("plan usage: in=%d out=%d stop=%s ($%.3f)" % (rec["input_tokens"], rec["output_tokens"], msg.stop_reason, drv.cost_of(rec)))
    plan = drv.parse_json_reply(text)
    drv.write_json(os.path.join(cfg["run_dir"], "plan.json"), plan)
    n = sum(len(u.get("lessons", [])) for u in plan.get("article_units", []))
    print("plan saved: %d units, %d lessons, gaps: %s" % (len(plan.get("article_units", [])), n, plan.get("gaps") or "none"))
    for u in plan.get("article_units", []):
        print("UNIT", u["slug"], "|", u["name"])
        for l in u["lessons"]:
            print("   L%d %s | years %s | transfer %s" % (l["number"], l["title"][:60], l.get("cohort_years"),
                  (l.get("content_transfer") or {}).get("transfer_score")))


def stage_gate(cfg):
    plan = _plan(cfg)
    subject = drv.supa(cfg, "GET", "/rest/v1/subjects?slug=eq.%s&school_id=is.null&select=id,settings" % cfg["slug"])[0]
    settings = subject.get("settings") or {}
    ym = dict(settings.get("exam_year_lessons") or {})
    for u in plan["article_units"]:
        for l in u["lessons"]:
            ys = l.get("cohort_years")
            if ys:
                ym["%s/%d" % (u["slug"], l["number"])] = ys if len(ys) > 1 else ys[0]
    settings["exam_year_lessons"] = ym
    drv.supa(cfg, "PATCH", "/rest/v1/subjects?id=eq.%s" % subject["id"], {"settings": settings})
    print("exam_year_lessons now:", json.dumps(ym))


STAGES = dict(drv.STAGES)
STAGES.update({"plan": stage_plan, "gate": stage_gate, "heroes": stats.stage_heroes, "narrate": stats.stage_narrate})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("stage", choices=sorted(STAGES))
    args = ap.parse_args()
    STAGES[args.stage](drv.load_config(args.config))


if __name__ == "__main__":
    main()
