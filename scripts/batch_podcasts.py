"""
Batch podcast generator for lessons without podcasts.

Creates NotebookLM notebooks, adds lesson content, generates audio overviews
with unit context prompt, polls for completion, downloads, uploads to R2,
updates Supabase related_media.

Usage:
    python scripts/batch_podcasts.py --limit 200
    python scripts/batch_podcasts.py --limit 200 --subject science-edexcel
    python scripts/batch_podcasts.py --status
    python scripts/batch_podcasts.py --download --cleanup
    python scripts/batch_podcasts.py --dry-run --limit 10
"""

import argparse
import io
import json
import os
import re
import subprocess
import sys
import time
import html as html_mod

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
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL

STATE_FILE = os.path.join(SCRIPT_DIR, "_batch_podcast_state.json")
NLM_ENV = {**os.environ, "NO_COLOR": "1", "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}

LIVE_ONLY = False  # set by --live-only: only podcast lessons students can see

SUBJECT_ORDER = [
    "science-edexcel", "science-ocr",
    "english-language-edexcel", "english-language-ocr", "english-language-eduqas",
    "maths-aqa", "maths-ocr", "maths-eduqas",
    "english-literature-ocr", "english-literature-eduqas",
    "english-literature", "english-literature-edexcel",
]


def _reauth():
    print("  [AUTH] Cookies expired — re-authenticating...")
    result = subprocess.run(
        ["nlm", "login"], capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=NLM_ENV, timeout=120
    )
    if result.returncode == 0 and "success" in (result.stdout or "").lower():
        print("  [AUTH] Re-auth successful")
        return True
    print(f"  [AUTH] Re-auth may have failed: {(result.stdout or '')[:200]}")
    return False


def nlm_run(args, timeout=120, _retried=False):
    result = subprocess.run(
        ["nlm"] + args,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=NLM_ENV, timeout=timeout,
    )
    output = (result.stdout or "") + (result.stderr or "")
    if not _retried and ("Authentication expired" in output or "Authentication Error" in output):
        if _reauth():
            return nlm_run(args, timeout, _retried=True)
    if result.returncode != 0 and "Error" in (result.stderr or ""):
        raise RuntimeError(f"nlm {' '.join(args)} failed: {result.stderr[:300]}")
    return result.stdout.strip()


def nlm_json(args, timeout=120):
    out = nlm_run(args, timeout)
    for start_char, end_char in [("[", "]"), ("{", "}")]:
        idx = out.find(start_char)
        if idx >= 0:
            end = out.rfind(end_char)
            if end > idx:
                return json.loads(out[idx:end + 1])
    return None


def strip_html(content_html):
    c = content_html
    c = re.sub(r'<figure class="diagram">.*?</figure>', '', c, flags=re.DOTALL)
    c = re.sub(r'<img[^>]*>', '', c)
    c = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n\n## \1\n', c)
    c = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', c)
    c = re.sub(r'<li>(.*?)</li>', r'- \1', c, flags=re.DOTALL)
    c = re.sub(r'<[^>]+>', '', c)
    c = html_mod.unescape(c)
    c = c.replace('\u2014', ' - ').replace('\u2013', '-').replace('\u2019', "'")
    c = c.replace('\u201c', '"').replace('\u201d', '"')
    c = re.sub(r'\\\(.*?\\\)', '', c)
    c = re.sub(r'\$\$.*?\$\$', '', c)
    c = re.sub(r'\n{3,}', '\n\n', c)
    c = re.sub(r'[ \t]+', ' ', c)
    return '\n'.join(line.strip() for line in c.split('\n')).strip()


def build_podcast_prompt(lesson, subject_name, unit_name, exam_board, unit_lessons):
    n = lesson["lesson_number"]
    total = len(unit_lessons)
    ordinal = {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")

    # Build lesson list with context markers
    lesson_list = []
    for ul in unit_lessons:
        num = ul["lesson_number"]
        marker = " <-- THIS LESSON" if num == n else " (covered)" if num < n else " (upcoming)"
        lesson_list.append(f"{num}. {ul['title']}{marker}")

    return (
        f"This is a lesson podcast for the {ordinal} of {total} GCSE revision "
        f"lessons in the {unit_name} unit, for students studying {exam_board} "
        f"{subject_name}. The lesson is called \"{lesson['title']}\".\n\n"
        f"UNIT CONTEXT — here is where this lesson sits in the sequence:\n"
        + "\n".join(lesson_list) + "\n\n"
        f"The source titled \"Lesson Material\" is the focus of this podcast. The hosts "
        f"should treat lessons before this one as things students have already covered, "
        f"and lessons after it as things still to come. They can reference earlier "
        f"topics as assumed knowledge and tease future ones briefly, but should not "
        f"teach content from other lessons in detail — that is what those lessons are for.\n\n"
        f"TONE AND LANGUAGE:\n"
        f"- Two hosts having a natural, engaging conversation — not a lecture.\n"
        f"- Keep language accessible for 15-16 year olds but preserve the key "
        f"subject-specific terms students need for exams. Define and explain these "
        f"when first introduced.\n"
        f"- Use relatable analogies or everyday examples to make concepts stick.\n\n"
        f"OPENING — IMPORTANT:\n"
        f"- DO NOT start with 'imagine' or 'imagine that' or 'picture this'. "
        f"Vary the opening every time. Some ideas: jump straight into a surprising "
        f"fact, start with a question to the listener, begin with a bold statement, "
        f"open with a real-world connection, reference something from the previous "
        f"lesson, or just dive into the topic naturally. Be creative and different "
        f"each time."
    )


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"jobs": []}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def has_podcast(lesson):
    media = lesson.get("related_media") or []
    for cat in media:
        if (cat.get("category") or "").lower() in ("podcasts", "podcast"):
            for item in cat.get("items", []):
                if item.get("title") == "Lesson Podcast" and item.get("url") and item["url"] != "#":
                    return True
    return False


def _fetch_subject_lessons(sb, slug, subject, limit, all_pending):
    """Fetch pending lessons for a single subject and append to all_pending."""
    units = sb.from_('units').select('id, name, slug').eq('subject_id', subject['id']).order('sort_order').execute()
    for unit in (units.data or []):
        # Get all lessons in unit for context
        all_unit_lessons = sb.from_('lessons').select(
            'id, title, lesson_number, status, content_html, related_media'
        ).eq('unit_id', unit['id']).order('lesson_number').execute()

        for lesson in (all_unit_lessons.data or []):
            if has_podcast(lesson):
                continue
            # practice-format / stub lessons can't sustain a podcast
            if len(lesson.get("content_html") or "") < 800:
                continue
            if LIVE_ONLY and lesson.get("status") != "live":
                continue
            all_pending.append({
                "lesson": lesson,
                "subject_slug": slug,
                "subject_name": subject["name"],
                "unit_slug": unit["slug"],
                "unit_name": unit["name"],
                "exam_board": subject.get("exam_board", "AQA"),
                "unit_lessons": [{"lesson_number": l["lesson_number"], "title": l["title"]}
                                 for l in (all_unit_lessons.data or [])],
            })
        if len(all_pending) >= limit:
            break


def get_pending_lessons(sb, limit, subject_filter=None, school_id=None):
    all_pending = []

    # If a specific subject is requested that isn't in SUBJECT_ORDER, query directly
    if subject_filter and subject_filter not in SUBJECT_ORDER:
        query = sb.from_('subjects').select('id, name, exam_board').eq('slug', subject_filter)
        if school_id:
            query = query.eq('school_id', school_id)
        else:
            query = query.is_('school_id', 'null')
        subj = query.execute()
        if not subj.data:
            # Try without school_id filter as fallback
            subj = sb.from_('subjects').select('id, name, exam_board').eq('slug', subject_filter).execute()
        if subj.data:
            _fetch_subject_lessons(sb, subject_filter, subj.data[0], limit, all_pending)
        return all_pending[:limit]

    # Default: iterate SUBJECT_ORDER for generic subjects
    for slug in SUBJECT_ORDER:
        if subject_filter and slug != subject_filter:
            continue
        subj = sb.from_('subjects').select('id, name, exam_board').eq('slug', slug).is_('school_id', 'null').execute()
        if not subj.data:
            continue
        _fetch_subject_lessons(sb, slug, subj.data[0], limit, all_pending)
        if len(all_pending) >= limit:
            break
    return all_pending[:limit]


def cmd_generate(args):
    sb = get_client()
    state = load_state()
    active_ids = {j["lesson_id"] for j in state["jobs"] if j.get("status") == "in_progress"}

    pending = get_pending_lessons(sb, args.limit, args.subject, getattr(args, 'school', None))
    pending = [p for p in pending if p["lesson"]["id"] not in active_ids]

    if not pending:
        print("No lessons pending podcast generation!")
        return

    print(f"Generating podcasts for {len(pending)} lessons")
    print("=" * 60)

    created = 0
    for entry in pending:
        lesson = entry["lesson"]
        label = f"{entry['subject_slug']}/{entry['unit_slug']}/L{lesson['lesson_number']:02d}"
        print(f"\n  {label}: {lesson['title']}")

        if args.dry_run:
            print(f"  [DRY RUN] Would create notebook + generate podcast")
            created += 1
            continue

        # Export content
        content = strip_html(lesson["content_html"] or "")
        safe_label = label.replace("/", "_")
        temp_path = os.path.join(SCRIPT_DIR, f"_temp_nlm_{safe_label}.txt")
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Create notebook
        notebook_title = f"{entry['subject_name']} - {entry['unit_name']} - L{lesson['lesson_number']:02d} - {lesson['title']}"
        try:
            nlm_run(["notebook", "create", notebook_title])
        except Exception as e:
            print(f"  ERROR creating notebook: {e}")
            continue

        time.sleep(2)
        notebooks = nlm_json(["notebook", "list"])
        nb = next((n for n in notebooks if n["title"] == notebook_title), notebooks[0]) if notebooks else None
        if not nb:
            print(f"  ERROR: Could not find notebook")
            continue
        notebook_id = nb["id"]

        # Add source
        try:
            nlm_run(["source", "add", notebook_id, "--file", temp_path, "--title", "Lesson Material", "--wait"], timeout=60)
        except Exception:
            pass

        try:
            os.remove(temp_path)
        except OSError:
            pass
        time.sleep(2)

        # Generate podcast
        focus = build_podcast_prompt(lesson, entry["subject_name"], entry["unit_name"],
                                      entry["exam_board"], entry["unit_lessons"])
        try:
            nlm_run(["audio", "create", notebook_id, "--focus", focus, "--confirm"], timeout=60)
        except Exception:
            pass
        time.sleep(2)

        # Get artifact ID
        audio_artifact_id = None
        status = nlm_json(["studio", "status", notebook_id])
        if status:
            for s in status:
                if s.get("type") == "audio" and s.get("status") in ("in_progress", "completed"):
                    audio_artifact_id = s["id"]
                    break

        job = {
            "lesson_id": lesson["id"],
            "label": label,
            "notebook_id": notebook_id,
            "audio_artifact_id": audio_artifact_id,
            "status": "in_progress",
        }
        state["jobs"].append(job)
        save_state(state)
        created += 1
        print(f"  LAUNCHED (artifact: {audio_artifact_id})")
        time.sleep(3)

    print(f"\n{'=' * 60}")
    print(f"Launched {created} podcast generations")
    print(f"Run with --status to check, --download --cleanup when complete")


def cmd_status(args):
    state = load_state()
    active = [j for j in state["jobs"] if j.get("status") == "in_progress"]
    if not active:
        print("No in-progress jobs.")
        return

    print(f"Checking {len(active)} in-progress jobs...\n")
    completed = 0
    for job in active:
        try:
            status = nlm_json(["studio", "status", job["notebook_id"]])
        except Exception:
            print(f"  {job['label']}: Could not check")
            continue
        if not status:
            print(f"  {job['label']}: No status")
            continue
        for s in status:
            if s.get("type") == "audio":
                print(f"  {job['label']}: {s['status']}")
                if s["status"] == "completed":
                    job["status"] = "completed"
                    job["audio_artifact_id"] = s["id"]
                    completed += 1
                break
    save_state(state)
    print(f"\n{completed} completed, {len(active) - completed} still in progress")


def cmd_download(args):
    sb = get_client()
    r2 = get_r2_client()
    state = load_state()
    completed = [j for j in state["jobs"] if j.get("status") == "completed"]

    if not completed:
        print("No completed jobs to download.")
        return

    print(f"Downloading {len(completed)} podcasts...\n")
    downloaded = 0

    for job in completed:
        label = job["label"]
        notebook_id = job["notebook_id"]

        try:
            # Download audio
            mp3_path = os.path.join(SCRIPT_DIR, f"_temp_podcast_{label.replace('/', '_')}.m4a")
            nlm_run(["download", "audio", notebook_id, "-o", mp3_path], timeout=120)

            if not os.path.exists(mp3_path):
                print(f"  {label}: Download failed — file not found")
                continue

            # Upload to R2
            parts = label.split("/")
            r2_key = f"{parts[0]}/{parts[1]}/podcast_{parts[2].lower()}.mp3"
            with open(mp3_path, "rb") as f:
                audio_bytes = f.read()
            upload_bytes_to_r2(r2, AUDIO_BUCKET, r2_key, audio_bytes, "audio/mp4")
            podcast_url = f"{AUDIO_PUBLIC_URL}/{r2_key}"

            # Update Supabase related_media
            lesson_result = sb.from_('lessons').select('related_media').eq('id', job['lesson_id']).single().execute()
            media = lesson_result.data.get('related_media') or []

            # Find or create Podcasts category
            podcast_cat = None
            for cat in media:
                if (cat.get("category") or "").lower() in ("podcasts", "podcast"):
                    podcast_cat = cat
                    break
            if not podcast_cat:
                podcast_cat = {"emoji": "\U0001f3a7", "category": "Podcasts", "items": []}
                media.append(podcast_cat)

            # Add lesson podcast at top
            podcast_cat["items"].insert(0, {
                "url": podcast_url,
                "title": "Lesson Podcast",
                "description": "AI-generated audio overview of this lesson"
            })

            sb.from_('lessons').update({"related_media": media}).eq('id', job['lesson_id']).execute()

            # Cleanup
            os.remove(mp3_path)
            if args.cleanup:
                try:
                    nlm_run(["notebook", "delete", notebook_id, "--confirm"], timeout=30)
                except Exception:
                    pass

            job["status"] = "downloaded"
            save_state(state)
            downloaded += 1
            print(f"  {label}: Uploaded to R2 + Supabase updated")

        except Exception as e:
            print(f"  {label}: ERROR — {e}")

    print(f"\nDownloaded {downloaded}/{len(completed)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=200, help="Max lessons (default: 200)")
    parser.add_argument("--subject", help="Only process a specific subject slug")
    parser.add_argument("--school", help="School ID (UUID) for school-specific subjects")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--cleanup", action="store_true")
    parser.add_argument("--live-only", action="store_true",
                        help="Only lessons with status=live (dispatcher mode)")
    args = parser.parse_args()
    global LIVE_ONLY
    LIVE_ONLY = args.live_only

    if args.status:
        cmd_status(args)
    elif args.download:
        cmd_download(args)
    else:
        cmd_generate(args)


if __name__ == "__main__":
    main()
