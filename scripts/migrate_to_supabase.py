"""
Migrate all 140 StudyVault lessons + guide pages from static HTML into Supabase.

Parses each lesson HTML with BeautifulSoup, extracts content, questions, narration
manifests, related media, and upserts into Supabase tables.

Usage:
    python scripts/migrate_to_supabase.py              # Full migration
    python scripts/migrate_to_supabase.py --dry-run    # Parse only, no DB writes
    python scripts/migrate_to_supabase.py --validate   # Count check after migration

Env vars required:
    SUPABASE_URL            (project URL)
    SUPABASE_SERVICE_KEY    (service role key — bypasses RLS)
"""

import io
import json
import os
import re
import sys
import glob as globmod

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from bs4 import BeautifulSoup
from supabase import create_client

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# R2 base URLs for asset rewriting
R2_AUDIO_URL = "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev"

# ============================================================
# SCHOOL + SUBJECT + UNIT DEFINITIONS
# ============================================================

SCHOOL = {
    "name": "Unity College",
    "slug": "unity-college",
    "domain": "unity.lancs.sch.uk",
}

SUBJECTS = [
    {
        "slug": "history",
        "name": "History",
        "exam_board": "AQA",
        "spec_code": "8145",
        "color": "#c44536",
        "image_url": "/images/subject-history.jpg",
        "detail": "4 units, 60 lessons",
        "sort_order": 1,
    },
    {
        "slug": "business",
        "name": "Business Studies",
        "exam_board": "Edexcel",
        "spec_code": "1BS0",
        "color": "#0891b2",
        "image_url": "/images/subject-business.jpg",
        "detail": "2 themes, 30 lessons",
        "sort_order": 2,
    },
    {
        "slug": "geography",
        "name": "Geography",
        "exam_board": "AQA",
        "spec_code": "8035",
        "color": "#4f46e5",
        "image_url": "/images/subject-geography.jpg",
        "detail": "2 papers, 40 lessons",
        "sort_order": 3,
    },
    {
        "slug": "sport-science",
        "name": "Sport Science",
        "exam_board": "OCR",
        "spec_code": "R180",
        "color": "#ea580c",
        "image_url": "/images/subject-sport-science.jpg",
        "detail": "1 unit, 10 lessons",
        "sort_order": 4,
    },
]

UNITS = [
    # History
    {
        "subject_slug": "history",
        "slug": "conflict-tension",
        "name": "Conflict & Tension",
        "subtitle": "The Inter-War Years, 1918\u20131939",
        "body_class": "unit-conflict",
        "accent": "#c44536",
        "accent_light": "#fdf2f0",
        "accent_badge": "#fce8e5",
        "lesson_count": 15,
        "sort_order": 1,
        "local_dir": "history/conflict-tension",
    },
    {
        "subject_slug": "history",
        "slug": "health-people",
        "name": "Health & the People",
        "subtitle": "c.1000 to the present day",
        "body_class": "unit-health",
        "accent": "#0d9488",
        "accent_light": "#f0fdfa",
        "accent_badge": "#ccfbf1",
        "lesson_count": 15,
        "sort_order": 2,
        "local_dir": "history/health-people",
    },
    {
        "subject_slug": "history",
        "slug": "elizabethan",
        "name": "Elizabethan England",
        "subtitle": "c.1568\u20131603",
        "body_class": "unit-elizabethan",
        "accent": "#b45309",
        "accent_light": "#fffbeb",
        "accent_badge": "#fef3c7",
        "lesson_count": 15,
        "sort_order": 3,
        "local_dir": "history/elizabethan",
    },
    {
        "subject_slug": "history",
        "slug": "america",
        "name": "America, 1920\u20131973",
        "subtitle": "Opportunity and inequality",
        "body_class": "unit-america",
        "accent": "#2563eb",
        "accent_light": "#eff6ff",
        "accent_badge": "#dbeafe",
        "lesson_count": 15,
        "sort_order": 4,
        "local_dir": "history/america",
    },
    # Business
    {
        "subject_slug": "business",
        "slug": "theme-1",
        "name": "Theme 1: Investigating Small Business",
        "subtitle": None,
        "body_class": "unit-business-1",
        "accent": "#0891b2",
        "accent_light": "#ecfeff",
        "accent_badge": "#cffafe",
        "lesson_count": 15,
        "sort_order": 1,
        "local_dir": "business/theme-1",
    },
    {
        "subject_slug": "business",
        "slug": "theme-2",
        "name": "Theme 2: Building a Business",
        "subtitle": None,
        "body_class": "unit-business-2",
        "accent": "#059669",
        "accent_light": "#ecfdf5",
        "accent_badge": "#d1fae5",
        "lesson_count": 15,
        "sort_order": 2,
        "local_dir": "business/theme-2",
    },
    # Geography
    {
        "subject_slug": "geography",
        "slug": "paper-1",
        "name": "Paper 1: Physical Geography",
        "subtitle": None,
        "body_class": "unit-geography-1",
        "accent": "#4f46e5",
        "accent_light": "#eef2ff",
        "accent_badge": "#e0e7ff",
        "lesson_count": 20,
        "sort_order": 1,
        "local_dir": "geography/paper-1",
    },
    {
        "subject_slug": "geography",
        "slug": "paper-2",
        "name": "Paper 2: Human Geography",
        "subtitle": None,
        "body_class": "unit-geography-2",
        "accent": "#dc2626",
        "accent_light": "#fef2f2",
        "accent_badge": "#fee2e2",
        "lesson_count": 20,
        "sort_order": 2,
        "local_dir": "geography/paper-2",
    },
    # Sport Science
    {
        "subject_slug": "sport-science",
        "slug": "r180",
        "name": "R180: Reducing the Risk of Sports Injuries",
        "subtitle": None,
        "body_class": "unit-sport-science",
        "accent": "#ea580c",
        "accent_light": "#fff7ed",
        "accent_badge": "#ffedd5",
        "lesson_count": 10,
        "sort_order": 1,
        "local_dir": "sport-science/r180",
    },
]


# ============================================================
# JS PARSING HELPERS
# ============================================================

def parse_js_array(html_text, var_name):
    """Extract a window.varName = [...] JS array from HTML and parse to Python list."""
    # Match: window.varName = [ ... ];
    pattern = rf"window\.{var_name}\s*=\s*(\[.*?\]);\s*$"
    match = re.search(pattern, html_text, re.DOTALL | re.MULTILINE)
    if not match:
        return []

    js_text = match.group(1)

    # Convert JS object notation to valid JSON:
    # 1. Unquoted keys like { type: "..." } -> { "type": "..." }
    js_text = re.sub(r'(?<=[{,])\s*(\w+)\s*:', r' "\1":', js_text)

    # 2. Single quotes to double quotes (careful with apostrophes in values)
    # Only convert quotes that are likely string delimiters
    # First, temporarily escape escaped single quotes within double-quoted strings
    # Then handle single-quoted strings
    js_text = re.sub(r"'([^']*)'", lambda m: '"' + m.group(1).replace('"', '\\"') + '"', js_text)

    # 3. Trailing commas before ] or }
    js_text = re.sub(r",\s*([}\]])", r"\1", js_text)

    # 4. Handle unicode escapes like \u2019
    # json.loads handles \uXXXX natively, so no conversion needed

    try:
        return json.loads(js_text)
    except json.JSONDecodeError as e:
        print(f"    WARNING: Failed to parse {var_name}: {e}")
        # Try with demjson3 as fallback if available
        try:
            import demjson3
            return demjson3.decode(match.group(1))
        except ImportError:
            pass
        return []


# ============================================================
# HTML EXTRACTION
# ============================================================

def extract_lesson_data(html_path, unit_local_dir):
    """Extract all data from a lesson HTML file."""
    with open(html_path, "r", encoding="utf-8") as f:
        html_text = f.read()

    soup = BeautifulSoup(html_text, "html.parser")
    data = {}

    # Title
    h1 = soup.select_one(".lesson-header h1")
    if h1:
        data["title"] = h1.get_text(strip=True)
    else:
        # Fallback: <title> tag
        title_tag = soup.find("title")
        data["title"] = title_tag.get_text(strip=True).split(" - ")[0] if title_tag else "Untitled"

    # Lesson number from <span class="lesson-number"> or filename
    lesson_num_el = soup.select_one(".lesson-number")
    if lesson_num_el:
        num_text = lesson_num_el.get_text(strip=True)
        num_match = re.search(r"\d+", num_text)
        data["lesson_number"] = int(num_match.group()) if num_match else 1
    else:
        fname = os.path.basename(html_path)
        num_match = re.search(r"lesson-0*(\d+)", fname)
        data["lesson_number"] = int(num_match.group(1)) if num_match else 1

    data["slug"] = f"lesson-{data['lesson_number']:02d}"

    # Body class + data attributes
    body = soup.find("body")
    data["body_class"] = " ".join(body.get("class", [])) if body else ""
    data["data_unit"] = body.get("data-unit", "") if body else ""
    data["data_lesson"] = body.get("data-lesson", "") if body else ""

    # Content HTML — the main article
    article = soup.select_one("article.study-notes")
    if article:
        data["content_html"] = article.decode_contents()
    else:
        data["content_html"] = ""

    # Exam tip
    exam_tip = soup.select_one(".exam-tip")
    if exam_tip:
        data["exam_tip_html"] = exam_tip.decode_contents()
    else:
        data["exam_tip_html"] = None

    # Conclusion
    conclusion = soup.select_one(".conclusion")
    if conclusion:
        data["conclusion_html"] = conclusion.decode_contents()
    else:
        data["conclusion_html"] = None

    # Hero image
    hero_fig = soup.select_one("figure.lesson-hero-image")
    if hero_fig:
        img = hero_fig.find("img")
        if img:
            src = img.get("src", "")
            # Keep as-is for now — image upload script will rewrite to R2 URLs
            data["hero_image_url"] = src
            data["hero_image_alt"] = img.get("alt", "")
            # Extract object-position from inline style
            style = img.get("style", "")
            pos_match = re.search(r"object-position:\s*([^;]+)", style)
            data["hero_image_position"] = pos_match.group(1).strip() if pos_match else "center 50%"
        caption = hero_fig.find("figcaption")
        data["hero_image_caption"] = caption.get_text(strip=True) if caption else None
    else:
        data["hero_image_url"] = None
        data["hero_image_alt"] = None
        data["hero_image_position"] = "center 50%"
        data["hero_image_caption"] = None

    # Narration manifest (from inline script)
    data["narration_manifest"] = parse_js_array(html_text, "narrationManifest")

    # Practice questions
    data["practice_questions"] = parse_js_array(html_text, "practiceQuestions")

    # Knowledge checks
    data["knowledge_checks"] = parse_js_array(html_text, "knowledgeCheck")

    # Glossary terms — extract from <dfn class="term" data-def="...">
    glossary = []
    for dfn in soup.select("dfn.term[data-def]"):
        glossary.append({
            "term": dfn.get_text(strip=True),
            "definition": dfn.get("data-def", ""),
        })
    data["glossary_terms"] = glossary

    # Diagrams — extract from <figure class="diagram"> img elements
    diagrams = []
    for fig in soup.select("figure.diagram"):
        img = fig.find("img")
        if img:
            diagrams.append({
                "url": img.get("src", ""),
                "alt": img.get("alt", ""),
            })
    data["diagrams"] = diagrams

    # YouTube video ID
    video_iframe = soup.select_one(".sidebar-video iframe, .sidebar-section iframe")
    if video_iframe:
        iframe_src = video_iframe.get("src", "")
        yt_match = re.search(r"youtube\.com/embed/([^?&\"]+)", iframe_src)
        data["youtube_video_id"] = yt_match.group(1) if yt_match else None
    else:
        data["youtube_video_id"] = None

    # Related media — parse sidebar categories
    data["related_media"] = extract_related_media(soup)

    return data


def extract_related_media(soup):
    """Parse the sidebar-media section into structured JSONB."""
    media_section = soup.select_one(".sidebar-media")
    if not media_section:
        return []

    categories = []
    for toggle in media_section.select(".sidebar-collapsible-toggle"):
        # Category name and emoji from the toggle button text
        toggle_text = toggle.get_text(strip=True)
        # Emoji is usually the first character(s)
        emoji = ""
        name = toggle_text
        # Check if first char is emoji (non-ASCII)
        if toggle_text and ord(toggle_text[0]) > 127:
            # Find where the emoji ends and text begins
            i = 0
            while i < len(toggle_text) and (ord(toggle_text[i]) > 127 or toggle_text[i] in "\ufe0f\u200d"):
                i += 1
            emoji = toggle_text[:i].strip()
            name = toggle_text[i:].strip()

        # Get the items container (sibling .sidebar-collapsible-content)
        collapsible = toggle.find_parent(".sidebar-collapsible")
        if not collapsible:
            # Try next sibling
            content = toggle.find_next_sibling()
        else:
            content = collapsible.select_one(".sidebar-collapsible-content")

        items = []
        if content:
            for link in content.select("a.sidebar-media-item"):
                strong = link.find("strong")
                span = link.find("span")
                items.append({
                    "title": strong.get_text(strip=True) if strong else link.get_text(strip=True),
                    "url": link.get("href", ""),
                    "description": span.get_text(strip=True) if span else "",
                })

        if items:
            categories.append({
                "category": name,
                "emoji": emoji,
                "items": items,
            })

    return categories


def extract_guide_page(html_path):
    """Extract content from an exam technique or revision technique guide page."""
    with open(html_path, "r", encoding="utf-8") as f:
        html_text = f.read()

    soup = BeautifulSoup(html_text, "html.parser")

    # Title from <h1> or <title>
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else ""
    if not title:
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True).split(" - ")[0] if title_tag else "Untitled"

    # Content — take the main content area
    article = soup.select_one("article.study-notes, .guide-content, main")
    if article:
        content_html = article.decode_contents()
    else:
        # Fallback: everything in .lesson-content or body
        main = soup.select_one(".lesson-content, main")
        content_html = main.decode_contents() if main else ""

    slug = os.path.splitext(os.path.basename(html_path))[0]

    return {
        "slug": slug,
        "title": title,
        "content_html": content_html,
    }


# ============================================================
# SUPABASE OPERATIONS
# ============================================================

def get_supabase_client():
    """Create Supabase client with service role key."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")

    if not url or not key:
        print("ERROR: Missing SUPABASE_URL or SUPABASE_SERVICE_KEY environment variables.")
        sys.exit(1)

    return create_client(url, key)


def upsert_school(sb, school_data):
    """Create or update the school record. Returns school ID."""
    result = sb.table("schools").upsert(
        school_data, on_conflict="slug"
    ).execute()
    return result.data[0]["id"]


def upsert_subject(sb, subject_data):
    """Create or update a subject. Returns subject ID."""
    result = sb.table("subjects").upsert(
        subject_data, on_conflict="school_id,slug"
    ).execute()
    return result.data[0]["id"]


def upsert_unit(sb, unit_data):
    """Create or update a unit. Returns unit ID."""
    result = sb.table("units").upsert(
        unit_data, on_conflict="subject_id,slug"
    ).execute()
    return result.data[0]["id"]


def upsert_lesson(sb, lesson_data):
    """Create or update a lesson. Returns lesson ID."""
    result = sb.table("lessons").upsert(
        lesson_data, on_conflict="unit_id,lesson_number"
    ).execute()
    return result.data[0]["id"]


def upsert_guide(sb, guide_data):
    """Create or update a guide page. Returns guide ID."""
    result = sb.table("guide_pages").upsert(
        guide_data, on_conflict="subject_id,guide_type,slug"
    ).execute()
    return result.data[0]["id"]


# ============================================================
# MIGRATION PROCESS
# ============================================================

def find_lesson_files(unit_dir):
    """Find all lesson-NN.html files in a directory, sorted by number."""
    pattern = os.path.join(PROJECT_ROOT, unit_dir, "lesson-*.html")
    files = globmod.glob(pattern)
    # Sort by lesson number
    def lesson_num(path):
        m = re.search(r"lesson-0*(\d+)", os.path.basename(path))
        return int(m.group(1)) if m else 0
    return sorted(files, key=lesson_num)


def find_guide_files(subject_dir, guide_type):
    """Find guide page HTML files (excluding index.html)."""
    guide_dir = os.path.join(PROJECT_ROOT, subject_dir, guide_type)
    if not os.path.isdir(guide_dir):
        return []
    files = globmod.glob(os.path.join(guide_dir, "*.html"))
    return [f for f in sorted(files) if os.path.basename(f) != "index.html"]


def run_migration(dry_run=False):
    """Run the full migration."""
    if dry_run:
        print("=== DRY RUN MODE — parsing only, no database writes ===\n")
        sb = None
    else:
        sb = get_supabase_client()

    # Step 1: Create school
    print("Step 1: Creating school record...")
    if not dry_run:
        school_id = upsert_school(sb, SCHOOL)
        print(f"  School ID: {school_id}")
    else:
        school_id = "dry-run-school-id"
        print(f"  [DRY RUN] Would create: {SCHOOL['name']}")

    # Step 2: Create subjects
    print("\nStep 2: Creating subjects...")
    subject_ids = {}
    for subj in SUBJECTS:
        subj_data = {
            "school_id": school_id,
            "slug": subj["slug"],
            "name": subj["name"],
            "exam_board": subj["exam_board"],
            "spec_code": subj["spec_code"],
            "color": subj["color"],
            "image_url": subj["image_url"],
            "detail": subj["detail"],
            "status": "live",
            "is_active": True,
            "sort_order": subj["sort_order"],
        }
        if not dry_run:
            subject_ids[subj["slug"]] = upsert_subject(sb, subj_data)
            print(f"  {subj['name']}: {subject_ids[subj['slug']]}")
        else:
            subject_ids[subj["slug"]] = f"dry-run-{subj['slug']}"
            print(f"  [DRY RUN] {subj['name']}")

    # Step 3: Create units
    print("\nStep 3: Creating units...")
    unit_ids = {}  # keyed by local_dir
    for unit in UNITS:
        unit_data = {
            "subject_id": subject_ids[unit["subject_slug"]],
            "slug": unit["slug"],
            "name": unit["name"],
            "subtitle": unit.get("subtitle"),
            "body_class": unit["body_class"],
            "accent": unit["accent"],
            "accent_light": unit["accent_light"],
            "accent_badge": unit["accent_badge"],
            "lesson_count": unit["lesson_count"],
            "sort_order": unit["sort_order"],
        }
        if not dry_run:
            unit_ids[unit["local_dir"]] = upsert_unit(sb, unit_data)
            print(f"  {unit['name']}: {unit_ids[unit['local_dir']]}")
        else:
            unit_ids[unit["local_dir"]] = f"dry-run-{unit['slug']}"
            print(f"  [DRY RUN] {unit['name']} ({unit['lesson_count']} lessons)")

    # Step 4: Process lessons
    print("\nStep 4: Processing lessons...")
    total_lessons = 0
    total_questions = 0
    total_kc = 0
    total_narration = 0
    errors = []

    for unit in UNITS:
        local_dir = unit["local_dir"]
        unit_id = unit_ids[local_dir]
        lesson_files = find_lesson_files(local_dir)

        print(f"\n  {unit['name']} ({len(lesson_files)} files):")

        for html_path in lesson_files:
            fname = os.path.basename(html_path)
            try:
                lesson_data = extract_lesson_data(html_path, local_dir)

                # Build DB record
                record = {
                    "unit_id": unit_id,
                    "lesson_number": lesson_data["lesson_number"],
                    "slug": lesson_data["slug"],
                    "title": lesson_data["title"],
                    "content_html": lesson_data["content_html"],
                    "exam_tip_html": lesson_data["exam_tip_html"],
                    "conclusion_html": lesson_data["conclusion_html"],
                    "hero_image_url": lesson_data["hero_image_url"],
                    "hero_image_alt": lesson_data["hero_image_alt"],
                    "hero_image_position": lesson_data["hero_image_position"],
                    "hero_image_caption": lesson_data["hero_image_caption"],
                    "narration_manifest": lesson_data["narration_manifest"],
                    "practice_questions": lesson_data["practice_questions"],
                    "knowledge_checks": lesson_data["knowledge_checks"],
                    "glossary_terms": lesson_data["glossary_terms"],
                    "diagrams": lesson_data["diagrams"],
                    "related_media": lesson_data["related_media"],
                    "youtube_video_id": lesson_data["youtube_video_id"],
                    "status": "live",
                }

                if not dry_run:
                    upsert_lesson(sb, record)

                # Stats
                nq = len(lesson_data["practice_questions"])
                nk = len(lesson_data["knowledge_checks"])
                nn = len(lesson_data["narration_manifest"])
                total_lessons += 1
                total_questions += nq
                total_kc += nk
                total_narration += nn

                print(f"    {fname}: {lesson_data['title'][:50]}... "
                      f"({nq}q, {nk}kc, {nn}clips)")

                # Validation warnings
                if nq != 6:
                    print(f"      WARNING: Expected 6 questions, got {nq}")
                if nk != 5:
                    print(f"      WARNING: Expected 5 knowledge checks, got {nk}")
                if nn == 0:
                    print(f"      WARNING: No narration manifest found")

            except Exception as e:
                errors.append((html_path, str(e)))
                print(f"    ERROR: {fname}: {e}")

    # Step 5: Process guide pages
    print("\n\nStep 5: Processing guide pages...")
    total_guides = 0

    subject_dirs = {
        "history": "history",
        "business": "business",
        "geography": "geography",
        "sport-science": "sport-science",
    }

    for subj_slug, subj_dir in subject_dirs.items():
        subject_id = subject_ids[subj_slug]

        for guide_type in ["exam-technique", "revision-technique"]:
            guide_files = find_guide_files(subj_dir, guide_type)
            if not guide_files:
                continue

            print(f"\n  {subj_slug}/{guide_type} ({len(guide_files)} pages):")

            sort_idx = 0
            for gpath in guide_files:
                try:
                    gdata = extract_guide_page(gpath)
                    sort_idx += 1

                    record = {
                        "subject_id": subject_id,
                        "guide_type": guide_type,
                        "slug": gdata["slug"],
                        "title": gdata["title"],
                        "content_html": gdata["content_html"],
                        "sort_order": sort_idx,
                    }

                    if not dry_run:
                        upsert_guide(sb, record)

                    total_guides += 1
                    print(f"    {gdata['slug']}: {gdata['title'][:60]}")

                except Exception as e:
                    errors.append((gpath, str(e)))
                    print(f"    ERROR: {os.path.basename(gpath)}: {e}")

    # Summary
    print(f"\n{'=' * 55}")
    print(f"MIGRATION {'(DRY RUN) ' if dry_run else ''}SUMMARY")
    print(f"{'=' * 55}")
    print(f"Lessons migrated:     {total_lessons}")
    print(f"Practice questions:   {total_questions} ({total_questions / max(total_lessons, 1):.1f}/lesson)")
    print(f"Knowledge checks:     {total_kc} ({total_kc / max(total_lessons, 1):.1f}/lesson)")
    print(f"Narration clips:      {total_narration}")
    print(f"Guide pages:          {total_guides}")
    if errors:
        print(f"\nERRORS: {len(errors)}")
        for path, err in errors:
            print(f"  {path}: {err}")
    else:
        print(f"\nNo errors!")


def run_validation(sb):
    """Validate migration counts."""
    print("Validating migration...\n")

    lessons = sb.table("lessons").select("id", count="exact").execute()
    print(f"Total lessons: {lessons.count}")

    subjects = sb.table("subjects").select("id", count="exact").execute()
    print(f"Total subjects: {subjects.count}")

    units = sb.table("units").select("id", count="exact").execute()
    print(f"Total units: {units.count}")

    guides = sb.table("guide_pages").select("id", count="exact").execute()
    print(f"Total guide pages: {guides.count}")

    # Check each unit
    print("\nPer-unit breakdown:")
    unit_rows = sb.table("units").select("id, name, lesson_count").execute()
    for unit in unit_rows.data:
        actual = sb.table("lessons").select("id", count="exact").eq(
            "unit_id", unit["id"]
        ).execute()
        status = "OK" if actual.count == unit["lesson_count"] else "MISMATCH"
        print(f"  {unit['name']}: {actual.count}/{unit['lesson_count']} [{status}]")


# ============================================================
# MAIN
# ============================================================

def main():
    if "--validate" in sys.argv:
        sb = get_supabase_client()
        run_validation(sb)
    elif "--dry-run" in sys.argv:
        run_migration(dry_run=True)
    else:
        run_migration(dry_run=False)


if __name__ == "__main__":
    main()
