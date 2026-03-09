"""
Pipeline API Generate — Run content generation via the Anthropic API.

Uses Claude Opus 4.6 to generate lesson content from parsed teacher resources,
then writes results to Supabase via the existing pipeline infrastructure.

Usage:
    python scripts/pipeline_api_generate.py plan <job_id>
    python scripts/pipeline_api_generate.py generate <job_id> [--lesson N] [--unit SLUG] [--dry-run]
    python scripts/pipeline_api_generate.py cost <job_id>

Commands:
    plan       Generate a lesson plan from the job's extracted text
    generate   Generate lesson content (all lessons, or filtered by --lesson/--unit)
    cost       Estimate API cost for the job based on token counts
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

# Pricing per million tokens (USD)
INPUT_PRICE = 15.0
OUTPUT_PRICE = 75.0

# Question type specs per exam board
QUESTION_SPECS = {
    "AQA": "6 questions: 1x Define (1 mark), 1x Describe (2), 1x Explain (4), 1x Explain (6), 1x Evaluate (9), 1x Extended (12+4 SPaG)",
    "Edexcel": "6 questions: 1x Define (1 mark), 1x Outline (2), 2x Explain (3 each), 1x Discuss (6), 1x Justify/Evaluate (9 or 12)",
    "OCR": "6 questions: 1x Identify (1 mark), 1x State (2), 1x Describe (3), 1x Explain (4), 1x Extended response (6), 1x Discuss (8, QWC)",
    "WJEC": "6 questions: 1x Identify (1 mark), 1x Describe (2), 1x Explain (4), 1x Explain (6), 1x Assess (8), 1x Extended (12)",
}


def load_doc(filename):
    """Load a markdown doc from the docs/ directory."""
    path = os.path.join(PROJECT_ROOT, "docs", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_system_prompt():
    """Extract the system prompt from GENERATION_PROMPT.md."""
    doc = load_doc("GENERATION_PROMPT.md")
    # Extract content between ## System Prompt ```...```
    match = re.search(r"## System Prompt\s*```\s*\n(.*?)```", doc, re.DOTALL)
    if not match:
        print("ERROR: Could not extract system prompt from GENERATION_PROMPT.md")
        sys.exit(1)
    return match.group(1).strip()


def load_planning_prompt():
    """Extract the planning prompt from GENERATION_PROMPT.md."""
    doc = load_doc("GENERATION_PROMPT.md")
    match = re.search(r"## Planning Prompt\s*.*?```\s*\n(.*?)```", doc, re.DOTALL)
    if not match:
        print("ERROR: Could not extract planning prompt from GENERATION_PROMPT.md")
        sys.exit(1)
    return match.group(1).strip()


def get_example_lesson(sb):
    """Fetch a good example lesson from Supabase for structural reference."""
    # Use a Food Tech lesson — clean, recent, good format
    result = sb.table("lessons").select("content_html").eq("lesson_number", 3).limit(1).execute()
    if result.data:
        return result.data[0]["content_html"]
    return ""


def extract_source_for_lesson(extracted_text, lesson_plan):
    """Extract the relevant portion of source text for a lesson using its ppt_section_markers."""
    markers = lesson_plan.get("ppt_section_markers", [])
    if not markers:
        return extracted_text  # Fallback: send everything

    # Search for sections matching any marker
    text_lower = extracted_text.lower()
    chunks = []
    for marker in markers:
        marker_lower = marker.lower()
        # Find all occurrences of this marker
        idx = 0
        while True:
            pos = text_lower.find(marker_lower, idx)
            if pos == -1:
                break
            # Extract surrounding context (2000 chars before and after)
            start = max(0, pos - 500)
            end = min(len(extracted_text), pos + 3000)
            chunk = extracted_text[start:end]
            if chunk not in chunks:
                chunks.append(chunk)
            idx = pos + len(marker_lower)

    if chunks:
        return "\n\n---\n\n".join(chunks)
    return extracted_text  # Fallback if no markers matched


def validate_lesson_json(data, question_type_names=None):
    """Validate generated lesson JSON against the checklist. Returns (ok, errors)."""
    errors = []

    required_keys = ["description", "content_html", "exam_tip_html", "conclusion_html",
                     "practice_questions", "knowledge_checks", "glossary_terms"]
    for key in required_keys:
        if key not in data:
            errors.append(f"Missing required key: {key}")

    if not errors:
        # Description length
        desc = data.get("description", "")
        if len(desc) < 30 or len(desc) > 150:
            errors.append(f"Description length {len(desc)} (target 60-100)")

        # Content checks
        html = data.get("content_html", "")
        key_facts = len(re.findall(r'class="key-fact"', html))
        if key_facts < 2:
            errors.append(f"Only {key_facts} key-fact blocks (need 2+)")

        collapsibles = len(re.findall(r'class="collapsible"', html))
        if collapsibles < 2:
            errors.append(f"Only {collapsibles} collapsible blocks (need 2+)")

        glossary_in_html = len(re.findall(r'class="term"', html))
        if glossary_in_html < 3:
            errors.append(f"Only {glossary_in_html} glossary terms in HTML (need 3+)")

        diagrams = len(re.findall(r'<!-- DIAGRAM -->', html))
        if diagrams != 1:
            errors.append(f"Found {diagrams} DIAGRAM placeholders (need exactly 1)")

        if "<h1" in html:
            errors.append("Content contains <h1> tag (not allowed)")

        # Narration ID sequence check
        ids = re.findall(r'data-narration-id="n(\d+)"', html)
        if ids:
            id_nums = [int(x) for x in ids]
            expected = list(range(1, max(id_nums) + 1))
            if id_nums != expected:
                errors.append(f"Narration IDs not sequential (found gaps or disorder)")

        # Practice questions
        pqs = data.get("practice_questions", [])
        if len(pqs) != 6:
            errors.append(f"Found {len(pqs)} practice questions (need exactly 6)")
        for i, q in enumerate(pqs):
            if "text" not in q:
                errors.append(f"PQ {i+1}: missing 'text' field")
            if "type" not in q:
                errors.append(f"PQ {i+1}: missing 'type' field")
            if "marks" not in q:
                errors.append(f"PQ {i+1}: missing 'marks' field")

        # Knowledge checks
        kcs = data.get("knowledge_checks", [])
        if len(kcs) != 5:
            errors.append(f"Found {len(kcs)} knowledge checks (need exactly 5)")
        else:
            types = [kc.get("type") for kc in kcs]
            if types.count("mcq") != 2:
                errors.append(f"Knowledge checks: {types.count('mcq')} MCQs (need 2)")
            if types.count("fill") != 2:
                errors.append(f"Knowledge checks: {types.count('fill')} fill (need 2)")
            if types.count("match") != 1:
                errors.append(f"Knowledge checks: {types.count('match')} match (need 1)")

        # Diagram prompt should include accent colour
        dp = data.get("diagram_prompt", "")
        if not dp:
            errors.append("Missing diagram_prompt")
        elif not re.search(r"#[0-9a-fA-F]{6}", dp):
            errors.append("diagram_prompt doesn't include a hex colour")

    return len(errors) == 0, errors


def parse_json_response(text):
    """Parse JSON from API response, handling markdown fences."""
    text = text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
    return json.loads(text)


def cmd_plan(job_id):
    """Generate a lesson plan via the API."""
    sb = get_client()
    client = anthropic.Anthropic()

    # Fetch job data
    job = sb.table("upload_jobs").select("*").eq("id", job_id).single().execute().data
    config = job.get("subject_config") or {}
    extracted_text = job.get("extracted_text") or ""

    if not extracted_text:
        print("ERROR: No extracted text found for this job. Parse files first.")
        sys.exit(1)

    subject_name = config.get("subject_name", "Unknown")
    exam_board = config.get("exam_board", "Unknown")
    spec_code = config.get("spec_code", "")

    print(f"Generating lesson plan for: {subject_name} ({exam_board} {spec_code})")
    print(f"Source text: {len(extracted_text):,} characters")
    print(f"Model: {MODEL}")
    print()

    planning_prompt = load_planning_prompt()

    # Build the user message
    user_message = planning_prompt.replace("{subject_name}", subject_name)
    user_message = user_message.replace("{exam_board}", f"{exam_board} ({spec_code})")
    user_message = user_message.replace("{spec_code}", spec_code)
    # Replace source material placeholder
    user_message = user_message.replace("{full spec text or relevant sections}", extracted_text[:50000])
    user_message = user_message.replace("{extracted PPT/doc text}", extracted_text[:100000])
    user_message = user_message.replace("{extracted past paper and mark scheme text}", "(included in source material above)")

    print("Calling API...")
    start = time.time()

    response = client.messages.create(
        model=MODEL,
        max_tokens=8192,
        messages=[{"role": "user", "content": user_message}],
    )

    elapsed = time.time() - start
    usage = response.usage
    input_cost = (usage.input_tokens / 1_000_000) * INPUT_PRICE
    output_cost = (usage.output_tokens / 1_000_000) * OUTPUT_PRICE
    total_cost = input_cost + output_cost

    print(f"Done in {elapsed:.1f}s")
    print(f"Tokens: {usage.input_tokens:,} in / {usage.output_tokens:,} out")
    print(f"Cost: ${total_cost:.4f} (${input_cost:.4f} in + ${output_cost:.4f} out)")
    print()

    # Parse the plan
    raw = response.content[0].text
    try:
        plan = parse_json_response(raw)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse plan JSON: {e}")
        # Save raw response for debugging
        debug_path = os.path.join(SCRIPT_DIR, "_temp_plan_raw.txt")
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(raw)
        print(f"Raw response saved to {debug_path}")
        sys.exit(1)

    # Display the plan
    print("Lesson Plan:")
    for unit in plan.get("units", []):
        print(f"\n  {unit['name']} ({unit['slug']}):")
        if unit.get("subtitle"):
            print(f"    {unit['subtitle']}")
        for lesson in unit.get("lessons", []):
            print(f"    L{lesson['number']}: {lesson['title']}")

    if plan.get("question_type_names"):
        print(f"\nQuestion types: {plan['question_type_names']}")

    if plan.get("gaps"):
        print(f"\nSpec gaps: {plan['gaps']}")

    total_lessons = sum(len(u.get("lessons", [])) for u in plan.get("units", []))
    print(f"\nTotal: {total_lessons} lessons across {len(plan.get('units', []))} units")

    # Save plan to Supabase
    sb.table("upload_jobs").update({
        "lesson_plan": plan,
        "current_phase": "planned",
    }).eq("id", job_id).execute()
    print("\nPlan saved to Supabase.")

    # Also save locally for review
    plan_path = os.path.join(SCRIPT_DIR, f"_temp_plan_{job_id[:8]}.json")
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)
    print(f"Plan saved locally: {plan_path}")

    return plan


def cmd_generate(job_id, lesson_filter=None, unit_filter=None, dry_run=False):
    """Generate lesson content via the API."""
    sb = get_client()
    client = anthropic.Anthropic()

    # Fetch job data
    job = sb.table("upload_jobs").select("*").eq("id", job_id).single().execute().data
    config = job.get("subject_config") or {}
    extracted_text = job.get("extracted_text") or ""
    plan = job.get("lesson_plan")

    if not plan:
        print("ERROR: No lesson plan found. Run 'plan' command first.")
        sys.exit(1)

    if isinstance(plan, str):
        plan = json.loads(plan)

    subject_name = plan.get("subject_name", config.get("subject_name", "Unknown"))
    exam_board = plan.get("exam_board", config.get("exam_board", "Unknown"))
    spec_code = plan.get("spec_code", config.get("spec_code", ""))
    question_type_names = plan.get("question_type_names", [])

    # Get question spec for this exam board
    q_spec = QUESTION_SPECS.get(exam_board, QUESTION_SPECS.get("OCR"))

    # Load prompts and reference docs
    system_prompt = load_system_prompt()
    lesson_template_doc = load_doc("LESSON_TEMPLATE.md")
    questions_doc = load_doc("QUESTIONS_PIPELINE.md")
    example_html = get_example_lesson(sb)

    print(f"Subject: {subject_name} ({exam_board} {spec_code})")
    print(f"Model: {MODEL}")
    if dry_run:
        print("DRY RUN — will not call API or write to Supabase")
    print()

    # Build list of lessons to generate
    lessons_to_generate = []
    for unit in plan.get("units", []):
        if unit_filter and unit["slug"] != unit_filter:
            continue
        for lesson in unit.get("lessons", []):
            if lesson_filter is not None and lesson["number"] != lesson_filter:
                continue
            lessons_to_generate.append((unit, lesson))

    if not lessons_to_generate:
        print("No lessons matched the filter.")
        sys.exit(1)

    total = len(lessons_to_generate)
    print(f"Generating {total} lesson{'s' if total != 1 else ''}...")
    print()

    # Check which are already done
    steps = sb.table("pipeline_steps").select("unit_slug,lesson_number,content_done").eq("job_id", job_id).execute()
    done_set = set()
    for s in (steps.data or []):
        if s["content_done"]:
            done_set.add((s["unit_slug"], s["lesson_number"]))

    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0.0
    succeeded = 0
    failed = 0
    skipped = 0

    for idx, (unit, lesson) in enumerate(lessons_to_generate):
        unit_slug = unit["slug"]
        lesson_num = lesson["number"]
        title = lesson["title"]

        # Skip if already done
        if (unit_slug, lesson_num) in done_set:
            print(f"[{idx+1}/{total}] L{lesson_num:02d} '{title}' — already done, skipping")
            skipped += 1
            continue

        print(f"[{idx+1}/{total}] L{lesson_num:02d} '{title}' ({unit_slug})")

        # Extract source text for this lesson
        source_text = extract_source_for_lesson(extracted_text, lesson)

        # Get unit accent colour
        colors = config.get("colors", {})
        unit_index = next((i for i, u in enumerate(plan.get("units", [])) if u["slug"] == unit_slug), 0)
        accent = unit.get("accent") or colors.get(f"color{unit_index + 1}", colors.get("color1", "#6b7280"))

        # Total lessons in this unit
        total_in_unit = len(unit.get("lessons", []))

        # Build user message from template
        user_message = f"""SUBJECT: {subject_name} ({exam_board} {spec_code})
UNIT: {unit['name']} — {unit.get('subtitle', '')}
UNIT ACCENT COLOUR: {accent} — use this as the primary colour in the diagram_prompt
LESSON {lesson_num} of {total_in_unit}: {title}

EXAM SPECIFICATION (relevant extract):
<spec>
{lesson.get('spec_references', ['(see source material)'])}
</spec>

QUESTION TYPES FOR THIS EXAM BOARD:
{q_spec}

QUESTION TYPE NAMES (must use these exact strings in the "type" field):
{json.dumps(question_type_names)}

SOURCE MATERIAL FROM TEACHER:
<source>
{source_text[:80000]}
</source>

PAST PAPERS AND MARK SCHEMES (extract real questions where relevant):
<past_papers>
{lesson.get('relevant_past_papers', '(included in source material if available)')}
</past_papers>

STRUCTURAL REFERENCE (an existing lesson from StudyVault for format guidance):
<example>
{example_html[:8000]}
</example>

LESSON TEMPLATE COMPONENTS (available HTML patterns):
<template_doc>
{lesson_template_doc}
</template_doc>

QUESTIONS FORMAT REFERENCE:
<questions_doc>
{questions_doc}
</questions_doc>

Generate the complete lesson as a JSON object."""

        if dry_run:
            # Estimate token count (~4 chars per token)
            est_input = len(system_prompt + user_message) // 4
            print(f"  Estimated input: ~{est_input:,} tokens")
            continue

        # Call the API
        start = time.time()
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=8192,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )
        except Exception as e:
            print(f"  ERROR: API call failed: {e}")
            failed += 1
            continue

        elapsed = time.time() - start
        usage = response.usage
        input_cost = (usage.input_tokens / 1_000_000) * INPUT_PRICE
        output_cost = (usage.output_tokens / 1_000_000) * OUTPUT_PRICE
        lesson_cost = input_cost + output_cost
        total_input_tokens += usage.input_tokens
        total_output_tokens += usage.output_tokens
        total_cost += lesson_cost

        print(f"  API: {elapsed:.1f}s, {usage.input_tokens:,} in / {usage.output_tokens:,} out, ${lesson_cost:.4f}")

        # Parse response
        raw = response.content[0].text
        try:
            lesson_data = parse_json_response(raw)
        except json.JSONDecodeError as e:
            print(f"  ERROR: JSON parse failed: {e}")
            debug_path = os.path.join(SCRIPT_DIR, f"_temp_api_fail_L{lesson_num:02d}.txt")
            with open(debug_path, "w", encoding="utf-8") as f:
                f.write(raw)
            print(f"  Raw response saved to {debug_path}")
            failed += 1
            continue

        # Validate
        ok, validation_errors = validate_lesson_json(lesson_data, question_type_names)
        if not ok:
            print(f"  WARNINGS ({len(validation_errors)}):")
            for err in validation_errors:
                print(f"    - {err}")
            # Continue anyway — warnings, not blockers

        # Save JSON locally
        json_path = os.path.join(SCRIPT_DIR, f"_temp_api_{unit_slug}_L{lesson_num:02d}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(lesson_data, f, indent=2, ensure_ascii=False)

        # Write to Supabase via pipeline_generate.py write logic
        try:
            _write_lesson(sb, job_id, job, plan, config, unit_slug, lesson_num, lesson_data)
            print(f"  Written to Supabase")
            succeeded += 1
        except Exception as e:
            print(f"  ERROR writing to Supabase: {e}")
            failed += 1

    # Summary
    print(f"\n{'='*50}")
    print(f"Generation complete")
    print(f"  Succeeded: {succeeded}")
    print(f"  Failed:    {failed}")
    print(f"  Skipped:   {skipped}")
    if not dry_run and total_cost > 0:
        print(f"  Tokens:    {total_input_tokens:,} in / {total_output_tokens:,} out")
        print(f"  Cost:      ${total_cost:.4f} (~{chr(163)}{total_cost * 0.79:.2f})")


def _write_lesson(sb, job_id, job, plan, config, unit_slug, lesson_number, lesson_data):
    """Write a generated lesson to Supabase (mirrors pipeline_generate.py cmd_write)."""
    school_id = job.get("school_id")

    # Find unit and lesson in plan
    unit_plan = None
    lesson_plan = None
    unit_index = 0
    for i, u in enumerate(plan.get("units", [])):
        if u["slug"] == unit_slug:
            unit_plan = u
            unit_index = i
            for l in u.get("lessons", []):
                if l["number"] == lesson_number:
                    lesson_plan = l
                    break
            break

    if not unit_plan or not lesson_plan:
        raise ValueError(f"Unit '{unit_slug}' lesson {lesson_number} not found in plan")

    # Upsert subject
    subject_slug = plan.get("subject_slug", job.get("subject_slug"))
    subject_data = {
        "slug": subject_slug,
        "name": plan.get("subject_name", config.get("subject_name", "Unknown")),
        "exam_board": plan.get("exam_board", config.get("exam_board", "Unknown")),
        "spec_code": plan.get("spec_code", config.get("spec_code")) or None,
        "status": "live",
        "is_active": True,
    }
    if school_id:
        subject_data["school_id"] = school_id
    else:
        schools = sb.table("schools").select("id").limit(1).execute()
        subject_data["school_id"] = schools.data[0]["id"] if schools.data else None

    result = sb.table("subjects").upsert(subject_data, on_conflict="school_id,slug").execute()
    subject_id = result.data[0]["id"]

    # Upsert unit (preserve accent if already set)
    existing_unit = sb.table("units").select("id").eq("subject_id", subject_id).eq("slug", unit_slug).execute()
    if existing_unit.data:
        unit_id = existing_unit.data[0]["id"]
        sb.table("units").update({
            "name": unit_plan["name"],
            "lesson_count": len(unit_plan.get("lessons", [])),
        }).eq("id", unit_id).execute()
    else:
        colors = config.get("colors", {})
        accent = colors.get(f"color{unit_index + 1}", colors.get("color1", "#6b7280"))
        unit_data = {
            "subject_id": subject_id,
            "slug": unit_slug,
            "name": unit_plan["name"],
            "body_class": f"unit-{subject_slug}-{unit_index + 1}",
            "accent": accent,
            "accent_light": accent + "22",
            "accent_badge": accent + "33",
            "lesson_count": len(unit_plan.get("lessons", [])),
        }
        result = sb.table("units").upsert(unit_data, on_conflict="subject_id,slug").execute()
        unit_id = result.data[0]["id"]

    # Upsert lesson
    lesson_record = {
        "unit_id": unit_id,
        "lesson_number": lesson_number,
        "slug": f"lesson-{lesson_number:02d}",
        "title": lesson_plan["title"],
        "content_html": lesson_data.get("content_html", ""),
        "exam_tip_html": lesson_data.get("exam_tip_html"),
        "conclusion_html": lesson_data.get("conclusion_html"),
        "practice_questions": lesson_data.get("practice_questions", []),
        "knowledge_checks": lesson_data.get("knowledge_checks", []),
        "glossary_terms": lesson_data.get("glossary_terms", []),
        "status": "live",
    }
    if lesson_data.get("description"):
        lesson_record["description"] = lesson_data["description"]
    result = sb.table("lessons").upsert(lesson_record, on_conflict="unit_id,lesson_number").execute()
    lesson_id = result.data[0]["id"]

    # Update pipeline step
    step_data = {
        "job_id": job_id,
        "unit_slug": unit_slug,
        "lesson_number": lesson_number,
        "lesson_title": lesson_plan["title"],
        "lesson_id": lesson_id,
        "content_done": True,
        "questions_done": True,
        "glossary_done": True,
        "subject_slug": plan.get("subject_slug"),
    }
    if lesson_data.get("diagram_prompt"):
        step_data["diagram_prompt"] = lesson_data["diagram_prompt"]
    if lesson_data.get("hero_keywords"):
        step_data["hero_keywords"] = lesson_data["hero_keywords"]
    if lesson_data.get("diagram_style"):
        step_data["diagram_style"] = lesson_data["diagram_style"]

    sb.table("pipeline_steps").upsert(
        step_data, on_conflict="job_id,unit_slug,lesson_number"
    ).execute()

    # Update job progress
    completed = sb.table("pipeline_steps").select("id").eq("job_id", job_id).eq("content_done", True).execute()
    sb.table("upload_jobs").update({
        "lessons_created": len(completed.data),
        "current_phase": "generating",
    }).eq("id", job_id).execute()

    # Save content locally
    subject_slug = plan.get("subject_slug")
    content_dir = os.path.join(PROJECT_ROOT, subject_slug, unit_slug)
    os.makedirs(content_dir, exist_ok=True)
    filepath = os.path.join(content_dir, f"lesson-{lesson_number:02d}-content.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {lesson_plan['title']}\n\n")
        f.write(lesson_data.get("content_html", ""))
        if lesson_data.get("exam_tip_html"):
            f.write(f"\n\n## Exam Tip\n\n{lesson_data['exam_tip_html']}")
        if lesson_data.get("conclusion_html"):
            f.write(f"\n\n## Conclusion\n\n{lesson_data['conclusion_html']}")


def cmd_cost(job_id):
    """Estimate API cost for generating all lessons in a job."""
    sb = get_client()

    job = sb.table("upload_jobs").select("*").eq("id", job_id).single().execute().data
    config = job.get("subject_config") or {}
    extracted_text = job.get("extracted_text") or ""
    plan = job.get("lesson_plan")

    if not plan:
        print("ERROR: No lesson plan found. Run 'plan' command first.")
        sys.exit(1)

    if isinstance(plan, str):
        plan = json.loads(plan)

    system_prompt = load_system_prompt()
    lesson_template_doc = load_doc("LESSON_TEMPLATE.md")
    questions_doc = load_doc("QUESTIONS_PIPELINE.md")

    # Rough token estimate: ~4 chars per token
    system_tokens = len(system_prompt) // 4
    template_tokens = len(lesson_template_doc) // 4
    questions_tokens = len(questions_doc) // 4
    example_tokens = 2000  # Example lesson

    total_lessons = sum(len(u.get("lessons", [])) for u in plan.get("units", []))
    avg_source = len(extracted_text) // max(total_lessons, 1)
    source_tokens = avg_source // 4

    per_lesson_input = system_tokens + template_tokens + questions_tokens + example_tokens + source_tokens + 500
    per_lesson_output = 5000  # Typical output

    total_input = per_lesson_input * total_lessons
    total_output = per_lesson_output * total_lessons

    input_cost = (total_input / 1_000_000) * INPUT_PRICE
    output_cost = (total_output / 1_000_000) * OUTPUT_PRICE
    total_cost = input_cost + output_cost

    print(f"Cost Estimate for {plan.get('subject_name', 'Unknown')}")
    print(f"  Model: {MODEL}")
    print(f"  Lessons: {total_lessons}")
    print(f"  Source text: {len(extracted_text):,} chars")
    print()
    print(f"  Per lesson (estimated):")
    print(f"    Input:  ~{per_lesson_input:,} tokens")
    print(f"    Output: ~{per_lesson_output:,} tokens")
    print()
    print(f"  Total (estimated):")
    print(f"    Input:  ~{total_input:,} tokens  (${input_cost:.2f})")
    print(f"    Output: ~{total_output:,} tokens  (${output_cost:.2f})")
    print(f"    TOTAL:  ${total_cost:.2f} (~{chr(163)}{total_cost * 0.79:.2f})")
    print()
    print(f"  Note: Actual cost depends on source text per lesson and output length.")
    print(f"  Plan step adds ~${0.50:.2f} extra.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    job_id = sys.argv[2]

    if command == "plan":
        cmd_plan(job_id)

    elif command == "generate":
        lesson_filter = None
        unit_filter = None
        dry_run = False

        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--lesson" and i + 1 < len(sys.argv):
                lesson_filter = int(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == "--unit" and i + 1 < len(sys.argv):
                unit_filter = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--dry-run":
                dry_run = True
                i += 1
            else:
                print(f"Unknown argument: {sys.argv[i]}")
                sys.exit(1)

        cmd_generate(job_id, lesson_filter, unit_filter, dry_run)

    elif command == "cost":
        cmd_cost(job_id)

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)
