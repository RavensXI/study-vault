# -*- coding: utf-8 -*-
"""Unit add-on runner: append new lessons to an existing unit and/or apply
surgical corrections to its existing lessons, through driver.py's Batch-API
stages. First used 13 Sep 2026 for the Geography Eduqas fieldwork cohort
lessons and the Edexcel Computer Science Python unit (PLS v6 repair + two
new lessons).

Config keys beyond the driver's: subject_slug, unit_slug, corrected_status
(status to leave corrected existing rows at; default keeps the row's own).
Plan lessons carry an optional cohort_year for the `gate` stage.

Stages:
  new lessons ....... prep | submit | poll | fix | pollfix | factcheck |
                      pollfactcheck | applyfixes | pollapplyfixes | insert |
                      heroes | narrate | gate
  corrections ....... (write run/lessons/<unit>-L0X.json + run/factcheck.json
                      first) applyfixes | pollapplyfixes | patch | narrate
"""

import argparse
import importlib.util
import io
import json
import os
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


def _plan(cfg):
    return json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))


def _unit_id(cfg):
    subject = drv.supa(cfg, "GET", "/rest/v1/subjects?slug=eq.%s&school_id=is.null&select=id"
                       % cfg["subject_slug"])
    units = drv.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&slug=eq.%s&select=id"
                     % (subject[0]["id"], cfg["unit_slug"]))
    return subject[0]["id"], units[0]["id"]


# ---------------------------------------------------------------- prep

def stage_prep(cfg):
    plan = _plan(cfg)
    system = drv.shared_system_blocks(cfg, plan)
    system = [{k: v for k, v in blk.items() if k != "cache_control"} for blk in system]
    requests = []
    for u in plan["article_units"]:
        for l in u["lessons"]:
            user = (
                "UNIT: %s — %s\nUNIT ACCENT COLOUR: %s\n"
                "LESSON %d of %d: %s\n"
                "PLANNED DESCRIPTION (refine to 60-100 chars if needed): %s\n\n"
                "COHORT — READ THIS FIRST:\n%s\n\n"
                "SPEC REFERENCES: %s\n"
                "SECTION MARKERS (verbatim specification text; they scope THIS "
                "lesson's content and nothing else):\n%s\n\n"
                "THIS LESSON MUST COVER (teaching agenda — every bullet needs real "
                "coverage in content_html):\n%s\n\n"
                "This is a SHORT companion lesson (about 60-70%% of a normal lesson, "
                "roughly 900-1300 words of teaching in content_html). It sits after "
                "three general lessons on the enquiry cycle, so do not re-teach the "
                "six stages; refer to them. The student's own fieldwork sites and "
                "data are unknown: never invent a class's results, place names or "
                "figures as if real. Illustrate only with the specification's own "
                "example enquiries.\n\n"
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
                    "max_tokens": 24000,
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


# ---------------------------------------------------------------- insert (new rows)

FIELDS = ("description", "content_html", "exam_tip_html", "conclusion_html",
          "practice_questions", "knowledge_checks", "flashcard_questions",
          "glossary_terms")


def stage_insert(cfg):
    plan = _plan(cfg)
    subject_id, unit_id = _unit_id(cfg)
    lessons_dir = os.path.join(cfg["run_dir"], "lessons")
    existing = drv.supa(cfg, "GET", "/rest/v1/lessons?unit_id=eq.%s&select=lesson_number,slug"
                        % unit_id)
    have = {r["lesson_number"] for r in existing}
    slugs = {r["slug"] for r in existing}
    n = 0
    for u in plan["article_units"]:
        for l in u["lessons"]:
            cid = drv.lesson_key(u["slug"], l["number"])
            path = os.path.join(lessons_dir, cid + ".json")
            if not os.path.exists(path):
                print("SKIP (no validated JSON):", cid)
                continue
            if l["number"] in have:
                print("SKIP (row exists — lesson_number %d already in unit):" % l["number"], cid)
                continue
            obj = json.load(io.open(path, encoding="utf-8"))
            slug = drv.slugify(l["title"])[:80]
            if slug in slugs:
                slug += "-%d" % l["number"]
            row = {k: obj[k] for k in FIELDS}
            row.update({
                "unit_id": unit_id,
                "lesson_number": l["number"],
                "slug": slug,
                "title": l["title"],
                "status": "pending_review",
                "tier": "both",
                # the hero and its caption come from the heroes stage, which
                # describes the photograph that actually shipped
                "hero_image_caption": None,
            })
            out = drv.supa(cfg, "POST", "/rest/v1/lessons", row, prefer="return=representation")
            print("inserted %s -> id %s (status=pending_review)" % (cid, out[0]["id"] if out else "?"))
            n += 1
    # the unit card counts live lessons itself; the column is only a fallback
    print("inserted %d new rows" % n)


# ---------------------------------------------------------------- heroes

def stage_heroes(cfg):
    from lib.hero_pipeline import HeroFinder  # noqa: E402
    plan = _plan(cfg)
    subject_id, unit_id = _unit_id(cfg)
    unit = drv.supa(cfg, "GET", "/rest/v1/units?id=eq.%s&select=slug,name" % unit_id)[0]
    numbers = [l["number"] for u in plan["article_units"] for l in u["lessons"]]
    rows = drv.supa(cfg, "GET",
                    "/rest/v1/lessons?unit_id=eq.%s&select=id,lesson_number,title,description,"
                    "hero_image_url&order=lesson_number" % unit_id)
    finder = HeroFinder()
    for r in rows:
        if r.get("hero_image_url"):
            finder.used.add(r["hero_image_url"])
    done = fail = 0
    for r in rows:
        if r["lesson_number"] not in numbers or (r.get("hero_image_url") or "").strip():
            continue
        print("\n  %s L%02d  %s" % (unit["slug"], r["lesson_number"], r["title"]))
        res = finder.find(
            subject_slug=cfg["subject_slug"], subject_name=cfg["subject_name"],
            unit_slug=unit["slug"], unit_name=unit["name"],
            lesson_number=r["lesson_number"], title=r["title"],
            description=r.get("description") or "", reuse_pool=[])
        if not res:
            print("      NO HERO FOUND")
            fail += 1
            continue
        drv.supa(cfg, "PATCH", "/rest/v1/lessons?id=eq.%s" % r["id"], {
            "hero_image_url": res["url"],
            "hero_image_alt": res["shows"],
            "hero_image_caption": res["caption"],
            "hero_image_position": "center",
        })
        print("      -> %s" % res["caption"])
        done += 1
    print("\nheroes: %d assigned, %d failed, %d vision calls"
          % (done, fail, finder.vision_calls))


# ---------------------------------------------------------------- narrate

def stage_narrate(cfg):
    plan = _plan(cfg)
    subject_id, unit_id = _unit_id(cfg)
    st = drv.load_state(cfg)
    numbers = {l["number"] for u in plan["article_units"] for l in u["lessons"]
               if drv.lesson_key(u["slug"], l["number"]) in st.get("content_ok", [])}
    numbers |= {int(c.rsplit("-L", 1)[1]) for c in st.get("patched", [])}
    rows = drv.supa(cfg, "GET", "/rest/v1/lessons?unit_id=eq.%s&select=id,lesson_number"
                    "&lesson_number=in.(%s)" % (unit_id, ",".join(str(n) for n in sorted(numbers))))
    for r in rows:
        print("narrating L%02d %s" % (r["lesson_number"], r["id"]))
        subprocess.run([sys.executable, os.path.join(REPO, "scripts", "_narrate_single_lesson.py"),
                        r["id"]], check=True)


# ---------------------------------------------------------------- gate

def stage_patch(cfg):
    """Write corrected existing lessons back onto their rows (content fields
    only; hero, media, slug, title, ids untouched; narration manifest cleared
    so `narrate` rebuilds it)."""
    st = drv.load_state(cfg)
    report = json.load(io.open(os.path.join(cfg["run_dir"], "factcheck.json"), encoding="utf-8"))
    corrected = sorted({f["lesson"] for f in report["findings"]
                        if f.get("severity") in ("high", "medium")})
    subject_id, unit_id = _unit_id(cfg)
    lessons_dir = os.path.join(cfg["run_dir"], "lessons")
    failures = st.get("content_failures", {})
    n = 0
    for cid in corrected:
        if cid in failures:
            print("SKIP (last validation failed):", cid, failures[cid][:3])
            continue
        num = int(cid.rsplit("-L", 1)[1])
        obj = json.load(io.open(os.path.join(lessons_dir, cid + ".json"), encoding="utf-8"))
        patch = {k: obj[k] for k in FIELDS}
        patch["narration_manifest"] = None
        if cfg.get("corrected_status"):
            patch["status"] = cfg["corrected_status"]
        drv.supa(cfg, "PATCH", "/rest/v1/lessons?unit_id=eq.%s&lesson_number=eq.%d" % (unit_id, num), patch)
        print("patched %s (%d fields, manifest cleared)" % (cid, len(patch)))
        n += 1
    st["patched"] = sorted(set(st.get("patched", [])) | set(corrected))
    drv.save_state(cfg, st)
    print("patched %d existing lessons" % n)


def stage_gate(cfg):
    plan = _plan(cfg)
    subject = drv.supa(cfg, "GET", "/rest/v1/subjects?slug=eq.%s&school_id=is.null&select=id,settings"
                       % cfg["subject_slug"])[0]
    settings = subject.get("settings") or {}
    ym = dict(settings.get("exam_year_lessons") or {})
    for u in plan["article_units"]:
        for l in u["lessons"]:
            if l.get("cohort_year"):
                ym["%s/%d" % (u["slug"], l["number"])] = l["cohort_year"]
    settings["exam_year_lessons"] = ym
    drv.supa(cfg, "PATCH", "/rest/v1/subjects?id=eq.%s" % subject["id"], {"settings": settings})
    print("exam_year_lessons now:", json.dumps(ym))


STAGES = dict(drv.STAGES)
STAGES["prep"] = stage_prep
STAGES["insert"] = stage_insert
STAGES["heroes"] = stage_heroes
STAGES["narrate"] = stage_narrate
STAGES["gate"] = stage_gate
STAGES["patch"] = stage_patch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("stage", choices=sorted(STAGES))
    args = ap.parse_args()
    cfg = drv.load_config(args.config)
    STAGES[args.stage](cfg)


if __name__ == "__main__":
    main()
