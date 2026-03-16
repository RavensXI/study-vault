"""Batch-generate generic lesson content for the free tier.

Reads lesson plans, generates content via Anthropic API, inserts into Supabase.
Generates diagrams using Gemini (matplotlib for maths/science, concept diagrams for humanities).

Usage:
    python scripts/generate_generic_content.py
    python scripts/generate_generic_content.py --subject maths
    python scripts/generate_generic_content.py --subject english-literature --unit macbeth
    python scripts/generate_generic_content.py --dry-run
"""

import argparse
import io
import json
import os
import re
import sys
import time

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import anthropic
from lib.supabase_client import get_client

MODEL = "claude-sonnet-4-20250514"
SPECS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "specs")

# State file to track progress
STATE_FILE = os.path.join(SCRIPT_DIR, "_generic_content_state.json")


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"completed": []}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def load_generation_prompt():
    path = os.path.join(os.path.dirname(SCRIPT_DIR), "docs", "GENERATION_PROMPT.md")
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_spec_text(spec_file, pages=None):
    """Extract text from a spec PDF."""
    import fitz
    path = os.path.join(SPECS_DIR, spec_file)
    doc = fitz.open(path)
    text = ""
    page_range = pages or range(doc.page_count)
    for p in page_range:
        if p < doc.page_count:
            text += doc[p].get_text()
    doc.close()
    return text


# Spec files and relevant page ranges per subject
SPEC_CONFIG = {
    "science": ("AQA-8464-Combined-Science-Spec.pdf", None),
    "maths": ("Edexcel-1MA1-Maths-Spec.pdf", None),
    "english-language": ("AQA-8700-English-Language-Spec.pdf", None),
    "english-literature": ("AQA-8702-English-Literature-Spec.pdf", None),
}


# ── Subject + unit metadata for auto-setup ───────────────────────────────

def _q(text, author, color):
    return f'<span class="quote-item" style="--q-color: {color};">"{text}" <em>— {author}</em></span>'


def _ticker(quotes):
    items = "".join(quotes)
    return f'<div class="quote-ticker"><div class="quote-ticker-track">{items}{items}</div></div>'


SUBJECT_SETUP = {
    "maths": {
        "color": "#2563eb",
        "image_url": "/images/subject-maths.jpg",
        "quote_ticker_html": _ticker([
            _q("Mathematics is the queen of the sciences.", "Carl Friedrich Gauss", "#2563eb"),
            _q("Pure mathematics is, in its way, the poetry of logical ideas.", "Albert Einstein", "#7c3aed"),
            _q("The only way to learn mathematics is to do mathematics.", "Paul Halmos", "#059669"),
            _q("Mathematics is not about numbers, equations, or algorithms: it is about understanding.", "William Paul Thurston", "#dc2626"),
        ]),
    },
    "science": {
        "color": "#16a34a",
        "image_url": "/images/subject-science.jpg",
        "quote_ticker_html": _ticker([
            _q("The good thing about science is that it's true whether or not you believe in it.", "Neil deGrasse Tyson", "#16a34a"),
            _q("Nothing in life is to be feared, it is only to be understood.", "Marie Curie", "#7c3aed"),
            _q("The important thing is not to stop questioning.", "Albert Einstein", "#dc2626"),
            _q("Science is a way of thinking much more than it is a body of knowledge.", "Carl Sagan", "#059669"),
        ]),
    },
    "english-language": {
        "color": "#1e40af",
        "image_url": "/images/subject-english-lang.jpg",
        "quote_ticker_html": _ticker([
            _q("The limits of my language mean the limits of my world.", "Ludwig Wittgenstein", "#1e40af"),
            _q("Language is the road map of a culture.", "Rita Mae Brown", "#b45309"),
            _q("Write to be understood, speak to be heard, read to grow.", "Lawrence Clark Powell", "#0891b2"),
        ]),
    },
    "english-literature": {
        "color": "#991b1b",
        "image_url": "/images/subject-english-lit.jpg",
        "quote_ticker_html": _ticker([
            _q("A reader lives a thousand lives before he dies.", "George R.R. Martin", "#991b1b"),
            _q("Literature is the most agreeable way of ignoring life.", "Fernando Pessoa", "#be185d"),
            _q("The world is a book, and those who do not travel read only one page.", "Saint Augustine", "#4338ca"),
        ]),
    },
}

# Unit metadata: body_class must match CSS definitions, image per unit
UNIT_SETUP = {
    # Science
    "science/biology-paper-1": {"body_class": "unit-science-1", "accent": "#16a34a", "image_url": "https://images.unsplash.com/photo-1767486366904-ebbfaaefb2ff?w=1080&q=80"},
    "science/biology-paper-2": {"body_class": "unit-science-2", "accent": "#059669"},
    "science/chemistry-paper-1": {"body_class": "unit-science-3", "accent": "#7c3aed", "image_url": "https://images.unsplash.com/photo-1603126857599-f6e157fa2fe6?w=1080&q=80"},
    "science/chemistry-paper-2": {"body_class": "unit-science-4", "accent": "#2563eb", "image_url": "/images/subject-chemistry.jpg"},
    "science/physics-paper-1": {"body_class": "unit-science-5", "accent": "#dc2626"},
    "science/physics-paper-2": {"body_class": "unit-science-6", "accent": "#ea580c", "image_url": "/images/subject-physics.jpg"},
    # Maths
    "maths/number": {"body_class": "unit-maths-1", "accent": "#2563eb", "image_url": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1080&q=80"},
    "maths/algebra": {"body_class": "unit-maths-2", "accent": "#7c3aed", "image_url": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=1080&q=80"},
    "maths/ratio-proportion": {"body_class": "unit-maths-3", "accent": "#059669", "image_url": "https://images.unsplash.com/photo-1596495578065-6e0763fa1178?w=1080&q=80"},
    "maths/geometry": {"body_class": "unit-maths-4", "accent": "#dc2626", "image_url": "https://images.unsplash.com/photo-1509228627152-72ae9ae6848d?w=1080&q=80"},
    "maths/probability": {"body_class": "unit-maths-5", "accent": "#ea580c", "image_url": "https://images.unsplash.com/photo-1596451190630-186aff535bf2?w=1080&q=80"},
    "maths/statistics": {"body_class": "unit-maths-6", "accent": "#0891b2", "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1080&q=80"},
    # English Language — body_class must match CSS (unit-english-language-*, NOT unit-english-lang-*)
    "english-language/paper-1-reading": {"body_class": "unit-english-language-1", "accent": "#1e40af"},
    "english-language/paper-1-writing": {"body_class": "unit-english-language-2", "accent": "#059669"},
    "english-language/paper-2-reading": {"body_class": "unit-english-language-3", "accent": "#b45309"},
    "english-language/paper-2-writing": {"body_class": "unit-english-language-4", "accent": "#0891b2"},
    # English Literature — units 1-5 use unit-english-literature-* (match CSS), units 6-8 use unit-english-lit-*
    "english-literature/macbeth": {"body_class": "unit-english-literature-1", "accent": "#991b1b", "image_url": "https://images.unsplash.com/photo-1508931133503-b1944a4ecdd5?w=1080&q=80"},
    "english-literature/romeo-and-juliet": {"body_class": "unit-english-lit-2", "accent": "#be185d", "image_url": "/images/subject-english-lit.jpg"},
    "english-literature/a-christmas-carol": {"body_class": "unit-english-literature-3", "accent": "#b45309", "image_url": "https://images.unsplash.com/photo-1678013614791-639029940cb0?w=1080&q=80"},
    "english-literature/jekyll-and-hyde": {"body_class": "unit-english-lit-4", "accent": "#4338ca", "image_url": "https://images.unsplash.com/photo-1551269901-5c5e14c25df7?w=1080&q=80"},
    "english-literature/animal-farm": {"body_class": "unit-english-literature-5", "accent": "#15803d", "image_url": "https://upload.wikimedia.org/wikipedia/commons/b/b8/George_Orwell_white_plaque.jpg"},
    "english-literature/an-inspector-calls": {"body_class": "unit-english-lit-6", "accent": "#7c3aed", "image_url": "https://images.unsplash.com/photo-1503095396549-807759245b35?w=1080&q=80"},
    "english-literature/power-and-conflict": {"body_class": "unit-english-lit-7", "accent": "#0891b2", "image_url": "https://images.unsplash.com/photo-1696508367537-7f082f547c14?w=1080&q=80"},
    "english-literature/unseen-poetry": {"body_class": "unit-english-lit-8", "accent": "#dc2626"},
}


def build_lesson_prompt(lesson_title, unit_name, subject_name, exam_board, spec_excerpt, generation_prompt):
    """Build the prompt for generating a single lesson."""
    return f"""You are generating a GCSE revision lesson for a FREE generic revision website.
The content must be based ONLY on the publicly available exam specification — NOT on any school's teaching materials.

SUBJECT: {subject_name}
EXAM BOARD: {exam_board}
UNIT: {unit_name}
LESSON TITLE: {lesson_title}

SPECIFICATION EXCERPT (use this as your source of truth for what content to cover):
{spec_excerpt[:3000]}

{generation_prompt}

Generate the complete lesson content_html for this lesson. Include:
- h2 section headings
- Key fact boxes (div class="key-fact")
- Collapsible sections where appropriate
- data-narration-id attributes on every paragraph/list item (n1, n2, n3, etc.)
- A <!-- DIAGRAM --> placeholder where a diagram would go
- Exam tip (div class="exam-tip")
- Conclusion (div class="conclusion")

Also generate:
1. Six practice questions as a JSON array (each with question, marks, type, answer fields)
2. Five knowledge check questions as a JSON array (each with question, options array, correct index)

Output format — return EXACTLY this JSON structure (no markdown code fences):
{{
  "content_html": "...",
  "exam_tip_html": "...",
  "conclusion_html": "...",
  "practice_questions": [...],
  "knowledge_checks": [...]
}}

The exam_tip_html and conclusion_html should be extracted from the content_html (the content within the exam-tip and conclusion divs). The content_html should still contain them inline.

Write for GCSE students aged 15-16. Accessible language but preserve all key terminology.
For maths/science equations, use KaTeX LaTeX notation: inline \\(...\\), display $$...$$.
"""


def generate_lesson(client, prompt):
    """Call Anthropic API to generate lesson content."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()

    # Try to parse as JSON
    # Find the JSON object in the response
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass

    # Fallback: try to extract content_html from the raw text
    print("  WARNING: Could not parse JSON response, attempting fallback")
    return None


def get_unit_lessons_plan(subject_slug, unit_slug):
    """Get the lesson plan for a specific unit from the plans file."""
    plans_path = os.path.join(SCRIPT_DIR, "_generic_lesson_plans.json")
    with open(plans_path, encoding="utf-8") as f:
        plans = json.load(f)

    for subj in plans.get("subjects", []):
        if subj["slug"] == subject_slug:
            for unit in subj.get("units", []):
                if unit["slug"] == unit_slug:
                    return unit["lessons"]
    return []


# Extra English Lit texts not in the original plan
EXTRA_LIT_UNITS = {
    "romeo-and-juliet": [
        {"number": 1, "title": "Context, Genre and the Prologue"},
        {"number": 2, "title": "Act 1: The Feud and the Party"},
        {"number": 3, "title": "Act 2: The Balcony Scene and Secret Marriage"},
        {"number": 4, "title": "Act 3: Tybalt, Mercutio and Banishment"},
        {"number": 5, "title": "Act 4: The Friar's Plan and the Sleeping Potion"},
        {"number": 6, "title": "Act 5: The Tomb and the Tragedy"},
        {"number": 7, "title": "Characters: Romeo and Juliet"},
        {"number": 8, "title": "Characters: Mercutio, Tybalt and the Nurse"},
        {"number": 9, "title": "Themes: Love, Conflict and Fate"},
        {"number": 10, "title": "Language, Structure and Form"},
    ],
    "jekyll-and-hyde": [
        {"number": 1, "title": "Context: Victorian Society and Duality"},
        {"number": 2, "title": "Chapters 1-3: The Door, the Will and Dr Jekyll"},
        {"number": 3, "title": "Chapters 4-6: The Carew Murder and Incident at the Window"},
        {"number": 4, "title": "Chapters 7-10: The Last Night and Jekyll's Statement"},
        {"number": 5, "title": "Characters: Jekyll and Hyde"},
        {"number": 6, "title": "Characters: Utterson, Lanyon and Enfield"},
        {"number": 7, "title": "Themes: Duality, Repression and Science"},
        {"number": 8, "title": "Language, Structure and Narrative Perspective"},
    ],
    "an-inspector-calls": [
        {"number": 1, "title": "Context: Priestley, 1912 and 1945"},
        {"number": 2, "title": "Act 1: The Engagement and the Inspector Arrives"},
        {"number": 3, "title": "Act 1-2: Sheila and Gerald's Involvement"},
        {"number": 4, "title": "Act 2: Mrs Birling and the Charity Committee"},
        {"number": 5, "title": "Act 3: Eric's Confession and the Inspector's Speech"},
        {"number": 6, "title": "Act 3: The Ending and the Phone Call"},
        {"number": 7, "title": "Characters: The Inspector and Mr Birling"},
        {"number": 8, "title": "Characters: Sheila, Eric, Gerald and Mrs Birling"},
        {"number": 9, "title": "Themes: Responsibility, Class and Gender"},
        {"number": 10, "title": "Language, Structure and Dramatic Devices"},
    ],
}


def ensure_subject_setup(sb, subject):
    """Ensure subject has quote ticker and correct settings."""
    setup = SUBJECT_SETUP.get(subject["slug"])
    if not setup:
        return
    settings = subject.get("settings") or {}
    if settings.get("quote_ticker_html"):
        return  # Already set
    settings["quote_ticker_html"] = setup["quote_ticker_html"]
    sb.table("subjects").update({"settings": settings}).eq("id", subject["id"]).execute()
    print(f"  Set quote ticker for {subject['slug']}")


def ensure_unit_setup(sb, subject_slug, unit):
    """Ensure unit has correct body_class, accent, and image_url."""
    key = f"{subject_slug}/{unit['slug']}"
    setup = UNIT_SETUP.get(key)
    if not setup:
        return
    updates = {}
    if setup.get("body_class") and unit.get("body_class") != setup["body_class"]:
        updates["body_class"] = setup["body_class"]
    if setup.get("accent") and unit.get("accent") != setup["accent"]:
        updates["accent"] = setup["accent"]
        updates["accent_light"] = setup["accent"] + "22"
        updates["accent_badge"] = setup["accent"] + "33"
    if setup.get("image_url") and not unit.get("image_url"):
        updates["image_url"] = setup["image_url"]
    if updates:
        sb.table("units").update(updates).eq("id", unit["id"]).execute()
        print(f"  Updated unit setup: {key} ({', '.join(updates.keys())})")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", help="Only process a specific subject slug")
    parser.add_argument("--unit", help="Only process a specific unit slug")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=999, help="Max lessons to generate")
    args = parser.parse_args()

    sb = get_client()
    client = anthropic.Anthropic()
    state = load_state()
    generation_prompt = load_generation_prompt()

    # Get all generic subjects (school_id IS NULL)
    subjects = sb.table("subjects").select("id, slug, name, exam_board, settings").is_("school_id", "null").execute()
    if not subjects.data:
        print("No generic subjects found!")
        return

    print(f"Found {len(subjects.data)} generic subjects")

    total_generated = 0

    for subject in subjects.data:
        if args.subject and subject["slug"] != args.subject:
            continue

        print(f"\n{'=' * 60}")
        print(f"  {subject['name']} ({subject['exam_board']})")
        print(f"{'=' * 60}")

        # Ensure subject has quote ticker etc.
        ensure_subject_setup(sb, subject)

        # Load spec text
        spec_config = SPEC_CONFIG.get(subject["slug"])
        spec_text = ""
        if spec_config:
            spec_text = load_spec_text(spec_config[0], spec_config[1])
            print(f"  Spec: {len(spec_text)} chars loaded")

        # Get units
        units = sb.table("units").select("id, slug, name, sort_order, body_class, accent, image_url").eq(
            "subject_id", subject["id"]
        ).order("sort_order").execute()

        for unit in (units.data or []):
            if args.unit and unit["slug"] != args.unit:
                continue

            print(f"\n  --- {unit['name']} ---")

            # Ensure unit has correct body_class, accent, image
            ensure_unit_setup(sb, subject["slug"], unit)

            # Get lesson plan
            lessons_plan = get_unit_lessons_plan(subject["slug"], unit["slug"])

            # Check for extra English Lit texts
            if not lessons_plan and unit["slug"] in EXTRA_LIT_UNITS:
                lessons_plan = EXTRA_LIT_UNITS[unit["slug"]]

            if not lessons_plan:
                print(f"  No lesson plan found for {subject['slug']}/{unit['slug']}")
                continue

            for lesson_plan in lessons_plan:
                lesson_key = f"{subject['slug']}/{unit['slug']}/L{lesson_plan['number']:02d}"

                if lesson_key in state["completed"]:
                    print(f"  {lesson_key}: Already done, skipping")
                    continue

                if total_generated >= args.limit:
                    print(f"\n  Reached limit ({args.limit})")
                    return

                print(f"\n  {lesson_key}: {lesson_plan['title']}")

                if args.dry_run:
                    print(f"  [DRY RUN]")
                    total_generated += 1
                    continue

                # Check if lesson already exists in DB
                existing = sb.table("lessons").select("id").eq(
                    "unit_id", unit["id"]
                ).eq("lesson_number", lesson_plan["number"]).execute()
                if existing.data:
                    print(f"  Already in DB, skipping")
                    state["completed"].append(lesson_key)
                    save_state(state)
                    continue

                # Build prompt with spec excerpt relevant to this lesson
                prompt = build_lesson_prompt(
                    lesson_plan["title"],
                    unit["name"],
                    subject["name"],
                    subject["exam_board"],
                    spec_text,
                    generation_prompt,
                )

                # Generate content
                try:
                    result = generate_lesson(client, prompt)
                except Exception as e:
                    print(f"  ERROR: {e}")
                    time.sleep(5)
                    continue

                if not result:
                    print(f"  FAILED: No valid response")
                    continue

                # Insert lesson
                try:
                    lesson_slug = re.sub(r'[^a-z0-9]+', '-', lesson_plan["title"].lower()).strip('-')[:60]
                    sb.table("lessons").insert({
                        "unit_id": unit["id"],
                        "slug": lesson_slug,
                        "lesson_number": lesson_plan["number"],
                        "title": lesson_plan["title"],
                        "content_html": result.get("content_html", ""),
                        "exam_tip_html": result.get("exam_tip_html", ""),
                        "conclusion_html": result.get("conclusion_html", ""),
                        "practice_questions": result.get("practice_questions", []),
                        "knowledge_checks": result.get("knowledge_checks", []),
                        "status": "live",
                    }).execute()
                    print(f"  DONE: Inserted into Supabase")
                except Exception as e:
                    print(f"  DB ERROR: {e}")
                    continue

                state["completed"].append(lesson_key)
                save_state(state)
                total_generated += 1

                # Brief pause to avoid rate limits
                time.sleep(2)

    print(f"\n{'=' * 60}")
    print(f"COMPLETE: Generated {total_generated} lessons")
    print(f"State saved to {STATE_FILE}")


if __name__ == "__main__":
    main()
