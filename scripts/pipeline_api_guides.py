"""
Pipeline API Guides — Generate exam technique + revision technique guides via the Anthropic API.

Usage:
    python scripts/pipeline_api_guides.py exam <job_id>
    python scripts/pipeline_api_guides.py revision <job_id>
"""

import json
import os
import re
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

import anthropic
from lib.supabase_client import get_client

MODEL = "claude-opus-4-6"
INPUT_PRICE = 15.0
OUTPUT_PRICE = 75.0


def load_doc(filename):
    path = os.path.join(PROJECT_ROOT, "docs", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


GUIDE_HTML_STRUCTURE = """
The guide page HTML must use this structure:

<main>
  [guide content here — use h2, p, div.key-fact, div.collapsible components]
</main>
<aside>
  <div class="sidebar-section">
    <div class="sidebar-section-title">Quick Reference</div>
    <div class="sidebar-media-item"><strong>Key point 1</strong><span>Brief detail</span></div>
    <div class="sidebar-media-item"><strong>Key point 2</strong><span>Brief detail</span></div>
  </div>
  <div class="sidebar-section">
    <div class="sidebar-section-title">Other Guides</div>
    OTHER_GUIDES_PLACEHOLDER
  </div>
</aside>

Use these HTML components in <main>: <h2>, <p>, <div class="key-fact"><div class="key-fact-label">Key Fact</div><p>...</p></div>,
<div class="collapsible"><button class="collapsible-toggle" aria-expanded="false"><span>Title</span><svg class="collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button><div class="collapsible-content"><div class="collapsible-inner"><p>Content</p></div></div></div>

Do NOT include data-narration-id attributes. Return ONLY the HTML, no markdown fences or explanation.
"""


def cmd_exam_guides(job_id):
    sb = get_client()
    client = anthropic.Anthropic()

    job = sb.table("upload_jobs").select("*").eq("id", job_id).single().execute().data
    plan = job.get("lesson_plan")
    if isinstance(plan, str):
        plan = json.loads(plan)

    subject_name = plan.get("subject_name", "GCSE Music")
    exam_board = plan.get("exam_board", "Eduqas")
    spec_code = plan.get("spec_code", "C660U")
    subject_slug = plan.get("subject_slug", "gcse-music")

    subj = sb.table("subjects").select("id").eq("slug", subject_slug).single().execute().data
    subject_id = subj["id"]

    question_types = plan.get("question_type_names", [])

    # Map question types to slugs
    type_slugs = {
        "1 mark \u2014 Multiple Choice / One-word Answer": "multiple-choice",
        "1 mark \u2014 Identification (bar number, instrument, key etc.)": "identification",
        "4 marks \u2014 Short Feature Identification (give bar numbers or identify features)": "short-feature-identification",
        "10 marks \u2014 Extended Listening Response (explain how music describes/creates effect)": "extended-listening-response",
        "12 marks \u2014 Prepared Extract with Score (multiple sub-questions)": "prepared-extract",
    }

    gen_prompt = load_doc("GENERATION_PROMPT.md")
    # Extract exam technique section
    match = re.search(r"## Exam Technique Guide Prompt\s*.*?```\s*\n(.*?)```", gen_prompt, re.DOTALL)
    exam_system = match.group(1).strip() if match else ""

    total_cost = 0.0
    total_input = 0
    total_output = 0
    guides_written = 0

    # Build other guides links for sidebar
    def other_guides_html(exclude_slug):
        links = []
        for qt, slug in type_slugs.items():
            if slug != exclude_slug:
                links.append(f'<a href="/guide/{subject_slug}/exam-technique/{slug}" class="sidebar-media-item"><strong>{qt}</strong></a>')
        return "\n    ".join(links)

    print(f"Generating exam technique guides for {subject_name}")
    print(f"Model: {MODEL}")
    print()

    for qt_name, slug in type_slugs.items():
        print(f"  Generating: {qt_name} -> {slug}")

        marks_match = re.match(r"(\d+) mark", qt_name)
        marks = marks_match.group(1) if marks_match else "?"

        structure = GUIDE_HTML_STRUCTURE.replace("OTHER_GUIDES_PLACEHOLDER", other_guides_html(slug))

        user_msg = f"""SUBJECT: {subject_name} ({exam_board} {spec_code})
QUESTION TYPE: {qt_name} [{marks} marks]
SET TEXT / CONTEXT: Eduqas GCSE Music Component 3 Appraising — listening exam (1hr 15min). Students listen to musical extracts and answer questions about what they hear. Set works: Bach Badinerie and Toto Africa.

Generate an exam technique guide page as HTML. Include:

1. WHAT THE QUESTION ASKS: Explain what this question type requires in plain language.
2. HOW MARKS ARE ALLOCATED: Include mark scheme descriptors.
3. STEP-BY-STEP METHOD: Numbered steps for answering this question type.
4. TIMING: How long to spend on this question in the exam (total paper is 1hr 15min).
5. MODEL ANSWER: A strong example answer (in a collapsible section).
6. WEAK ANSWER: A weak example showing common mistakes (in a collapsible section).
7. COMMON MISTAKES: 3-4 bullet points of what to avoid.
8. KEY TERMINOLOGY: Terms students should use in their answers.

{structure}"""

        start = time.time()
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=exam_system,
            messages=[{"role": "user", "content": user_msg}],
        )
        elapsed = time.time() - start
        usage = response.usage
        cost = (usage.input_tokens / 1_000_000) * INPUT_PRICE + (usage.output_tokens / 1_000_000) * OUTPUT_PRICE
        total_cost += cost
        total_input += usage.input_tokens
        total_output += usage.output_tokens

        content_html = response.content[0].text.strip()
        # Strip markdown fences if present
        if content_html.startswith("```"):
            content_html = re.sub(r"^```(?:html)?\s*\n?", "", content_html)
            content_html = re.sub(r"\n?```\s*$", "", content_html)

        sb.table("guide_pages").upsert({
            "subject_id": subject_id,
            "guide_type": "exam-technique",
            "slug": slug,
            "title": qt_name,
            "content_html": content_html,
        }, on_conflict="subject_id,guide_type,slug").execute()

        guides_written += 1
        print(f"    {elapsed:.1f}s, {usage.input_tokens:,} in / {usage.output_tokens:,} out, ${cost:.4f}")

    # Generate hub/index page
    print(f"  Generating: Hub index")
    hub_items = ""
    for qt_name, slug in type_slugs.items():
        hub_items += f'<li><a href="/guide/{subject_slug}/exam-technique/{slug}"><strong>{qt_name}</strong></a></li>\n'

    hub_msg = f"""Generate a hub/index page for the exam technique guides for {subject_name} ({exam_board} {spec_code}).

This is a listing page that introduces the exam format and links to individual guides.

The Eduqas GCSE Music Component 3 (Appraising) is a listening exam worth 40% of the GCSE. It lasts 1 hour 15 minutes.

Question types:
{chr(10).join(f'- {qt}' for qt in type_slugs.keys())}

Set works: Bach Badinerie (AoS1) and Toto Africa (AoS4).

The page should:
1. Briefly explain the exam format
2. Give an overview of how the paper is structured
3. List each question type with a brief description and link

Use links in format: /guide/{subject_slug}/exam-technique/[slug]

{GUIDE_HTML_STRUCTURE.replace('OTHER_GUIDES_PLACEHOLDER', '')}

In the sidebar Other Guides section, link to the revision technique hub:
<a href="/guide/{subject_slug}/revision-technique" class="sidebar-media-item"><strong>Revision Techniques</strong><span>Study methods for GCSE Music</span></a>"""

    start = time.time()
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": hub_msg}],
    )
    elapsed = time.time() - start
    usage = response.usage
    cost = (usage.input_tokens / 1_000_000) * INPUT_PRICE + (usage.output_tokens / 1_000_000) * OUTPUT_PRICE
    total_cost += cost
    total_input += usage.input_tokens
    total_output += usage.output_tokens

    content_html = response.content[0].text.strip()
    if content_html.startswith("```"):
        content_html = re.sub(r"^```(?:html)?\s*\n?", "", content_html)
        content_html = re.sub(r"\n?```\s*$", "", content_html)

    sb.table("guide_pages").upsert({
        "subject_id": subject_id,
        "type": "exam-technique",
        "slug": "index",
        "title": "Exam Technique Guides",
        "content_html": content_html,
        "status": "live",
    }, on_conflict="subject_id,type,slug").execute()
    guides_written += 1
    print(f"    {elapsed:.1f}s, {usage.input_tokens:,} in / {usage.output_tokens:,} out, ${cost:.4f}")

    print(f"\nExam guides complete: {guides_written} pages written")
    print(f"  Tokens: {total_input:,} in / {total_output:,} out")
    print(f"  Cost: ${total_cost:.4f}")
    return total_cost


def cmd_revision_guides(job_id):
    sb = get_client()
    client = anthropic.Anthropic()

    job = sb.table("upload_jobs").select("*").eq("id", job_id).single().execute().data
    plan = job.get("lesson_plan")
    if isinstance(plan, str):
        plan = json.loads(plan)

    subject_name = plan.get("subject_name", "GCSE Music")
    exam_board = plan.get("exam_board", "Eduqas")
    spec_code = plan.get("spec_code", "C660U")
    subject_slug = plan.get("subject_slug", "gcse-music")

    subj = sb.table("subjects").select("id").eq("slug", subject_slug).single().execute().data
    subject_id = subj["id"]

    gen_prompt = load_doc("GENERATION_PROMPT.md")
    match = re.search(r"## Revision Technique Guide Prompt\s*.*?```\s*\n(.*?)```", gen_prompt, re.DOTALL)
    rev_system = match.group(1).strip() if match else ""

    techniques = {
        "retrieval-practice": "Retrieval Practice",
        "spaced-repetition": "Spaced Repetition",
        "interleaving": "Interleaving",
        "dual-coding": "Dual Coding",
        "elaborative-interrogation": "Elaborative Interrogation",
        "knowledge-organisers": "Knowledge Organisers",
        "timed-exam-practice": "Timed Exam Practice",
        "active-listening": "Active Listening Practice",
    }

    total_cost = 0.0
    total_input = 0
    total_output = 0
    guides_written = 0

    def other_guides_html(exclude_slug):
        links = []
        for slug, name in techniques.items():
            if slug != exclude_slug:
                links.append(f'<a href="/guide/{subject_slug}/revision-technique/{slug}" class="sidebar-media-item"><strong>{name}</strong></a>')
        return "\n    ".join(links)

    print(f"Generating revision technique guides for {subject_name}")
    print(f"Model: {MODEL}")
    print()

    for slug, technique_name in techniques.items():
        print(f"  Generating: {technique_name} -> {slug}")

        structure = GUIDE_HTML_STRUCTURE.replace("OTHER_GUIDES_PLACEHOLDER", other_guides_html(slug))

        is_music_specific = slug == "active-listening"
        extra = ""
        if is_music_specific:
            extra = """This is a MUSIC-SPECIFIC technique. Active listening means deliberately analysing music while you listen — identifying elements using the MADTSHRIT framework (Melody, Articulation, Dynamics, Texture, Structure, Harmony, Rhythm, Instrumentation, Tempo). Students should practise with unfamiliar pieces as well as the set works (Bach Badinerie, Toto Africa)."""

        user_msg = f"""SUBJECT: {subject_name} ({exam_board} {spec_code})
TECHNIQUE: {technique_name}
{extra}

The subject covers: Musical Forms and Devices (binary, ternary, rondo), Music for Ensemble (chamber, jazz, musical theatre), Film Music (leitmotifs, minimalism, fusion), Popular Music (pop, rock, technology, bhangra), Set Works (Bach Badinerie, Toto Africa), and Musical Elements (melody, harmony, texture, rhythm, dynamics, instrumentation).

Generate a revision technique guide as HTML. Include:
1. WHAT IT IS: Explain the technique in plain language for a 15-16 year old.
2. WHY IT WORKS: Brief cognitive science explanation (1-2 paragraphs max).
3. HOW TO DO IT: Step-by-step instructions with GCSE Music examples.
4. EXAMPLE: A worked example using real music content (in a collapsible section).
5. COMMON MISTAKES: 2-3 bullet points.
6. QUICK START: A "try it now" prompt — one concrete action.

{structure}"""

        start = time.time()
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=rev_system,
            messages=[{"role": "user", "content": user_msg}],
        )
        elapsed = time.time() - start
        usage = response.usage
        cost = (usage.input_tokens / 1_000_000) * INPUT_PRICE + (usage.output_tokens / 1_000_000) * OUTPUT_PRICE
        total_cost += cost
        total_input += usage.input_tokens
        total_output += usage.output_tokens

        content_html = response.content[0].text.strip()
        if content_html.startswith("```"):
            content_html = re.sub(r"^```(?:html)?\s*\n?", "", content_html)
            content_html = re.sub(r"\n?```\s*$", "", content_html)

        sb.table("guide_pages").upsert({
            "subject_id": subject_id,
            "guide_type": "revision-technique",
            "slug": slug,
            "title": technique_name,
            "content_html": content_html,
        }, on_conflict="subject_id,guide_type,slug").execute()

        guides_written += 1
        print(f"    {elapsed:.1f}s, {usage.input_tokens:,} in / {usage.output_tokens:,} out, ${cost:.4f}")

    # Hub page
    print(f"  Generating: Hub index")
    hub_items = "\n".join(f"- {name}: /guide/{subject_slug}/revision-technique/{slug}" for slug, name in techniques.items())

    hub_msg = f"""Generate a hub/index page for the revision technique guides for {subject_name} ({exam_board} {spec_code}).

This is a listing page that introduces revision techniques and links to individual guides.

Techniques:
{hub_items}

The page should:
1. Briefly introduce why revision technique matters for music
2. List each technique with a brief description and link
3. Recommend which techniques work best for different aspects of music revision

{GUIDE_HTML_STRUCTURE.replace('OTHER_GUIDES_PLACEHOLDER', '')}

In the sidebar Other Guides section, link to the exam technique hub:
<a href="/guide/{subject_slug}/exam-technique" class="sidebar-media-item"><strong>Exam Technique Guides</strong><span>Question types for Component 3</span></a>"""

    start = time.time()
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": hub_msg}],
    )
    elapsed = time.time() - start
    usage = response.usage
    cost = (usage.input_tokens / 1_000_000) * INPUT_PRICE + (usage.output_tokens / 1_000_000) * OUTPUT_PRICE
    total_cost += cost
    total_input += usage.input_tokens
    total_output += usage.output_tokens

    content_html = response.content[0].text.strip()
    if content_html.startswith("```"):
        content_html = re.sub(r"^```(?:html)?\s*\n?", "", content_html)
        content_html = re.sub(r"\n?```\s*$", "", content_html)

    sb.table("guide_pages").upsert({
        "subject_id": subject_id,
        "type": "revision-technique",
        "slug": "index",
        "title": "Revision Technique Guides",
        "content_html": content_html,
        "status": "live",
    }, on_conflict="subject_id,type,slug").execute()
    guides_written += 1
    print(f"    {elapsed:.1f}s, {usage.input_tokens:,} in / {usage.output_tokens:,} out, ${cost:.4f}")

    print(f"\nRevision guides complete: {guides_written} pages written")
    print(f"  Tokens: {total_input:,} in / {total_output:,} out")
    print(f"  Cost: ${total_cost:.4f}")
    return total_cost


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    job_id = sys.argv[2]

    if command == "exam":
        cmd_exam_guides(job_id)
    elif command == "revision":
        cmd_revision_guides(job_id)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
