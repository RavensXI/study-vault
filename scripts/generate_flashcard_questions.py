"""
Generate 5 flashcard Q&A pairs per lesson and write to Supabase.

Reads lesson content_html, extracts key facts and concepts, generates
5 short Q&A pairs suitable for flashcard recall practice. These are
different from knowledge_checks (which test via MCQ/fill/match).

Usage:
    python scripts/generate_flashcard_questions.py                    # all lessons
    python scripts/generate_flashcard_questions.py --subject history  # one subject
    python scripts/generate_flashcard_questions.py --limit 50         # first 50
    python scripts/generate_flashcard_questions.py --dry-run          # preview
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

from lib.supabase_client import get_client


def strip_html(html):
    """Remove HTML tags, keep text."""
    text = re.sub(r'<[^>]+>', ' ', html or '')
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:3000]  # Limit context size


def generate_questions_from_content(title, content_text, glossary_terms, existing_kc):
    """Generate 5 flashcard Q&A pairs from lesson content.

    Returns a list of {q, a} dicts. Uses simple extraction patterns
    rather than an LLM call — fast and free.
    """
    questions = []

    # Strategy 1: Reverse glossary — give definition, ask for term
    for term in glossary_terms[:3]:
        if term.get('term') and term.get('definition'):
            questions.append({
                'q': term['definition'],
                'a': term['term']
            })

    # Strategy 2: Extract key facts from content
    # Look for sentences with dates, numbers, names, or key phrases
    sentences = re.split(r'[.!?]+', content_text)
    key_sentences = []
    for s in sentences:
        s = s.strip()
        if len(s) < 20 or len(s) > 200:
            continue
        # Prefer sentences with specific facts
        if re.search(r'\d{4}|\d+%|\d+ million|\d+ billion', s):
            key_sentences.append(s)
        elif re.search(r'is called|is known as|refers to|means that|is defined as', s, re.I):
            key_sentences.append(s)

    # Create fill-in-blank style questions from key sentences
    for s in key_sentences:
        if len(questions) >= 5:
            break
        # Find a key term to blank out
        words = s.split()
        if len(words) < 5:
            continue
        # Find capitalised words or numbers as candidates for blanking
        for i, w in enumerate(words):
            clean = re.sub(r'[^a-zA-Z0-9]', '', w)
            if len(clean) > 3 and (clean[0].isupper() or re.match(r'\d+', clean)):
                blanked = ' '.join(words[:i] + ['_____'] + words[i+1:])
                questions.append({
                    'q': blanked,
                    'a': clean
                })
                break

    # Strategy 3: If we still need more, create "What is..." questions from remaining glossary
    for term in glossary_terms[3:]:
        if len(questions) >= 5:
            break
        if term.get('term') and term.get('definition'):
            questions.append({
                'q': f"What is meant by '{term['term']}'?",
                'a': term['definition']
            })

    # Strategy 4: If still short, create questions from the title
    if len(questions) < 5:
        questions.append({
            'q': f"Name a key concept from '{title}'.",
            'a': glossary_terms[0]['term'] if glossary_terms else title
        })

    return questions[:5]


def main():
    parser = argparse.ArgumentParser(description="Generate flashcard questions for lessons")
    parser.add_argument("--subject", help="Only process a specific subject slug")
    parser.add_argument("--limit", type=int, help="Max lessons to process")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--school-only", action="store_true", help="Only school-specific subjects")
    parser.add_argument("--generic-only", action="store_true", help="Only generic subjects")
    args = parser.parse_args()

    sb = get_client()

    # Get subjects
    query = sb.table("subjects").select("id, name, slug, school_id").eq("status", "live").order("name")
    if args.subject:
        query = query.eq("slug", args.subject)
    subjects = query.execute().data or []

    if args.school_only:
        subjects = [s for s in subjects if s.get("school_id")]
    elif args.generic_only:
        subjects = [s for s in subjects if not s.get("school_id")]

    total = 0
    written = 0
    skipped = 0

    for subject in subjects:
        units = sb.table("units").select("id, slug, name").eq("subject_id", subject["id"]).order("sort_order").execute().data or []

        for unit in units:
            lessons = sb.table("lessons").select(
                "id, title, lesson_number, content_html, glossary_terms, knowledge_checks, flashcard_questions"
            ).eq("unit_id", unit["id"]).eq("status", "live").order("lesson_number").execute().data or []

            for lesson in lessons:
                if args.limit and total >= args.limit:
                    break

                total += 1

                # Skip if already has flashcard questions
                existing = lesson.get("flashcard_questions") or []
                if isinstance(existing, list) and len(existing) >= 5:
                    skipped += 1
                    continue

                content_text = strip_html(lesson.get("content_html", ""))
                glossary = lesson.get("glossary_terms", []) or []
                kc = lesson.get("knowledge_checks", []) or []

                questions = generate_questions_from_content(
                    lesson["title"], content_text, glossary, kc
                )

                scope = "school" if subject.get("school_id") else "generic"
                label = f"{subject['slug']}/{unit['slug']}/L{lesson['lesson_number']:02d}"

                if args.dry_run:
                    print(f"  {label}: {len(questions)} questions generated")
                    for q in questions:
                        print(f"    Q: {q['q'][:80]}")
                        print(f"    A: {q['a'][:80]}")
                    continue

                sb.table("lessons").update({
                    "flashcard_questions": questions
                }).eq("id", lesson["id"]).execute()

                written += 1
                if written % 50 == 0:
                    print(f"  Written {written} lessons...")

            if args.limit and total >= args.limit:
                break
        if args.limit and total >= args.limit:
            break

    print(f"\nDone! Processed {total} lessons: {written} written, {skipped} already had questions.")


if __name__ == "__main__":
    main()
