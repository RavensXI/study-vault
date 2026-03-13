"""
Classify AQA Science PPTs — Sorts uploaded resources into Combined Science
(Trilogy 8464) vs Separate Sciences (Biology 8461 / Chemistry 8462 / Physics 8463).

Reads parsed PPT text from a Supabase upload_job, sends each PPT's content to
Claude with the AQA spec map, and produces a routing plan that maps each PPT
to the correct subject/unit.

Usage:
    python scripts/classify_aqa_science.py <job_id>                  # Classify all PPTs
    python scripts/classify_aqa_science.py <job_id> --dry-run        # Show plan without saving
    python scripts/classify_aqa_science.py <job_id> --save           # Save routing plan to Supabase
    python scripts/classify_aqa_science.py <job_id> --export FILE    # Export routing plan to JSON file
"""

import json
import os
import re
import sys

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

MODEL = "claude-sonnet-4-6"  # Sonnet for classification — fast + cheap

# Pricing per million tokens (USD) — Sonnet 4
INPUT_PRICE = 3.0
OUTPUT_PRICE = 15.0


def load_spec_map():
    """Load the AQA science spec map JSON."""
    path = os.path.join(SCRIPT_DIR, "aqa_science_spec_map.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def split_extracted_text(extracted_text):
    """Split extracted text into individual PPT documents.

    The parser outputs text with headers like:
        === filename.pptx ===
    or:
        --- Slide N ---

    Returns list of dicts: [{filename, text, slide_count}, ...]
    """
    documents = []

    # Try splitting by === filename === markers first
    file_pattern = r"={3,}\s*(.+?\.(?:pptx?|pdf|docx?))\s*={3,}"
    file_splits = re.split(file_pattern, extracted_text, flags=re.IGNORECASE)

    if len(file_splits) > 1:
        # Odd indices are filenames, even indices are content
        for i in range(1, len(file_splits), 2):
            filename = file_splits[i].strip()
            text = file_splits[i + 1].strip() if i + 1 < len(file_splits) else ""
            slide_count = len(re.findall(r"---\s*Slide\s+\d+", text, re.IGNORECASE))
            if text:
                documents.append({
                    "filename": filename,
                    "text": text,
                    "slide_count": max(slide_count, 1),
                })
    else:
        # No file markers — try splitting by slide markers with filenames in headers
        # Or treat entire text as one document
        # Check for common PPT filename patterns in the text
        ppt_refs = re.findall(r"[\w\s\-\.]+\.pptx?", extracted_text, re.IGNORECASE)
        if ppt_refs:
            # Single document with known filename
            documents.append({
                "filename": ppt_refs[0].strip(),
                "text": extracted_text,
                "slide_count": len(re.findall(r"---\s*Slide\s+\d+", extracted_text, re.IGNORECASE)),
            })
        else:
            documents.append({
                "filename": "unknown",
                "text": extracted_text,
                "slide_count": 1,
            })

    return documents


def build_classification_prompt(spec_map):
    """Build the system prompt for the classifier."""
    # Build a concise summary of the spec map for the prompt
    combined_sections = []
    separate_sections = {"biology": [], "chemistry": [], "physics": []}

    for science in ["biology", "chemistry", "physics"]:
        science_data = spec_map[science]
        for topic_key, topic in science_data["topics"].items():
            for section_key, section in topic.get("sections", {}).items():
                for sub_key, sub in section.get("subsections", {}).items():
                    entry = f"{sub_key} {sub['title']}"
                    if sub.get("ht_only"):
                        entry += " (HT only)"
                    if sub.get("combined", True):
                        combined_sections.append(f"[{science.upper()}] {entry}")
                    else:
                        separate_sections[science].append(entry)
                # Handle sections with no subsections but a combined flag
                if not section.get("subsections") and "combined" in section:
                    entry = f"{section_key} {section['title']}"
                    if not section["combined"]:
                        separate_sections[science].append(entry)

    return f"""You are an AQA GCSE Science content classifier. Your job is to analyse
parsed PowerPoint content and determine:

1. Which science discipline(s) it covers (Biology, Chemistry, Physics)
2. Which specific AQA spec sections it maps to
3. Whether the content is Combined Science (Trilogy 8464) or Separate Science only

## Classification Rules

- Content is "combined" if it covers spec points that appear in the Trilogy specification
- Content is "separate_only" if it covers spec points that are ONLY in the individual science specs
- A single PPT may contain BOTH combined and separate content — flag both
- If a PPT covers topics from multiple sciences, classify each portion separately

## Separate Science Only Sections

These sections are NOT in Trilogy — they only appear in the separate science specs:

### Biology Only
{chr(10).join(f"- {s}" for s in separate_sections["biology"])}

### Chemistry Only
{chr(10).join(f"- {s}" for s in separate_sections["chemistry"])}

### Physics Only
{chr(10).join(f"- {s}" for s in separate_sections["physics"])}

## Key Classification Markers

{json.dumps(spec_map["classification_keywords"], indent=2)}

## Output Format

For each PPT, return a JSON object:
```json
{{
  "filename": "the filename",
  "science": "biology|chemistry|physics",
  "topic_number": "4.X",
  "topic_title": "Topic Name",
  "spec_sections": ["4.X.Y.Z", ...],
  "classification": "combined|separate_only|mixed",
  "combined_sections": ["4.X.Y.Z section title", ...],
  "separate_sections": ["4.X.Y.Z section title", ...],
  "paper": 1 or 2,
  "confidence": "high|medium|low",
  "reasoning": "Brief explanation of why this classification was made",
  "suggested_lesson_title": "A concise revision lesson title for this content"
}}
```

If a PPT covers content from multiple topics or sciences, return multiple objects.

IMPORTANT: Return ONLY the JSON array, no other text."""


def classify_document(client, system_prompt, doc, batch_index, total):
    """Classify a single parsed PPT document."""
    print(f"  [{batch_index}/{total}] Classifying: {doc['filename']} ({len(doc['text']):,} chars, {doc['slide_count']} slides)")

    # Truncate very long documents to avoid token limits
    text = doc["text"]
    if len(text) > 50000:
        text = text[:50000] + "\n\n[... TRUNCATED — content continues ...]"

    user_prompt = f"""Classify this parsed PowerPoint content.

Filename: {doc['filename']}
Slides: {doc['slide_count']}

--- BEGIN CONTENT ---
{text}
--- END CONTENT ---

Return the classification as a JSON array of objects (one per topic/science covered).
Return ONLY the JSON array."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    # Track token usage
    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }

    # Parse the response
    response_text = response.content[0].text.strip()

    # Extract JSON from response (handle markdown code blocks)
    json_match = re.search(r"```(?:json)?\s*\n?(.*?)```", response_text, re.DOTALL)
    if json_match:
        response_text = json_match.group(1).strip()

    try:
        classifications = json.loads(response_text)
        if isinstance(classifications, dict):
            classifications = [classifications]
    except json.JSONDecodeError as e:
        print(f"    WARNING: Failed to parse JSON response: {e}")
        print(f"    Response: {response_text[:500]}")
        classifications = [{
            "filename": doc["filename"],
            "error": f"JSON parse error: {e}",
            "raw_response": response_text[:1000],
        }]

    return classifications, usage


def build_routing_plan(all_classifications):
    """Build a routing plan from all classifications.

    Outputs a structured plan that maps content to StudyVault subjects and units:
    - Subject "science" (Combined Science) with 6 units (bio P1, bio P2, chem P1, chem P2, phys P1, phys P2)
    - Subject "separate-sciences" with 3 units (biology, chemistry, physics)
    """
    routing = {
        "science": {
            "subject_name": "Science",
            "exam_board": "AQA",
            "spec_code": "8464",
            "units": {
                "biology-paper-1": {"name": "Biology Paper 1", "topics": "4.1-4.4", "items": []},
                "biology-paper-2": {"name": "Biology Paper 2", "topics": "4.5-4.7", "items": []},
                "chemistry-paper-1": {"name": "Chemistry Paper 1", "topics": "4.1-4.5", "items": []},
                "chemistry-paper-2": {"name": "Chemistry Paper 2", "topics": "4.6-4.10", "items": []},
                "physics-paper-1": {"name": "Physics Paper 1", "topics": "4.1-4.4", "items": []},
                "physics-paper-2": {"name": "Physics Paper 2", "topics": "4.5-4.7", "items": []},
            },
        },
        "separate-sciences": {
            "subject_name": "Separate Sciences",
            "exam_board": "AQA",
            "spec_code": "8461/8462/8463",
            "units": {
                "biology-separate": {"name": "Biology (Separate)", "items": []},
                "chemistry-separate": {"name": "Chemistry (Separate)", "items": []},
                "physics-separate": {"name": "Physics (Separate)", "items": []},
            },
        },
        "unclassified": [],
        "errors": [],
    }

    # Paper boundaries for combined science
    paper_boundaries = {
        "biology": {"paper_1": ["4.1", "4.2", "4.3", "4.4"], "paper_2": ["4.5", "4.6", "4.7"]},
        "chemistry": {"paper_1": ["4.1", "4.2", "4.3", "4.4", "4.5"], "paper_2": ["4.6", "4.7", "4.8", "4.9", "4.10"]},
        "physics": {"paper_1": ["4.1", "4.2", "4.3", "4.4"], "paper_2": ["4.5", "4.6", "4.7", "4.8"]},
    }

    for c in all_classifications:
        if "error" in c:
            routing["errors"].append(c)
            continue

        science = c.get("science", "").lower()
        classification = c.get("classification", "")
        topic = c.get("topic_number", "")

        if science not in paper_boundaries:
            routing["unclassified"].append(c)
            continue

        item = {
            "filename": c.get("filename", "unknown"),
            "spec_sections": c.get("spec_sections", []),
            "topic": f"{topic} {c.get('topic_title', '')}",
            "suggested_title": c.get("suggested_lesson_title", ""),
            "confidence": c.get("confidence", "unknown"),
            "reasoning": c.get("reasoning", ""),
        }

        # Route combined content
        if classification in ("combined", "mixed"):
            # Determine which paper
            paper_key = None
            for paper, topics in paper_boundaries[science].items():
                if topic in topics:
                    paper_key = paper
                    break

            if paper_key:
                unit_slug = f"{science}-{paper_key.replace('_', '-')}"
                if unit_slug in routing["science"]["units"]:
                    combined_item = {**item, "sections": c.get("combined_sections", [])}
                    routing["science"]["units"][unit_slug]["items"].append(combined_item)
            else:
                routing["unclassified"].append(c)

        # Route separate-only content
        if classification in ("separate_only", "mixed"):
            separate_unit = f"{science}-separate"
            if separate_unit in routing["separate-sciences"]["units"]:
                separate_item = {**item, "sections": c.get("separate_sections", [])}
                routing["separate-sciences"]["units"][separate_unit]["items"].append(separate_item)

    return routing


def print_routing_summary(routing):
    """Print a human-readable summary of the routing plan."""
    print("\n" + "=" * 70)
    print("ROUTING PLAN — AQA Science Classification Results")
    print("=" * 70)

    # Combined Science
    print(f"\n{'─' * 50}")
    print(f"SUBJECT: Science (Combined — Trilogy 8464)")
    print(f"{'─' * 50}")
    total_combined = 0
    for slug, unit in routing["science"]["units"].items():
        items = unit["items"]
        total_combined += len(items)
        print(f"\n  {unit['name']} ({unit['topics']}) — {len(items)} PPTs")
        for item in items:
            conf = f"[{item['confidence']}]" if item.get("confidence") else ""
            print(f"    • {item['filename']}")
            print(f"      Topic: {item['topic']}")
            print(f"      Sections: {', '.join(item.get('sections', item.get('spec_sections', [])))}")
            if item.get("suggested_title"):
                print(f"      Suggested title: {item['suggested_title']}")
            if conf:
                print(f"      Confidence: {conf}")

    # Separate Sciences
    print(f"\n{'─' * 50}")
    print(f"SUBJECT: Separate Sciences (8461/8462/8463)")
    print(f"{'─' * 50}")
    total_separate = 0
    for slug, unit in routing["separate-sciences"]["units"].items():
        items = unit["items"]
        total_separate += len(items)
        print(f"\n  {unit['name']} — {len(items)} PPTs")
        for item in items:
            print(f"    • {item['filename']}")
            print(f"      Topic: {item['topic']}")
            print(f"      Sections: {', '.join(item.get('sections', item.get('spec_sections', [])))}")
            if item.get("suggested_title"):
                print(f"      Suggested title: {item['suggested_title']}")

    # Unclassified
    if routing["unclassified"]:
        print(f"\n{'─' * 50}")
        print(f"UNCLASSIFIED — {len(routing['unclassified'])} items")
        print(f"{'─' * 50}")
        for item in routing["unclassified"]:
            print(f"    • {item.get('filename', 'unknown')}: {item.get('reasoning', 'No reason given')}")

    # Errors
    if routing["errors"]:
        print(f"\n{'─' * 50}")
        print(f"ERRORS — {len(routing['errors'])} items")
        print(f"{'─' * 50}")
        for item in routing["errors"]:
            print(f"    • {item.get('filename', 'unknown')}: {item.get('error', 'Unknown error')}")

    # Summary
    print(f"\n{'=' * 70}")
    print(f"TOTALS: {total_combined} combined, {total_separate} separate-only, "
          f"{len(routing['unclassified'])} unclassified, {len(routing['errors'])} errors")
    print(f"{'=' * 70}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    job_id = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    save = "--save" in sys.argv
    export_file = None
    if "--export" in sys.argv:
        idx = sys.argv.index("--export")
        if idx + 1 < len(sys.argv):
            export_file = sys.argv[idx + 1]
        else:
            print("ERROR: --export requires a filename")
            sys.exit(1)

    # Load spec map
    print("Loading AQA spec map...")
    spec_map = load_spec_map()

    # Load job from Supabase
    print(f"Loading job {job_id}...")
    sb = get_client()
    result = sb.table("upload_jobs").select("*").eq("id", job_id).single().execute()
    job = result.data

    if not job:
        print(f"ERROR: Job {job_id} not found")
        sys.exit(1)

    extracted_text = job.get("extracted_text", "")
    if not extracted_text:
        print("ERROR: No extracted text found in job. Run parse_job_local.js first.")
        sys.exit(1)

    print(f"Job: {job['filename']}")
    print(f"Text length: {len(extracted_text):,} chars")

    # Split into individual documents
    documents = split_extracted_text(extracted_text)
    print(f"Found {len(documents)} document(s) to classify")

    if dry_run:
        print("\n--- DRY RUN: Showing documents found ---")
        for i, doc in enumerate(documents, 1):
            print(f"  {i}. {doc['filename']} — {len(doc['text']):,} chars, {doc['slide_count']} slides")
            print(f"     Preview: {doc['text'][:200]}...")
        return

    # Build system prompt
    system_prompt = build_classification_prompt(spec_map)

    # Classify each document
    client = anthropic.Anthropic()
    all_classifications = []
    total_usage = {"input_tokens": 0, "output_tokens": 0}

    for i, doc in enumerate(documents, 1):
        classifications, usage = classify_document(client, system_prompt, doc, i, len(documents))
        all_classifications.extend(classifications)
        total_usage["input_tokens"] += usage["input_tokens"]
        total_usage["output_tokens"] += usage["output_tokens"]

        for c in classifications:
            science = c.get("science", "?")
            classification = c.get("classification", "?")
            conf = c.get("confidence", "?")
            print(f"    → {science} / {classification} / confidence: {conf}")
            if c.get("separate_sections"):
                print(f"      Separate: {', '.join(c['separate_sections'])}")

    # Build routing plan
    routing = build_routing_plan(all_classifications)

    # Print summary
    print_routing_summary(routing)

    # Cost summary
    input_cost = (total_usage["input_tokens"] / 1_000_000) * INPUT_PRICE
    output_cost = (total_usage["output_tokens"] / 1_000_000) * OUTPUT_PRICE
    total_cost = input_cost + output_cost
    print(f"\nAPI Cost: ${total_cost:.4f} "
          f"({total_usage['input_tokens']:,} in / {total_usage['output_tokens']:,} out)")

    # Export to file
    if export_file:
        output = {
            "job_id": job_id,
            "filename": job["filename"],
            "document_count": len(documents),
            "classification_count": len(all_classifications),
            "routing": routing,
            "raw_classifications": all_classifications,
            "cost": {
                "input_tokens": total_usage["input_tokens"],
                "output_tokens": total_usage["output_tokens"],
                "usd": round(total_cost, 4),
            },
        }
        with open(export_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nRouting plan exported to: {export_file}")

    # Save to Supabase (update the job with routing plan)
    if save:
        sb.table("upload_jobs").update({
            "lesson_plan": {
                "type": "aqa_science_routing",
                "routing": routing,
                "raw_classifications": all_classifications,
            }
        }).eq("id", job_id).execute()
        print(f"\nRouting plan saved to Supabase (job {job_id})")


if __name__ == "__main__":
    main()
