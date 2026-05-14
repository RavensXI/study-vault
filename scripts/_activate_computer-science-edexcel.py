"""Phase 2 — Subject activation for Computer Science (Edexcel 1CP2), free tier.

Creates a fresh computer-science-edexcel subject row in Supabase with:
  1. subjects row  (slug, name, exam_board, spec_code, school_id=NULL,
                    color, status='live', settings with quote_ticker_html etc.)
  2. 6 unit rows   (from plan article_units)
  3. 26 lesson shells (status='pending_review')

Idempotent: re-runs skip rows that already exist (by slug). If the subject
row already exists the script STOPS and reports — per the
feedback_dont_wipe_existing_supabase_rows rule. Tom enforces this.

Reads scripts/_plan_computer-science-edexcel.json.
Does NOT touch CSS / index.html / wizard JS — those are separate Phase 2
steps documented below.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

scripts = Path(__file__).resolve().parent
plan = json.loads(
    (scripts / "_plan_computer-science-edexcel.json").read_text(encoding="utf-8")
)
sb = get_client()

SUBJECT_SLUG = plan["subject"]["slug"]   # computer-science-edexcel
SCHOOL_ID = None                          # free tier

# ── Colour palette used for the quote ticker ─────────────────────────────
TICKER_PALETTE = [
    "#0e7490",  # cyan-700 (subject accent)
    "#1d4ed8",  # blue-700
    "#7e22ce",  # purple-800
    "#0f766e",  # teal-700
    "#b91c1c",  # red-700
    "#0369a1",  # sky-700
]


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[''′]", "", s)
    s = re.sub(r"[–—]", "-", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]


def build_quote_ticker(quotes: list) -> str:
    """Build the quote-ticker HTML required by the CSS animation.

    The CSS animation requires:
      <div class="quote-ticker"><div class="quote-ticker-track">
        <span class="quote-item" style="--q-color: ...">...</span>
        ...
      </div></div>

    Quotes are duplicated (full sequence twice) for a seamless loop.
    """
    items = []
    for i, q in enumerate(quotes):
        color = TICKER_PALETTE[i % len(TICKER_PALETTE)]
        items.append(
            f'<span class="quote-item" style="--q-color: {color};">'
            f'{q["quote"]} <em>— {q["author"]}</em></span>'
        )
    # Duplicate full sequence for seamless scroll loop
    items = items + items
    return (
        '<div class="quote-ticker"><div class="quote-ticker-track">'
        + "".join(items)
        + "</div></div>"
    )


# ============================================================ 1. subject row

print(f"=== Activating {SUBJECT_SLUG} ===\n")

existing = (
    sb.table("subjects")
    .select("id, slug, status")
    .eq("slug", SUBJECT_SLUG)
    .is_("school_id", "null")
    .execute()
    .data
)
if existing:
    print(
        f"  STOP: subject row already exists (id={existing[0]['id']}, "
        f"status={existing[0]['status']}). "
        f"Per feedback_dont_wipe_existing_supabase_rows: do NOT delete/re-insert. "
        f"Investigate manually."
    )
    sys.exit(1)

quote_ticker_html = build_quote_ticker(plan.get("quote_ticker_quotes", []))

new_settings = {
    "practice_units": [],                              # article-only subject
    "question_type_names": plan.get("question_type_names", []),
    "quote_ticker_html": quote_ticker_html,
    "has_exam_guides": False,
    "unit_image_positions": {
        u["slug"]: "center center"
        for u in plan["article_units"]
    },
}

subject_payload = {
    "name": plan["subject"]["name"],           # "Computer Science"
    "slug": SUBJECT_SLUG,
    "exam_board": plan["subject"]["exam_board"],  # "Edexcel"
    "spec_code": plan["subject"]["spec_code"],    # "1CP2"
    "school_id": SCHOOL_ID,
    "color": plan["subject"]["target_hero_colour"],  # "#0e7490"
    "is_active": True,
    "status": "live",    # free-tier subject row goes live (memory: feedback_freetier_inserts_at_live)
    "sort_order": 0,
    "settings": new_settings,
}

res = sb.table("subjects").insert(subject_payload).execute()
SUBJECT_ID = res.data[0]["id"]
print(f"  subject row INSERTED: {SUBJECT_ID}")
print(f"  status: live  (lessons will be pending_review)")
print(f"  settings: practice_units=[], {len(new_settings['unit_image_positions'])} unit_image_positions\n")


# ============================================================ 2. units

print(f"--- Inserting {len(plan['article_units'])} units ---")

unit_rows = {}   # slug -> inserted row
for pu in plan["article_units"]:
    # accent_badge from the plan — per feedback_accent_badge_must_be_translucent.md
    # the plan provides hex values like "#155e75" but the CSS convention is <accent>33
    # (translucent alpha). The DB stores the plan value; CSS overrides apply the 33-alpha.
    # We store the plan value so downstream code can derive the translucent badge.
    # Actually: the plan's accent_badge is already a solid hex colour. The translucency
    # rule says the CSS pill background should use <accent>33 not a solid darker hex.
    # We write what the plan says to Supabase (it's used by lesson-loader.js for --accent-badge
    # var). We apply the 33-alpha version in CSS (see Phase 2 CSS step).

    payload = {
        "subject_id": SUBJECT_ID,
        "slug": pu["slug"],
        "name": pu["name"],
        "subtitle": pu["subtitle"],
        "body_class": pu["body_class"],
        "accent": pu["accent"],
        "accent_light": pu["accent_light"],
        "accent_badge": pu["accent_badge"] + "33" if not pu["accent_badge"].endswith("33") else pu["accent_badge"],
        "lesson_count": pu["lesson_count"],
        "sort_order": pu["sort_order"],
        "image_url": None,   # auto-sync trigger fills this from L1 hero in Phase 4
    }
    res = sb.table("units").insert(payload).execute()
    unit_rows[pu["slug"]] = res.data[0]
    print(
        f"  inserted: sort={pu['sort_order']:>2}  "
        f"{pu['slug']:40s} ({pu['lesson_count']} lessons)  "
        f"accent={pu['accent']}"
    )

print(f"\n  Units inserted: {len(unit_rows)}\n")


# ============================================================ 3. lesson shells

print(f"--- Inserting lesson shells ---")

total_inserted = 0
for pu in plan["article_units"]:
    unit_id = unit_rows[pu["slug"]]["id"]
    used_slugs: set[str] = set()
    new_in_unit = 0

    for L in pu["lessons"]:
        n = L["number"]
        title = L["title"].strip()
        description = (L.get("description") or "").strip()[:300]

        base_slug = slugify(title) or f"lesson-{n}"
        slug = base_slug
        i = 2
        while slug in used_slugs:
            slug = f"{base_slug}-{i}"
            i += 1
        used_slugs.add(slug)

        sb.table("lessons").insert(
            {
                "unit_id": unit_id,
                "lesson_number": n,
                "slug": slug,
                "title": title,
                "description": description,
                "status": "pending_review",
                # content fields left NULL — Phase 3 content agents fill them
            }
        ).execute()
        new_in_unit += 1
        total_inserted += 1

    print(
        f"  {pu['slug']:40s} planned={pu['lesson_count']:>2}  "
        f"inserted={new_in_unit:>2}"
    )

print(f"\n  Lesson shells inserted: {total_inserted}\n")


# ============================================================ verify

print("--- Verification ---")
total_in_db = 0
for pu in plan["article_units"]:
    unit_id = unit_rows[pu["slug"]]["id"]
    cnt = (
        sb.table("lessons")
        .select("id", count="exact")
        .eq("unit_id", unit_id)
        .execute()
        .count
    )
    total_in_db += cnt
    status_str = "OK" if cnt == pu["lesson_count"] else f"MISMATCH (expected {pu['lesson_count']})"
    print(f"  {pu['slug']:40s} lessons={cnt:>2}  {status_str}")

expected = sum(u["lesson_count"] for u in plan["article_units"])
print(f"\n  Total lessons in DB: {total_in_db}  /  Expected: {expected}")

if total_in_db == expected:
    print(f"\n=== DB activation complete for {SUBJECT_SLUG} ===")
    print(f"  Subject id : {SUBJECT_ID}")
    print(f"  Units      : {len(unit_rows)}")
    print(f"  Lessons    : {total_in_db}")
    print()
    print("Next steps (manual / separate agents):")
    print("  CSS      : append 6 .unit-computer-science-edexcel-N rules to css/style.css")
    print("  Wizard   : update slugMap + freeSubjectMeta + boardConfig in index.html")
    print("  Browse   : add 'computer-science' entry to BASE_SLUG_BOARDS in js/browse-loader.js")
    print("  Videos   : add 'computer-science-edexcel' to SUBJECT_ORDER in scripts/generate_cinematic_videos.py")
    print("  Verifier : python scripts/_verify_subject_build.py computer-science-edexcel --skip-yt")
else:
    print(f"\n  WARN: row count mismatch ({total_in_db} vs {expected}) — investigate before Phase 3.")
