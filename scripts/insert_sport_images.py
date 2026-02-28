"""
insert_sport_images.py — Insert hero images and diagram images into Sport Science R180 lesson HTML.

Handles three types:
1. Hero images — between lesson-header and accessibility toolbar
2. Matplotlib diagrams — after the first key-fact block
3. Gemini concept diagrams — before the exam-tip div

Skips insertion if image ref already in HTML or file doesn't exist on disk.

Usage: python insert_sport_images.py
"""

import os
import re
import sys
import json
import html as html_module

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
R180_DIR = os.path.join(PROJECT_ROOT, 'sport-science', 'r180')
ATTRIB_FILE = os.path.join(PROJECT_ROOT, 'sport-science', 'hero_attributions.json')

# ---------- Diagram data ----------
DIAGRAMS = {
    1:  {"mpl": "diagram_extrinsic_factors.jpg",
         "mpl_alt": "Grouped bar chart comparing extrinsic risk factors before and after mitigation"},
    2:  {"mpl": "diagram_intrinsic_factors.jpg",
         "mpl_alt": "Radar chart showing intrinsic risk factor profiles for higher and lower risk athletes"},
    3:  {"mpl": "diagram_warm_up_components.jpg",
         "mpl_alt": "Flow chart of four warm-up components: pulse raiser, mobility, stretching and sport-specific"},
    4:  {"mpl": "diagram_stretching_types.jpg",
         "mpl_alt": "Horizontal bar chart comparing stretching types by effectiveness and injury risk"},
    5:  {"mpl": "diagram_acute_injuries.jpg",
         "mpl_alt": "Matrix grid of six acute sports injuries with symptoms and first treatment"},
    6:  {"mpl": "diagram_chronic_injuries.jpg",
         "mpl_alt": "Bar chart comparing chronic injuries by recovery time and prevalence"},
    7:  {"mpl": "diagram_risk_eap.jpg",
         "mpl_alt": "Dual stepped checklist showing risk assessment and emergency action plan steps"},
    8:  {"mpl": "diagram_treatment_protocols.jpg",
         "mpl_alt": "Three-column stepped process showing SALTAPS, DRABC and PRICE protocols"},
    9:  {"mpl": "diagram_medical_conditions_1.jpg",
         "mpl_alt": "Bar chart of UK prevalence for asthma, diabetes and epilepsy with key actions"},
    10: {"mpl": "diagram_medical_conditions_2.jpg",
         "mpl_alt": "Quadrant matrix of SCA, hypothermia, heat exhaustion and dehydration"},
}

# ---------- Hero alt texts ----------
HERO_ALTS = {
    1:  "Waterlogged football pitch showing environmental risk factors",
    2:  "Athlete performing a hamstring stretch",
    3:  "Football team warming up on the pitch before a match",
    4:  "Runner recovering after a race",
    5:  "Rugby player receiving treatment for an injury",
    6:  "Sports massage and physiotherapy treatment",
    7:  "First aid post at a sports ground",
    8:  "Athlete in a physiotherapy rehabilitation session",
    9:  "Asthma inhaler used for exercise-induced asthma",
    10: "Automated external defibrillator (AED) for use in sports emergencies",
}


def strip_html_tags(text):
    return re.sub(r'<[^>]+>', '', text)


def clean_author(author):
    author = strip_html_tags(author)
    author = re.sub(r'\s*\n\s*', ' ', author)
    author = re.sub(r' {2,}', ' ', author).strip()
    if len(author) > 100:
        for sep in ['.', ',', '/']:
            idx = author.find(sep, 20)
            if 20 < idx < 80:
                author = author[:idx].strip()
                break
        else:
            author = author[:80].strip()
    return author


def escape_html_attr(text):
    return html_module.escape(text, quote=True)


def load_attributions():
    if os.path.exists(ATTRIB_FILE):
        with open(ATTRIB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    print("  [WARN] hero_attributions.json not found — using default captions")
    return {}


def insert_hero_image(html_content, lesson_num, attributions):
    hero_file = f"lesson-{lesson_num:02d}-hero.jpg"
    hero_path = os.path.join(R180_DIR, hero_file)

    if hero_file in html_content:
        return html_content, False
    if not os.path.exists(hero_path):
        return html_content, False

    alt_text = HERO_ALTS.get(lesson_num, "Lesson hero image")
    attr_key = f"r180/{hero_file}"
    attr = attributions.get(attr_key, {})
    author = clean_author(attr.get('author', ''))
    license_text = attr.get('license', '')

    if author and author != 'Unknown':
        caption = f"{alt_text}. Photo: {author} / Wikimedia Commons ({license_text})"
    elif license_text:
        caption = f"{alt_text}. Photo: Wikimedia Commons ({license_text})"
    else:
        caption = f"{alt_text}. Photo: Wikimedia Commons"

    alt_escaped = escape_html_attr(alt_text)
    caption_escaped = html_module.escape(caption)

    hero_html = (
        f'\n      <!-- Hero Image -->\n'
        f'      <figure class="lesson-hero-image">\n'
        f'        <img src="{hero_file}" alt="{alt_escaped}" style="object-position: center 50%;">\n'
        f'        <figcaption>{caption_escaped}</figcaption>\n'
        f'      </figure>\n'
    )

    # Insert after lesson-header closing </h1></div>, before a11y toolbar
    pattern = r'(</h1>\s*</div>)\s*(<!-- Accessibility Toolbar -->|<div class="a11y-toolbar")'
    match = re.search(pattern, html_content)
    if match:
        div_end = match.end(1)
        insert_point = match.start(2)
        html_content = html_content[:div_end] + '\n' + hero_html + '\n      ' + html_content[insert_point:]
        return html_content, True

    # Fallback
    pattern2 = r'(<div class="lesson-header">.*?</div>)\s*(<!-- Accessibility Toolbar -->|<div class="a11y-toolbar")'
    match2 = re.search(pattern2, html_content, re.DOTALL)
    if match2:
        div_end = match2.end(1)
        insert_point = match2.start(2)
        html_content = html_content[:div_end] + '\n' + hero_html + '\n      ' + html_content[insert_point:]
        return html_content, True

    print(f"    [WARN] Could not find insertion point for hero image")
    return html_content, False


def insert_mpl_diagram(html_content, lesson_num):
    info = DIAGRAMS.get(lesson_num, {})
    mpl_file = info.get('mpl')
    if not mpl_file:
        return html_content, False

    if mpl_file in html_content:
        return html_content, False

    mpl_path = os.path.join(R180_DIR, mpl_file)
    if not os.path.exists(mpl_path):
        return html_content, False

    mpl_alt = escape_html_attr(info.get('mpl_alt', ''))

    diagram_html = (
        f'\n        <figure class="diagram">\n'
        f'          <img src="{mpl_file}" alt="{mpl_alt}">\n'
        f'        </figure>\n'
    )

    # Insert after first key-fact block
    key_fact_start = html_content.find('<div class="key-fact"')
    if key_fact_start == -1:
        print(f"    [WARN] No key-fact block found for MPL diagram")
        return html_content, False

    close_pattern = re.compile(r'</p>\s*</div>')
    match = close_pattern.search(html_content, key_fact_start)
    if match:
        insert_pos = match.end()
        html_content = html_content[:insert_pos] + diagram_html + html_content[insert_pos:]
        return html_content, True

    print(f"    [WARN] Could not find key-fact closing for MPL diagram")
    return html_content, False


def insert_gemini_diagram(html_content, lesson_num):
    # Gemini concept images removed — no longer used for Sport Science
    return html_content, False

    print(f"    [WARN] Could not find exam-tip div for Gemini diagram")
    return html_content, False


def process_lesson(lesson_num, attributions):
    filename = f"lesson-{lesson_num:02d}.html"
    filepath = os.path.join(R180_DIR, filename)

    if not os.path.exists(filepath):
        print(f"  [WARN] {filename} not found, skipping")
        return {"hero": 0, "mpl": 0, "gemini": 0}

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    counts = {"hero": 0, "mpl": 0, "gemini": 0}
    original = html

    html, inserted = insert_hero_image(html, lesson_num, attributions)
    if inserted:
        counts["hero"] = 1

    html, inserted = insert_mpl_diagram(html, lesson_num)
    if inserted:
        counts["mpl"] = 1

    html, inserted = insert_gemini_diagram(html, lesson_num)
    if inserted:
        counts["gemini"] = 1

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

    return counts


def main():
    attributions = load_attributions()
    totals = {"hero": 0, "mpl": 0, "gemini": 0}

    for lesson_num in range(1, 11):
        print(f"\nLesson {lesson_num:02d}:")
        counts = process_lesson(lesson_num, attributions)
        for k in totals:
            totals[k] += counts[k]
        parts = []
        if counts["hero"]:
            parts.append("hero")
        if counts["mpl"]:
            parts.append("mpl diagram")
        if counts["gemini"]:
            parts.append("concept image")
        if parts:
            print(f"  Inserted: {', '.join(parts)}")
        else:
            print(f"  No new insertions")

    print(f"\n=== Summary ===")
    print(f"  Hero images inserted: {totals['hero']}")
    print(f"  MPL diagrams inserted: {totals['mpl']}")
    print(f"  Concept images inserted: {totals['gemini']}")
    print(f"  Total insertions: {sum(totals.values())}")


if __name__ == "__main__":
    main()
