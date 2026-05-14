"""Generate cinematic video overviews for all lessons via NotebookLM CLI.

Supabase is the source of truth. Lessons with youtube_video_id IS NULL need
videos. The sessions file (_cinematic_sessions.json) is a temporary scratch
pad that maps active NotebookLM renders to lesson IDs. If it gets deleted,
nothing is lost — the next run re-queries Supabase and re-generates anything
missing.

Usage:
    python scripts/generate_cinematic_videos.py --limit 20
    python scripts/generate_cinematic_videos.py --limit 20 --subject sport-science
    python scripts/generate_cinematic_videos.py --status   (check in-progress jobs)
    python scripts/generate_cinematic_videos.py --download  (download completed videos)
    python scripts/generate_cinematic_videos.py --dry-run --limit 5
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import html as html_mod
from datetime import datetime

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

# ── Sessions file — tracks active in-progress renders only ───────────────
SESSIONS_FILE = os.path.join(SCRIPT_DIR, "_cinematic_sessions.json")

# ── Legacy state file — no longer used, kept for reference ───────────────
LEGACY_STATE_FILE = os.path.join(SCRIPT_DIR, "_cinematic_state.json")

# ── Subject order (smallest first) ──────────────────────────────────────
SUBJECT_ORDER = [
    "sport-science",
    "food-technology",
    "drama",
    "separate-sciences",
    "gcse-music",
    "business",
    "english-language",
    "english-language-edexcel",
    "english-language-ocr",
    "english-language-eduqas",
    "religious-education",
    "geography",
    "english-literature",
    "english-literature-edexcel",
    "english-literature-ocr",
    "english-literature-eduqas",
    "science",
    "science-edexcel",
    "science-ocr",
    "history",
    # "spanish",  # removed — no longer needs cinematic videos
    # "german",   # removed — no longer needs cinematic videos
    # "french",   # removed — no longer needs cinematic videos
    "design-technology",
    "creative-imedia",
    "computer-science",
    "computer-science-aqa",
    "computer-science-edexcel",
    "maths",
    "maths-aqa",
    "maths-ocr",
    "maths-eduqas",
    "health-social-care",
    "hospitality-catering",
    "music-technology",
    "it-ocr",
    "media-studies-aqa",
    "history-ocr",
]

# ── CLI env to avoid Windows encoding crashes ───────────────────────────
NLM_ENV = {**os.environ, "NO_COLOR": "1", "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}


def _reauth():
    """Re-authenticate with NotebookLM when cookies expire."""
    print("  [AUTH] Cookies expired — re-authenticating...")
    result = subprocess.run(
        ["nlm", "login"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=NLM_ENV, timeout=120,
    )
    if "Successfully authenticated" in (result.stdout or ""):
        print("  [AUTH] Re-authenticated successfully")
        return True
    print(f"  [AUTH] Re-auth may have failed: {(result.stdout or '')[:200]}")
    return False


def nlm_run(args, timeout=120, _retried=False):
    """Run an nlm CLI command and return stdout. Auto-retries on auth expiry."""
    result = subprocess.run(
        ["nlm"] + args,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=NLM_ENV, timeout=timeout,
    )
    output = (result.stdout or "") + (result.stderr or "")
    # Detect auth expiry and retry once
    if not _retried and ("Authentication expired" in output or "Authentication Error" in output):
        if _reauth():
            return nlm_run(args, timeout, _retried=True)
    if result.returncode != 0 and "Error" in (result.stderr or ""):
        raise RuntimeError(f"nlm {' '.join(args)} failed: {result.stderr[:300]}")
    return result.stdout.strip()


def nlm_json(args, timeout=120):
    """Run an nlm CLI command and parse JSON output."""
    out = nlm_run(args, timeout)
    # Find the JSON array or object in the output
    for start_char, end_char in [("[", "]"), ("{", "}")]:
        idx = out.find(start_char)
        if idx >= 0:
            end = out.rfind(end_char)
            if end > idx:
                return json.loads(out[idx:end + 1])
    return None


def strip_html(content_html):
    """Convert lesson HTML to clean text for NotebookLM."""
    c = content_html
    c = re.sub(r'<figure class="diagram">.*?</figure>', '', c, flags=re.DOTALL)
    c = re.sub(r'<img[^>]*>', '', c)
    c = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n\n## \1\n', c)
    c = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', c)
    c = re.sub(r'<li>(.*?)</li>', r'- \1', c, flags=re.DOTALL)
    c = re.sub(r'<span[^>]*>(.*?)</span>', r'\1', c)
    c = re.sub(r'<strong>(.*?)</strong>', r'\1', c)
    c = re.sub(r'<em>(.*?)</em>', r'\1', c)
    c = re.sub(r'<[^>]+>', '', c)
    c = html_mod.unescape(c)
    c = c.replace('\u2014', ' - ').replace('\u2013', '-').replace('\u2019', "'")
    c = c.replace('\u201c', '"').replace('\u201d', '"').replace('\u00d7', 'x')
    c = c.replace('\u00f7', '/').replace('\u2212', '-').replace('\u00b5', 'u')
    c = re.sub(r'\\\(.*?\\\)', '', c)
    c = re.sub(r'\$\$.*?\$\$', '', c)
    c = re.sub(r'\n{3,}', '\n\n', c)
    c = re.sub(r'[ \t]+', ' ', c)
    lines = [line.strip() for line in c.split('\n')]
    return '\n'.join(lines).strip()


def build_video_prompt(lesson, subject_name, unit_name, exam_board):
    """Build the NotebookLM focus prompt for cinematic video."""
    n = lesson["lesson_number"]
    ordinal = {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")

    headings = re.findall(r'<h2[^>]*>(.*?)</h2>', lesson.get("content_html", ""))
    if headings:
        topic_summary = "the key topics covered include " + ", ".join(headings[:6])
    else:
        topic_summary = f"the lesson titled '{lesson['title']}'"

    return (
        f"This is an overview of the {ordinal} GCSE revision lesson for students studying "
        f"{exam_board} {subject_name} ({unit_name}). It covers {lesson['title']} - "
        f"{topic_summary}. "
        f"Stick only to info present in the source material so as not to confuse or "
        f"overwhelm students. Keep language easy to understand but maintain the key "
        f"subject-specific terms that students will need to know for their exams. "
        f"Explain and define these where appropriate."
    )


# ── Sessions file helpers ────────────────────────────────────────────────

def load_sessions():
    """Load the active sessions scratch pad."""
    if os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("sessions", [])
    return []


def save_sessions(sessions):
    """Save the active sessions scratch pad."""
    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump({"sessions": sessions}, f, indent=2, ensure_ascii=False)


def prune_completed_sessions(sessions, sb):
    """Remove sessions whose lesson already has a youtube_video_id in Supabase."""
    if not sessions:
        return sessions

    lesson_ids = [s["lesson_id"] for s in sessions]
    # Query in batches of 50 to stay within URL length limits
    completed_ids = set()
    for i in range(0, len(lesson_ids), 50):
        batch = lesson_ids[i:i + 50]
        result = sb.table("lessons").select("id, youtube_video_id").in_("id", batch).execute()
        for row in (result.data or []):
            if row.get("youtube_video_id"):
                completed_ids.add(row["id"])

    if completed_ids:
        before = len(sessions)
        sessions = [s for s in sessions if s["lesson_id"] not in completed_ids]
        pruned = before - len(sessions)
        if pruned:
            print(f"Auto-pruned {pruned} sessions already completed in Supabase")

    return sessions


def _parse_timestamp(ts_str):
    """Parse a session timestamp (DD/MM/YYYY HH:MM) to datetime, or None."""
    if not ts_str:
        return None
    try:
        return datetime.strptime(ts_str, "%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        return None


def _session_age_hours(session):
    """Return how many hours ago the session was launched, or None if unknown."""
    ts = _parse_timestamp(session.get("launched_at"))
    if not ts:
        return None
    delta = datetime.now() - ts
    return delta.total_seconds() / 3600


# ── Core: get pending lessons from Supabase ──────────────────────────────

UNITY_SCHOOL_ID = "a5414d1c-8841-4bc5-8573-a9756752361b"


def get_pending_lessons(sb, limit, subject_filter=None, generic=False):
    """Get lessons needing videos (youtube_video_id IS NULL), ordered by SUBJECT_ORDER."""
    all_pending = []

    for subject_slug in SUBJECT_ORDER:
        if subject_filter and subject_slug != subject_filter:
            continue

        query = sb.table("subjects").select("id, name, exam_board").eq("slug", subject_slug)
        if generic:
            query = query.is_("school_id", "null")
        else:
            query = query.eq("school_id", UNITY_SCHOOL_ID)
        subj = query.execute()
        if not subj.data:
            continue
        subject = subj.data[0]

        units = sb.table("units").select("id, name, slug, accent").eq(
            "subject_id", subject["id"]
        ).order("sort_order").execute()

        for unit in (units.data or []):
            lessons = sb.table("lessons").select(
                "id, title, lesson_number, content_html, youtube_video_id"
            ).eq("unit_id", unit["id"]).is_("youtube_video_id", "null").order("lesson_number").execute()

            for lesson in (lessons.data or []):
                all_pending.append({
                    "lesson": lesson,
                    "subject_slug": subject_slug,
                    "subject_name": subject["name"],
                    "unit_slug": unit["slug"],
                    "unit_name": unit["name"],
                    "accent": unit.get("accent", "#666"),
                    "exam_board": subject.get("exam_board", "AQA"),
                })

        if len(all_pending) >= limit:
            break

    return all_pending[:limit]


# ── Commands ─────────────────────────────────────────────────────────────

def cmd_generate(args):
    """Generate cinematic videos for pending lessons (Supabase is source of truth)."""
    sb = get_client()

    # Load and prune sessions
    sessions = load_sessions()
    sessions = prune_completed_sessions(sessions, sb)
    save_sessions(sessions)

    # Build set of lesson IDs already in active sessions (prevents duplicate notebooks)
    active_lesson_ids = {s["lesson_id"] for s in sessions}
    if active_lesson_ids:
        print(f"{len(active_lesson_ids)} active sessions in progress\n")

    # Query Supabase for lessons needing videos
    pending = get_pending_lessons(sb, args.limit, args.subject, generic=args.generic)

    # Filter out lessons already in active sessions
    before = len(pending)
    pending = [p for p in pending if p["lesson"]["id"] not in active_lesson_ids]
    skipped = before - len(pending)
    if skipped:
        print(f"Skipped {skipped} lessons already in active sessions")

    if not pending:
        print("No lessons pending video generation!")
        return

    print(f"Generating videos for {len(pending)} lessons")
    print("=" * 60)

    timestamp = time.strftime("%d/%m/%Y %H:%M")
    created = 0

    for entry in pending:
        lesson = entry["lesson"]
        label = f"{entry['subject_slug']}/{entry['unit_slug']}/L{lesson['lesson_number']:02d}"

        print(f"\n  {label}: {lesson['title']}")

        if args.dry_run:
            print(f"  [DRY RUN] Would create notebook + generate video")
            created += 1
            continue

        # Export content — unique temp file per lesson to prevent cross-contamination
        content = strip_html(lesson["content_html"])
        safe_label = label.replace("/", "_")
        temp_path = os.path.join(SCRIPT_DIR, f"_temp_nlm_source_{safe_label}.txt")
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
        if not notebooks:
            print(f"  ERROR: Could not list notebooks")
            continue

        nb = next((n for n in notebooks if n["title"] == notebook_title), None)
        if not nb:
            nb = notebooks[0]
        notebook_id = nb["id"]
        print(f"  Notebook: {notebook_id}")

        # Add source
        try:
            nlm_run(["source", "add", notebook_id, "--file", temp_path, "--title", "Lesson Material", "--wait"], timeout=60)
        except Exception:
            pass

        # Clean up temp file immediately
        try:
            os.remove(temp_path)
        except OSError:
            pass
        time.sleep(2)

        # Generate video
        video_focus = build_video_prompt(lesson, entry["subject_name"], entry["unit_name"], entry["exam_board"])
        try:
            nlm_run(["video", "create", notebook_id, "--format", "cinematic", "--focus", video_focus, "--confirm"], timeout=60)
        except Exception:
            pass
        time.sleep(2)

        # Get artifact ID
        artifact_id = None
        status = nlm_json(["studio", "status", notebook_id])
        if status:
            for s in status:
                if s.get("type") == "video" and s.get("status") in ("in_progress", "completed"):
                    artifact_id = s["id"]
                    break

        # Save session
        session = {
            "lesson_id": lesson["id"],
            "label": label,
            "notebook_id": notebook_id,
            "artifact_id": artifact_id,
            "subject_name": entry["subject_name"],
            "unit_name": entry["unit_name"],
            "exam_board": entry.get("exam_board", "AQA"),
            "lesson_title": lesson["title"],
            "launched_at": timestamp,
        }
        sessions.append(session)
        save_sessions(sessions)

        created += 1
        aid_str = f" (artifact: {artifact_id[:8]})" if artifact_id else ""
        print(f"  LAUNCHED video{aid_str}")

        time.sleep(3)

    print(f"\n{'=' * 60}")
    print(f"Launched {created} cinematic video generations")
    print(f"Run with --status to check progress, --download when complete")


def cmd_status(args):
    """Check status of active sessions."""
    sb = get_client()
    sessions = load_sessions()
    sessions = prune_completed_sessions(sessions, sb)

    if not sessions:
        print("No active sessions.")
        save_sessions(sessions)
        return

    print(f"Checking {len(sessions)} active sessions...\n")

    completed = 0
    still_going = 0
    removed = 0
    remaining = []

    for session in sessions:
        label = session["label"]
        notebook_id = session.get("notebook_id")

        if not notebook_id:
            print(f"  {label}: No notebook ID — removing")
            removed += 1
            continue

        status = nlm_json(["studio", "status", notebook_id])

        if not status:
            # Notebook may have expired — check age
            age_h = _session_age_hours(session)
            if age_h is not None and age_h > 3:
                print(f"  {label}: EXPIRED (no response, {age_h:.1f}h old) — will be re-queued on next run")
                removed += 1
                continue
            else:
                print(f"  {label}: Could not check status (will retry)")
                remaining.append(session)
                still_going += 1
                continue

        # Find video artifact
        vid = None
        if session.get("artifact_id"):
            vid = next((s for s in status if s.get("id") == session["artifact_id"]), None)
        if not vid:
            vid = next((s for s in status if s.get("type") == "video"), None)

        if not vid:
            print(f"  {label}: No video artifact found — removing")
            removed += 1
            continue

        # Update artifact ID if we found one
        if vid and not session.get("artifact_id"):
            session["artifact_id"] = vid["id"]

        vid_status = vid.get("status", "unknown")

        if vid_status == "completed":
            completed += 1
            remaining.append(session)
            print(f"  {label}: COMPLETED — ready for download")
        elif vid_status == "failed":
            print(f"  {label}: FAILED — will be re-queued on next run")
            removed += 1
        else:
            still_going += 1
            remaining.append(session)
            print(f"  {label}: {vid_status}")

    save_sessions(remaining)

    summary = f"\nCompleted: {completed}, Still rendering: {still_going}"
    if removed:
        summary += f", Removed: {removed} (will be re-queued automatically)"
    print(summary)


def cmd_download(args):
    """Download completed videos, upload to R2, and update Supabase."""
    from lib.r2 import get_r2_client, VIDEO_BUCKET, VIDEO_PUBLIC_URL, AUDIO_BUCKET, AUDIO_PUBLIC_URL

    sb = get_client()
    sessions = load_sessions()
    sessions = prune_completed_sessions(sessions, sb)

    if not sessions:
        print("No active sessions. Run --status first or generate new videos.")
        save_sessions(sessions)
        return

    print(f"Checking {len(sessions)} sessions for completed videos...\n")

    download_dir = os.path.join(SCRIPT_DIR, "_cinematic_videos")
    os.makedirs(download_dir, exist_ok=True)

    r2_client = get_r2_client()
    downloaded = 0
    still_rendering = 0
    removed = 0
    remaining = []

    for session in sessions:
        label = session["label"]
        parts = label.split("/")
        lesson_id = session["lesson_id"]
        notebook_id = session.get("notebook_id")

        if not notebook_id:
            print(f"  {label}: No notebook ID — removing")
            removed += 1
            continue

        # Check notebook status
        try:
            nb_status = nlm_json(["studio", "status", notebook_id])
        except Exception:
            nb_status = None

        if not nb_status:
            age_h = _session_age_hours(session)
            if age_h is not None and age_h > 3:
                print(f"  {label}: Notebook expired — will be re-queued on next run")
                removed += 1
            else:
                print(f"  {label}: Could not check — keeping for retry")
                remaining.append(session)
            continue

        # Find video artifact
        vid = None
        if session.get("artifact_id"):
            vid = next((s for s in nb_status if s.get("id") == session["artifact_id"]), None)
        if not vid:
            vid = next((s for s in nb_status if s.get("type") == "video" and s.get("status") == "completed"), None)

        if not vid or vid.get("status") != "completed":
            vid_status = vid.get("status", "not found") if vid else "not found"
            print(f"  {label}: Video {vid_status} — skipping")
            remaining.append(session)
            still_rendering += 1
            continue

        # Update artifact ID if needed
        if vid and not session.get("artifact_id"):
            session["artifact_id"] = vid["id"]

        # ── Download video ──────────────────────────────────────
        video_filename = f"{label.replace('/', '_')}_cinematic.mp4"
        video_path = os.path.join(download_dir, video_filename)

        # Always delete stale cached file to prevent uploading wrong content
        if os.path.exists(video_path):
            os.remove(video_path)

        print(f"  {label}: Downloading video...")
        try:
            nlm_run([
                "download", "video", notebook_id,
                "--id", session["artifact_id"],
                "--output", video_path,
                "--no-progress",
            ], timeout=300)
        except Exception:
            pass

        if not (os.path.exists(video_path) and os.path.getsize(video_path) > 0):
            print(f"  {label}: Video download failed — keeping for retry")
            remaining.append(session)
            continue

        size_mb = os.path.getsize(video_path) / (1024 * 1024)
        print(f"  {label}: Video downloaded ({size_mb:.1f} MB)")

        # ── Upload to R2 ────────────────────────────────────────
        r2_key = f"{parts[0]}/{parts[1]}/cinematic_{parts[2].lower()}.mp4"
        print(f"  {label}: Uploading video to R2...")
        with open(video_path, "rb") as f:
            r2_client.put_object(Bucket=VIDEO_BUCKET, Key=r2_key, Body=f.read(), ContentType="video/mp4")
        video_r2_url = f"{VIDEO_PUBLIC_URL}/{r2_key}"

        # ── Update Supabase ─────────────────────────────────────
        sb.table("lessons").update({"youtube_video_id": video_r2_url}).eq("id", lesson_id).execute()
        print(f"  {label}: Published ({video_r2_url})")

        # ── Handle podcast artifact if present (legacy) ─────────
        audio_artifact_id = session.get("audio_artifact_id")
        if audio_artifact_id:
            audio_filename = f"{label.replace('/', '_')}_podcast.mp3"
            audio_path = os.path.join(download_dir, audio_filename)

            if not (os.path.exists(audio_path) and os.path.getsize(audio_path) > 0):
                print(f"  {label}: Downloading podcast...")
                try:
                    nlm_run([
                        "download", "audio", notebook_id,
                        "--id", audio_artifact_id,
                        "--output", audio_path,
                        "--no-progress",
                    ], timeout=300)
                except Exception:
                    pass

            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
                size_mb = os.path.getsize(audio_path) / (1024 * 1024)
                print(f"  {label}: Podcast downloaded ({size_mb:.1f} MB)")

                audio_r2_key = f"{parts[0]}/{parts[1]}/podcast_{parts[2].lower()}.mp3"
                print(f"  {label}: Uploading podcast to R2...")
                with open(audio_path, "rb") as f:
                    r2_client.put_object(Bucket=AUDIO_BUCKET, Key=audio_r2_key, Body=f.read(), ContentType="audio/mpeg")
                podcast_r2_url = f"{AUDIO_PUBLIC_URL}/{audio_r2_key}"

                # Update related_media — set Lesson Podcast URL
                lesson_row = sb.table("lessons").select("related_media").eq("id", lesson_id).single().execute()
                media = lesson_row.data.get("related_media") or [] if lesson_row.data else []

                podcast_cat = None
                for cat in media:
                    if (cat.get("category") or "").lower() == "podcasts":
                        podcast_cat = cat
                        break

                if not podcast_cat:
                    podcast_cat = {"emoji": "\U0001f3a7", "category": "Podcasts", "items": []}
                    media.append(podcast_cat)

                lp_item = None
                for item in podcast_cat.get("items", []):
                    if item.get("title") == "Lesson Podcast":
                        lp_item = item
                        break

                if lp_item:
                    lp_item["url"] = podcast_r2_url
                else:
                    podcast_cat["items"].insert(0, {
                        "title": "Lesson Podcast",
                        "url": podcast_r2_url,
                        "description": "AI-generated podcast overview of this lesson",
                    })

                sb.table("lessons").update({"related_media": media}).eq("id", lesson_id).execute()
                print(f"  {label}: Podcast published")

        # ── Clean up notebook ───────────────────────────────────
        if args.cleanup:
            try:
                nlm_run(["notebook", "delete", notebook_id, "--confirm"], timeout=30)
                print(f"  {label}: Notebook deleted")
            except Exception:
                pass

        # Session complete — do NOT add to remaining
        downloaded += 1
        time.sleep(2)

    save_sessions(remaining)

    print(f"\n{'=' * 60}")
    print(f"Downloaded & published: {downloaded}")
    if still_rendering:
        print(f"Still rendering: {still_rendering}")
    if removed:
        print(f"Removed (expired/invalid): {removed}")
    remaining_count = len(remaining)
    if remaining_count:
        print(f"Sessions remaining: {remaining_count}")
    print(f"Videos on R2, lessons updated in Supabase.")


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate cinematic video overviews via NotebookLM CLI. "
        "Supabase is the source of truth — lessons with no youtube_video_id are queued automatically."
    )
    parser.add_argument("--limit", type=int, default=20, help="Max lessons to process (default: 20)")
    parser.add_argument("--subject", help="Only process a specific subject slug")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated without doing it")
    parser.add_argument("--status", action="store_true", help="Check status of active sessions")
    parser.add_argument("--download", action="store_true", help="Download completed videos")
    parser.add_argument("--cleanup", action="store_true", help="Delete notebooks after downloading")
    parser.add_argument("--generic", action="store_true", help="Target generic (school_id NULL) subjects instead of school-specific")
    args = parser.parse_args()

    if args.status:
        cmd_status(args)
    elif args.download:
        cmd_download(args)
    else:
        cmd_generate(args)


if __name__ == "__main__":
    main()
