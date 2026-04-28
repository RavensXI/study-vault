"""One-off: build a human-readable summary of the History AQA master plan.

Reads scripts/_plan_history-aqa.json and writes scripts/_plan_history-aqa-summary.md.
"""
import json
from pathlib import Path

scripts = Path(__file__).resolve().parent
master = json.loads((scripts / "_plan_history-aqa.json").read_text(encoding="utf-8"))

L = []
L.append("# History (AQA 8145) — Master Plan Summary")
L.append("")
L.append(
    f"**Subject slug:** `{master['subject']['slug']}` · "
    f"**School:** free tier (school_id NULL) · "
    f"**Hero colour:** `{master['subject']['target_hero_colour']}`"
)
L.append("")
L.append("**Total: 214 lessons across 16 units** (within the 195-240 calibration band).")
L.append("")
L.append(
    "Single-planner output is not used — this came from a 1+16 fan-out (one subject-shell call + "
    "16 parallel per-option deep plans). Files: `scripts/_plan_history-aqa-shell.json`, "
    "`scripts/_plan_history-aqa-{slug}.json` × 16, merged into `scripts/_plan_history-aqa.json`."
)
L.append("")
L.append("---")
L.append("")
L.append("## The 16 options at a glance")
L.append("")
L.append("A student picks one from each section. Sort order within each section is set by best-guess uptake (research-led where stats existed, otherwise spec order).")
L.append("")

sec_titles = {
    "paper_1_section_a_period_studies": "Paper 1 Section A — Period Studies (pick 1 of 4)",
    "paper_1_section_b_wider_world_depth": "Paper 1 Section B — Wider World Depth (pick 1 of 5)",
    "paper_2_section_a_thematic": "Paper 2 Section A — Thematic Studies (pick 1 of 3)",
    "paper_2_section_b_british_depth": "Paper 2 Section B — British Depth Studies with Historic Environment (pick 1 of 4)",
}
for sec_key, sec_title in sec_titles.items():
    units = sorted(
        [u for u in master["article_units"] if u["section_key"] == sec_key],
        key=lambda x: x["sort_order"],
    )
    total = sum(u["lesson_count"] for u in units)
    L.append(f"### {sec_title} — {total} lessons")
    L.append("")
    L.append("| # | Option | Slug | Lessons | Accent | HE site (2026) |")
    L.append("|---|--------|------|--------:|--------|----------------|")
    for u in units:
        he = u.get("historic_environment_site_2026") or "—"
        L.append(
            f"| {u['sort_order']} | {u['name']} | `{u['slug']}` | "
            f"{u['lesson_count']} | `{u['accent']}` | {he} |"
        )
    L.append("")

L.append("---")
L.append("")
L.append("## Confirmed 2026 historic environment sites")
L.append("")
L.append("All four sourced from `aqa.org.uk/news/gcse-history-historic-environment-sites-2026-2028`:")
L.append("")
he_units = [u for u in master["article_units"] if u["section_key"] == "paper_2_section_b_british_depth"]
for u in he_units:
    full = u.get("historic_environment_full")
    if isinstance(full, dict):
        site = full.get("site_name") or "?"
        loc = full.get("location") or full.get("country") or ""
        loc_str = f" ({loc})" if loc else ""
    else:
        site = full or "?"
        loc_str = ""
    L.append(f"- **{u['name']}** → {site}{loc_str}")
L.append("")
L.append(
    "Each British depth unit has 2-3 lessons explicitly built around its site, with the 16-mark "
    "Historic Environment Essay anchored on the final or second-to-final lesson."
)
L.append("")

L.append("---")
L.append("")
L.append("## Question types registered")
L.append("")
L.append(
    "Every entry below will need a route in `getGuideUrl()` before content generation. All names "
    "are generic — no AQA spec/paper/component codes."
)
L.append("")
for q in master["question_type_names"]:
    L.append(f"- {q}")
L.append("")
L.append(
    "Period studies lean on the 4-mark interpretation pair, 8-mark Explain Effects, "
    "8-mark Evaluate an Interpretation, and the 12-mark Bullet-Format Essay. Wider world depth "
    "lessons cycle 4-mark Source Analysis, 12-mark Source Utility, 8-mark Narrative Account, "
    "and the 16-mark Source-Based Essay. Thematic uses 4-mark Two Ways Similar/Different, "
    "8-mark Explain Significance, 8-mark Explain a Development, 16-mark Factors Essay. "
    "British depth uses 4-mark Describe Two Features, 8-mark Explain Effects, "
    "8-mark Explain Significance, and the 16-mark Historic Environment Essay (the only place "
    "that one appears)."
)
L.append("")

L.append("---")
L.append("")
L.append("## Subject-wide examiner signals (from the shell)")
L.append("")
for s in master["subject_level_teaching_brief"]["examiner_signals_subject_wide"]:
    L.append(f"- {s['signal']}")
L.append("")

L.append("## Subject-wide misconceptions (top of the brief)")
L.append("")
for m in master["subject_level_teaching_brief"]["common_misconceptions_subject_wide"]:
    L.append(f"- **{m['topic']}** — {m['misconception']}")
L.append("")

L.append("---")
L.append("")
L.append("## Spec changes for 2026")
L.append("")
for c in master["subject_level_teaching_brief"]["spec_changes_2026"]:
    L.append(f"- {c['change']}")
L.append("")

L.append("---")
L.append("")
L.append("## Per-option highlights")
L.append("")
L.append("Pulled from each per-option planner. Detail lives in `scripts/_plan_history-aqa-{slug}.json`.")
L.append("")

for u in sorted(master["article_units"], key=lambda x: x["sort_order"]):
    tb = u.get("teaching_brief", {})
    misc_list = (tb.get("common_misconceptions") or [])[:2]
    hist_list = (tb.get("historiography_notes") or [])[:1]
    L.append(f"### {u['sort_order']}. {u['name']} ({u['lesson_count']} lessons)")
    for m in misc_list:
        if isinstance(m, dict):
            topic = m.get("topic", "?")
            text = (m.get("misconception") or "")[:220]
            L.append(f"- *Misconception:* **{topic}** — {text}")
        elif isinstance(m, str):
            L.append(f"- *Misconception:* {m[:240]}")
    for h in hist_list:
        if isinstance(h, dict):
            view = h.get("view") or h.get("debate") or h.get("note") or "?"
            who = h.get("historian_or_school") or h.get("historians") or h.get("source") or ""
            L.append(f"- *Historiography:* {view}" + (f" ({who})" if who else ""))
        elif isinstance(h, str):
            L.append(f"- *Historiography:* {h[:240]}")
    L.append("")

L.append("---")
L.append("")
L.append(f"## Gaps to review ({len(master['aggregated_gaps'])} entries)")
L.append("")
L.append(
    "Most gap entries are deliberate (out-of-scope notes, paywalled examiner reports, "
    "\"we don't name historians at GCSE\"). Skim for genuine to-decide items:"
)
L.append("")

prev_unit = None
shown = 0
for g in master["aggregated_gaps"]:
    if shown >= 30:
        L.append("")
        L.append(
            f"_(...{len(master['aggregated_gaps']) - shown} more gap entries — see master JSON `aggregated_gaps`)_"
        )
        break
    if g["unit_slug"] != prev_unit:
        L.append("")
        L.append(f"**{g['unit_slug']}:**")
        prev_unit = g["unit_slug"]
    gap = g["gap"]
    if isinstance(gap, dict):
        gap_text = (
            gap.get("issue")
            or gap.get("note")
            or gap.get("description")
            or gap.get("topic")
            or json.dumps(gap, ensure_ascii=False)[:240]
        )
    else:
        gap_text = str(gap)[:240]
    L.append(f"- {gap_text}")
    shown += 1

L.append("")
L.append("---")
L.append("")
L.append("## Files written")
L.append("")
L.append("- `scripts/_plan_history-aqa.json` (552 KB) — master plan, the input for Phase 2 subject activation")
L.append("- `scripts/_plan_history-aqa-shell.json` — subject shell from the first planner pass")
L.append("- `scripts/_plan_history-aqa-{slug}.json` × 16 — per-option deep plans")
L.append("- `scripts/_plan_history-aqa-summary.md` — this document")
L.append("")
L.append("## What I want you to look at first")
L.append("")
L.append(
    "1. The 16 options table above — sort order within each section is opinionated "
    "(Germany first in periods, Inter-War first in wider world, Health first in thematic, "
    "Elizabethan first in British depth). Push back if a different order matches your sense of "
    "school uptake better."
)
L.append(
    "2. Accent palette — every unit has a hex set. Section families are visually grouped "
    "(warm/cool/earthy/regal). Browse `scripts/_plan_history-aqa-shell.json` lines 57-313 to scan."
)
L.append(
    "3. Question types list above — these get hard-coded into `getGuideUrl()` at activation time. "
    "Add or rename if anything reads wrong."
)
L.append(
    "4. Slug — currently `history-aqa`. Existing free-tier Edexcel sits at bare `history`. "
    "Decide whether to rename Edexcel to `history-edexcel` for consistency, or leave the "
    "inconsistency with a doc note."
)
L.append(
    "5. The gap list above — mostly housekeeping but a couple may want your call "
    "(e.g. \"medieval migrants are spec-implied not spec-named\" on the Migration option)."
)
L.append("")
L.append(
    "Once you give the nod, I move to Phase 2 (subject activation) and Phase 3 "
    "(content generation for 214 lessons in parallel batches)."
)

text = "\n".join(L)
out = scripts / "_plan_history-aqa-summary.md"
out.write_text(text, encoding="utf-8")
print(f"Wrote {out} ({len(text):,} chars)")
