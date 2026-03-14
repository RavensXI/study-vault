"""Claude-powered diagram QA — sends an image to Claude Sonnet for automated review.

Used by generate_diagrams.py to QA each diagram after Gemini generation.
Requires ANTHROPIC_API_KEY environment variable.
"""

import base64
import os

import anthropic

MODEL = "claude-sonnet-4-20250514"

QA_PROMPT = """You are a QA agent reviewing a Gemini-generated diagram for a GCSE revision website (students aged 15-16). Review this image against the checklist below.

LESSON: {lesson_title}
SUBJECT: {subject_name}
UNIT: {unit_name}
EXPECTED ACCENT COLOUR: {accent_color}

**QA CHECKLIST:**
1. **Text accuracy** — Read ALL text in the image character by character. Flag any misspellings, garbled/corrupted text, nonsensical words, truncated words, or overlapping text.
2. **Duplicate labels** — Check if any text label appears more than once when it shouldn't.
3. **Arrow/flow issues** — If it's a flow diagram, check arrows point in logical directions with no excessive/redundant arrows.
4. **Content accuracy** — Is the scientific content accurate and relevant to the lesson topic? Any factual errors?
5. **Visual quality** — Any AI artifacts, blurry areas, cut-off elements, cramped layout, stray characters?
6. **Prompt leaks** — Any visible hex colour codes, "GCSE", "aged 15-16", "pictorial isotype", "educational", or other meta-instruction text rendered in the image?
7. **Colour scheme** — Does the diagram use the expected accent colour?

Respond with EXACTLY one of these two formats:

If the diagram passes all checks:
VERDICT: PASS

If the diagram fails any check:
VERDICT: FAIL
ISSUES:
- [specific issue 1]
- [specific issue 2]
...

Be strict but fair. Minor cosmetic issues (slightly different shade of accent colour, minor layout preferences) are acceptable. Text errors, garbled words, prompt leaks, duplicate labels, and factual errors are NOT acceptable."""


def qa_diagram(image_bytes, lesson_title, subject_name, unit_name, accent_color):
    """Send a diagram image to Claude for QA review.

    Args:
        image_bytes: Raw JPEG bytes of the diagram.
        lesson_title: Title of the lesson.
        subject_name: Name of the subject (e.g. "Science").
        unit_name: Name of the unit (e.g. "Biology Paper 1").
        accent_color: Expected accent colour hex code (e.g. "#16a34a").

    Returns:
        (passed: bool, issues: list[str]) tuple.
    """
    client = anthropic.Anthropic()

    prompt = QA_PROMPT.format(
        lesson_title=lesson_title,
        subject_name=subject_name,
        unit_name=unit_name,
        accent_color=accent_color,
    )

    img_b64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": img_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
    )

    result_text = response.content[0].text.strip()

    if "VERDICT: PASS" in result_text:
        return True, []

    # Parse issues
    issues = []
    if "ISSUES:" in result_text:
        issues_section = result_text.split("ISSUES:", 1)[1].strip()
        for line in issues_section.split("\n"):
            line = line.strip()
            if line.startswith("- "):
                issues.append(line[2:])
            elif line:
                issues.append(line)

    return False, issues
