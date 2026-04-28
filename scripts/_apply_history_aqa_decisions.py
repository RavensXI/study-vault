"""Apply Tom's three approved decisions to the History AQA plan:

1. Drop the rotating-site lesson from each British Depth option (1 per option = 4 lessons).
   For Edward I, fold the general Iron Ring castle-programme content into L9 since L10
   conflated general castles with the Caernarfon-specific anchor.

2. Rename two question types ("Source Utility" -> "Source Evaluation",
   "Bullet-Format Essay" -> "Period Essay"); remove "Historic Environment Essay";
   add a generic "Period Argument" 16-marker for British Depth.

3. The slug rename (existing free-tier `history` -> `history-edexcel`) is a DB
   migration handled at activation time, NOT a plan change.

Reads:  scripts/_plan_history-aqa-shell.json + scripts/_plan_history-aqa-{slug}.json (16)
Writes: scripts/_plan_history-aqa.json (master) + per-option JSONs in place.
Backs up unmodified copies to scripts/_archive_pre_decisions/ first.
"""
import json
import shutil
from pathlib import Path

scripts = Path(__file__).resolve().parent
archive = scripts / "_archive_pre_decisions"
archive.mkdir(exist_ok=True)


# Decisions

DROPS = {
    "elizabethan-england": {
        "drop_lesson_numbers": [13],
        "reason": "L13 anchored on The Globe (rotating 2026 site)",
    },
    "norman-england": {
        "drop_lesson_numbers": [13],
        "reason": "L13 anchored on Pevensey Castle (rotating 2026 site)",
    },
    "medieval-england-edward-i": {
        "drop_lesson_numbers": [10],
        "reason": "L10 conflated Iron Ring (general) with Caernarfon (rotating 2026 site)",
        "absorb_into": {
            9: (
                "Also covers the Iron Ring castle programme as the post-conquest "
                "settlement: Beaumaris, Conwy, Caernarfon and Harlech as instruments of "
                "Plantagenet control, polygonal towers, Master James of St George's "
                "designs, the £25,000 build cost. Treat castles as a class of structure, "
                "not as the rotating historic environment site."
            )
        },
    },
    "restoration-england": {
        "drop_lesson_numbers": [12],
        "reason": "L12 anchored on Ham House (rotating 2026 site)",
    },
}

QT_RENAMES = {
    "8 marks — Source Utility": "8 marks — Source Evaluation",
    "12 marks — Source Utility": "12 marks — Source Evaluation",
    "12 marks — Bullet-Format Essay": "12 marks — Period Essay",
}
QT_REMOVE = "16 marks — Historic Environment Essay"
QT_ADD = "16 marks — Period Argument"

CONTENT_AGENT_BANLIST = [
    "How far do you agree",
    "Has X been the main factor",
    "How does Interpretation B differ from Interpretation A?",
    "Write an account of",
    "You could include the following",
    "In what ways were",
    "Has the main factor in",
]


# Helpers

def lesson_num(L):
    return L.get("number") or L.get("lesson_number")


def set_lesson_num(L, n):
    if "number" in L:
        L["number"] = n
    else:
        L["lesson_number"] = n


def update_qt_list(lst, swap_he_to_period_argument):
    if not isinstance(lst, list):
        return lst
    out = []
    had_he = False
    for q in lst:
        if not isinstance(q, str):
            out.append(q)
            continue
        if q == QT_REMOVE:
            had_he = True
            continue
        out.append(QT_RENAMES.get(q, q))
    if swap_he_to_period_argument and had_he and QT_ADD not in out:
        out.append(QT_ADD)
    return out


def walk_replace_qt(obj):
    """Recursively replace question type strings inside any nested structure."""
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k == "suggested_question_types":
                obj[k] = update_qt_list(v, swap_he_to_period_argument=True)
            elif k in ("primary_question_type", "question_type"):
                if isinstance(v, str):
                    if v == QT_REMOVE:
                        obj[k] = QT_ADD
                    else:
                        obj[k] = QT_RENAMES.get(v, v)
            else:
                walk_replace_qt(v)
    elif isinstance(obj, list):
        for item in obj:
            walk_replace_qt(item)


# Backup originals

for f in scripts.glob("_plan_history-aqa*.json"):
    dst = archive / f.name
    if not dst.exists():
        shutil.copy2(f, dst)
print(f"Backed up {len(list(archive.glob('*.json')))} originals to {archive}")

# Update each British Depth plan

per_option_changes = {}
for slug, decision in DROPS.items():
    p = scripts / f"_plan_history-aqa-{slug}.json"
    plan = json.loads(p.read_text(encoding="utf-8"))
    before_n = len(plan["lessons"])

    drop_set = set(decision["drop_lesson_numbers"])
    absorb_into = decision.get("absorb_into") or {}

    # Capture dropped lesson titles for the summary
    dropped_titles = []
    for L in plan["lessons"]:
        if lesson_num(L) in drop_set:
            dropped_titles.append(L.get("title") or L.get("name") or "?")

    # Apply absorption notes BEFORE dropping
    for L in plan["lessons"]:
        n = lesson_num(L)
        if n in absorb_into:
            note = absorb_into[n]
            existing = L.get("absorbed_from_dropped_lesson") or ""
            L["absorbed_from_dropped_lesson"] = (existing + " " + note).strip()
            kt = L.get("key_topics")
            if isinstance(kt, list):
                kt.append(
                    "Iron Ring castle programme as a class of post-conquest "
                    "fortification — Beaumaris, Conwy, Caernarfon, Harlech (no "
                    "single-site focus)"
                )

    # Drop the targeted lessons
    plan["lessons"] = [L for L in plan["lessons"] if lesson_num(L) not in drop_set]

    # Renumber sequentially from 1
    for i, L in enumerate(plan["lessons"], start=1):
        set_lesson_num(L, i)

    # Apply question-type renames inside the option plan
    walk_replace_qt(plan)

    # Strip the historic environment field (we keep the data in the archive in case
    # we revive these lessons later, but the live plan should not advertise the site).
    plan["historic_environment_dropped_for_v1"] = {
        "site_2026": plan.pop("historic_environment_site_2026", None),
        "reason": decision["reason"],
        "dropped_lessons": dropped_titles,
    }

    # Add a content-agent guardrail visible to downstream agents
    plan["content_agent_guardrails_for_he"] = (
        "Do NOT reference the AQA-specified 2026 historic environment site for this "
        "option (e.g. Globe, Pevensey, Caernarfon, Ham House). The site rotates "
        "yearly and we are deferring that content. Period-general castle/theatre/"
        "site content is fine where naturally part of the topic."
    )

    after_n = len(plan["lessons"])
    p.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    per_option_changes[slug] = {
        "before": before_n,
        "after": after_n,
        "dropped": dropped_titles,
    }
    print(f"  {slug}: {before_n} -> {after_n} lessons (dropped: {dropped_titles})")


# Update shell JSON: question types + per-unit lesson_count for British Depth

shell_path = scripts / "_plan_history-aqa-shell.json"
shell = json.loads(shell_path.read_text(encoding="utf-8"))

shell["question_type_names"] = update_qt_list(
    shell["question_type_names"], swap_he_to_period_argument=True
)

for unit in shell["unit_shells"]:
    if unit["slug"] in per_option_changes:
        unit["target_lesson_count"] = per_option_changes[unit["slug"]]["after"]

shell_path.write_text(json.dumps(shell, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nShell updated. Question types: {len(shell['question_type_names'])} entries")
for q in shell["question_type_names"]:
    print(f"  - {q}")


# Re-merge into master plan

def normalize_he(he):
    if isinstance(he, str):
        return he
    if isinstance(he, dict):
        return he.get("site_name") or he.get("name") or he.get("site")
    return None


options = {}
for unit in shell["unit_shells"]:
    slug = unit["slug"]
    options[slug] = json.loads(
        (scripts / f"_plan_history-aqa-{slug}.json").read_text(encoding="utf-8")
    )

article_units = []
all_gaps = []
for unit in shell["unit_shells"]:
    slug = unit["slug"]
    opt = options[slug]
    article_units.append(
        {
            "name": unit["name"],
            "slug": slug,
            "option_code_internal": unit["option_code_internal"],
            "section_key": unit["section_key"],
            "subtitle": unit["subtitle"],
            "body_class": unit["body_class"],
            "accent": unit["accent"],
            "accent_light": unit["accent_light"],
            "accent_badge": unit["accent_badge"],
            "lesson_count": len(opt["lessons"]),
            "sort_order": unit["sort_order"],
            "spec_section_focus": unit["spec_section_focus"],
            "format": "article",
            "historic_environment_dropped_for_v1": opt.get(
                "historic_environment_dropped_for_v1"
            ),
            "content_agent_guardrails_for_he": opt.get(
                "content_agent_guardrails_for_he"
            ),
            "lessons": opt["lessons"],
            "teaching_brief": opt.get("teaching_brief", {}),
            "key_individuals_and_groups": opt.get("key_individuals_and_groups", []),
        }
    )
    for g in opt.get("gaps", []) or []:
        all_gaps.append({"unit_slug": slug, "gap": g})

master = {
    "subject": shell["subject"],
    "section_structure": shell["section_structure"],
    "article_units": article_units,
    "practice_units": [],
    "question_type_names": shell["question_type_names"],
    "subject_level_teaching_brief": shell["subject_level_teaching_brief"],
    "quote_ticker_quotes": shell["quote_ticker_quotes"],
    "content_agent_banlist_aqa_specific": CONTENT_AGENT_BANLIST,
    "v1_scope_note": (
        "16 article units, 210 lessons. British Depth options (Norman, Edward I, "
        "Elizabethan, Restoration) ship without their historic environment "
        "rotating-site lessons or the 16-mark Historic Environment Essay format. "
        "These can be added in a later pass tied to AQA's annual site rotation."
    ),
    "aggregated_gaps": all_gaps,
}

out = scripts / "_plan_history-aqa.json"
out.write_text(json.dumps(master, indent=2, ensure_ascii=False), encoding="utf-8")
size = out.stat().st_size
print(f"\nMaster plan rewritten: {out} ({size:,} bytes)")

# Per-section totals

print("\nPer-section totals after decisions:")
totals = {}
for u in article_units:
    totals.setdefault(u["section_key"], 0)
    totals[u["section_key"]] += u["lesson_count"]
for sec, n in totals.items():
    print(f"  {sec}: {n}")
total_lessons = sum(u["lesson_count"] for u in article_units)
print(f"\n  TOTAL: {total_lessons} lessons across {len(article_units)} units")
