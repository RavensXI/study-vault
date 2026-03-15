"""Generate cinematic video overviews for all lessons via NotebookLM CLI.

Pulls lessons from Supabase that don't have video overviews yet,
creates NotebookLM notebooks, adds lesson content, generates cinematic
videos, downloads them, and updates the lesson record.

Usage:
    python scripts/generate_cinematic_videos.py --limit 20
    python scripts/generate_cinematic_videos.py --limit 20 --subject sport-science
    python scripts/generate_cinematic_videos.py --status   (check in-progress jobs)
    python scripts/generate_cinematic_videos.py --download  (download completed videos)
    python scripts/generate_cinematic_videos.py --dry-run --limit 5
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

# ── State file — tracks in-progress jobs across runs ─────────────────────
STATE_FILE = os.path.join(SCRIPT_DIR, "_cinematic_state.json")

# ── Subject order (smallest first) ──────────────────────────────────────
SUBJECT_ORDER = [
    "sport-science",
    "food-technology",
    "drama",
    "separate-sciences",
    "gcse-music",
    "business",
    "english-language",
    "religious-education",
    "geography",
    "english-literature",
    "science",
    "history",
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


def build_podcast_prompt(lesson, subject_name, unit_name, exam_board, unit_lessons):
    """Build the NotebookLM focus prompt for lesson podcast.

    Includes unit context (lesson sequence with covered/upcoming markers)
    so the AI hosts know what students have already learned and what's
    still to come.
    """
    n = lesson["lesson_number"]
    total = len(unit_lessons)
    ordinal = {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")

    # Build lesson list with marker
    lesson_list_lines = []
    for ul in unit_lessons:
        num = ul["lesson_number"]
        title = ul["title"]
        if num < n:
            lesson_list_lines.append(f"{num}. {title} (covered)")
        elif num == n:
            lesson_list_lines.append(f"{num}. {title} <-- THIS LESSON")
        else:
            lesson_list_lines.append(f"{num}. {title} (upcoming)")
    lesson_list = "\n".join(lesson_list_lines)

    return (
        f'This is a lesson podcast for the {ordinal} of {total} GCSE revision '
        f'lessons in the {unit_name} unit, for students studying {exam_board} '
        f'{subject_name}. The lesson is called "{lesson["title"]}".\n\n'
        f'UNIT CONTEXT — here is where this lesson sits in the sequence:\n'
        f'{lesson_list}\n\n'
        f'The source titled "Lesson Material" is the focus of this podcast. The hosts '
        f'should treat lessons before this one as things students have already covered, '
        f'and lessons after it as things still to come. They can reference earlier '
        f'topics as assumed knowledge and tease future ones briefly, but should not '
        f'teach content from other lessons in detail — that is what those lessons are '
        f'for.\n\n'
        f'TONE AND LANGUAGE:\n'
        f'- Two hosts having a natural, engaging conversation — not a lecture.\n'
        f'- Keep language accessible for 15-16 year olds but preserve the key '
        f'subject-specific terms students need for exams. Define and explain these '
        f'when first introduced.\n'
        f'- Use relatable analogies or everyday examples to make concepts stick.'
    )


def load_state():
    """Load in-progress job state."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"jobs": []}


def save_state(state):
    """Save in-progress job state."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def _has_podcast(lesson):
    """Check if a lesson already has a real podcast URL in related_media."""
    for cat in (lesson.get("related_media") or []):
        if (cat.get("category") or "").lower() == "podcasts":
            for item in cat.get("items", []):
                if item.get("title") == "Lesson Podcast" and item.get("url") and item["url"] != "#":
                    return True
    return False


def get_pending_lessons(sb, limit, subject_filter=None, mode="both"):
    """Get lessons needing media, ordered by subject priority.

    mode: 'both' = needs video, 'podcast-only' = needs podcast, 'video-only' = needs video
    """
    all_pending = []

    for subject_slug in SUBJECT_ORDER:
        if subject_filter and subject_slug != subject_filter:
            continue

        subj = sb.table("subjects").select("id, name, exam_board").eq("slug", subject_slug).execute()
        if not subj.data:
            continue
        subject = subj.data[0]

        units = sb.table("units").select("id, name, slug, accent").eq(
            "subject_id", subject["id"]
        ).order("sort_order").execute()

        for unit in (units.data or []):
            lessons = sb.table("lessons").select(
                "id, title, lesson_number, content_html, youtube_video_id, related_media"
            ).eq("unit_id", unit["id"]).order("lesson_number").execute()

            unit_lessons = [{"lesson_number": l["lesson_number"], "title": l["title"]} for l in (lessons.data or [])]

            for lesson in (lessons.data or []):
                # Determine if this lesson is pending based on mode
                if mode == "podcast-only":
                    if _has_podcast(lesson):
                        continue
                else:
                    # both or video-only: skip if already has video
                    if lesson.get("youtube_video_id"):
                        continue

                all_pending.append({
                    "lesson": lesson,
                    "subject_slug": subject_slug,
                    "subject_name": subject["name"],
                    "unit_slug": unit["slug"],
                    "unit_name": unit["name"],
                    "accent": unit.get("accent", "#666"),
                    "exam_board": subject.get("exam_board", "AQA"),
                    "unit_lessons": unit_lessons,
                })

        if len(all_pending) >= limit:
            break

    return all_pending[:limit]


def _get_video_only_pending(state, limit):
    """Find jobs that have podcasts done but no video — reuse their notebooks."""
    pending = []
    for job in state["jobs"]:
        if job.get("podcast_done") and not job.get("video_done") and not job.get("notebook_deleted"):
            pending.append(job)
        if len(pending) >= limit:
            break
    return pending


def cmd_generate(args):
    """Generate cinematic videos and/or podcasts for pending lessons."""
    sb = get_client()
    state = load_state()

    mode = "podcast-only" if args.podcast_only else "video-only" if args.video_only else "both"
    limit = args.limit if args.limit != 20 else (200 if mode == "podcast-only" else 20)

    # Check for already in-progress jobs
    active = [j for j in state["jobs"] if j["status"] == "in_progress"]
    if active:
        print(f"WARNING: {len(active)} jobs still in progress. Run --status to check or --download to complete them first.")
        print("Continuing with new jobs anyway...\n")

    # For video-only mode, reuse existing notebooks from state
    if args.video_only:
        pending = _get_video_only_pending(state, limit)
    else:
        pending = get_pending_lessons(sb, limit, args.subject, mode)

    if not pending:
        label = {"both": "video+podcast", "podcast-only": "podcast", "video-only": "video"}[mode]
        print(f"No lessons pending {label} generation!")
        return

    print(f"Generating {mode.upper()} for {len(pending)} lessons")
    print("=" * 60)

    timestamp = time.strftime("%d/%m/%Y %H:%M")
    do_video = mode in ("both", "video-only")
    do_podcast = mode in ("both", "podcast-only")

    created = 0
    for entry in pending:
        # video-only mode reuses existing jobs (entry IS the job dict)
        if args.video_only:
            job = entry
            label = job["label"]
            notebook_id = job["notebook_id"]
            lesson = {"lesson_number": int(label.split("/L")[1]), "title": job["lesson_title"]}
            print(f"\n  {label}: {job['lesson_title']}")

            if args.dry_run:
                print(f"  [DRY RUN] Would add video to existing notebook")
                created += 1
                continue

            video_focus = build_video_prompt(
                {"lesson_number": lesson["lesson_number"], "title": lesson["title"],
                 "content_html": ""},  # content already in notebook
                job.get("subject_name", ""), job.get("unit_name", ""), job.get("exam_board", "AQA"),
            )
            try:
                nlm_run(["video", "create", notebook_id, "--format", "cinematic", "--focus", video_focus, "--confirm"], timeout=60)
            except Exception:
                pass
            time.sleep(2)

            status = nlm_json(["studio", "status", notebook_id])
            if status:
                for s in status:
                    if s.get("type") == "video" and s.get("status") in ("in_progress", "completed") and not job.get("artifact_id"):
                        job["artifact_id"] = s["id"]

            job["status"] = "in_progress"
            job["video_launched"] = True
            job["video_launched_at"] = timestamp
            save_state(state)
            created += 1
            print(f"  LAUNCHED video (artifact: {job.get('artifact_id')})")
            time.sleep(3)
            continue

        # Normal mode (both or podcast-only): create notebook + source
        lesson = entry["lesson"]
        label = f"{entry['subject_slug']}/{entry['unit_slug']}/L{lesson['lesson_number']:02d}"

        print(f"\n  {label}: {lesson['title']}")

        if args.dry_run:
            print(f"  [DRY RUN] Would create notebook + generate {mode}")
            created += 1
            continue

        # Export content
        content = strip_html(lesson["content_html"])
        temp_path = os.path.join(SCRIPT_DIR, "_temp_nlm_source.txt")
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
        time.sleep(2)

        video_artifact_id = None
        audio_artifact_id = None

        # Generate video (if not podcast-only)
        if do_video:
            video_focus = build_video_prompt(lesson, entry["subject_name"], entry["unit_name"], entry["exam_board"])
            try:
                nlm_run(["video", "create", notebook_id, "--format", "cinematic", "--focus", video_focus, "--confirm"], timeout=60)
            except Exception:
                pass
            time.sleep(2)

        # Generate podcast (if not video-only)
        if do_podcast:
            podcast_focus = build_podcast_prompt(
                lesson, entry["subject_name"], entry["unit_name"],
                entry["exam_board"], entry.get("unit_lessons", []),
            )
            try:
                nlm_run(["audio", "create", notebook_id, "--focus", podcast_focus, "--confirm"], timeout=60)
            except Exception:
                pass
            time.sleep(2)

        # Get artifact IDs
        status = nlm_json(["studio", "status", notebook_id])
        if status:
            for s in status:
                if s.get("type") == "video" and s.get("status") in ("in_progress", "completed") and not video_artifact_id:
                    video_artifact_id = s["id"]
                elif s.get("type") == "audio" and s.get("status") in ("in_progress", "completed") and not audio_artifact_id:
                    audio_artifact_id = s["id"]

        # Save to state
        job = {
            "lesson_id": lesson["id"],
            "lesson_title": lesson["title"],
            "label": label,
            "notebook_id": notebook_id,
            "notebook_title": notebook_title,
            "artifact_id": video_artifact_id,
            "audio_artifact_id": audio_artifact_id,
            "status": "in_progress",
            "subject_name": entry["subject_name"],
            "unit_name": entry["unit_name"],
            "exam_board": entry.get("exam_board", "AQA"),
            "launched_at": timestamp,
            "podcast_done": False,
            "video_done": not do_video,  # True if we're not generating video (podcast-only)
        }
        state["jobs"].append(job)
        save_state(state)

        created += 1
        launched = []
        if video_artifact_id:
            launched.append(f"video:{video_artifact_id[:8]}")
        if audio_artifact_id:
            launched.append(f"podcast:{audio_artifact_id[:8]}")
        print(f"  LAUNCHED ({', '.join(launched)})")

        time.sleep(3)

    print(f"\n{'=' * 60}")
    print(f"Launched {created} cinematic video generations")
    print(f"Run with --status to check progress, --download when complete")


def cmd_status(args):
    """Check status of in-progress jobs."""
    state = load_state()
    active = [j for j in state["jobs"] if j["status"] == "in_progress"]

    if not active:
        print("No in-progress jobs.")
        return

    print(f"Checking {len(active)} in-progress jobs...\n")

    completed = 0
    still_going = 0

    for job in active:
        status = nlm_json(["studio", "status", job["notebook_id"]])
        if not status:
            print(f"  {job['label']}: Could not check status")
            still_going += 1
            continue

        # Find video artifact
        vid = next((s for s in status if s.get("id") == job.get("artifact_id")), None)
        if not vid:
            vid = next((s for s in status if s.get("type") == "video" and s.get("status") == "completed"), None)

        # Find audio artifact
        aud = next((s for s in status if s.get("id") == job.get("audio_artifact_id")), None)
        if not aud:
            aud = next((s for s in status if s.get("type") == "audio" and s.get("status") == "completed"), None)

        vid_done = vid and vid.get("status") == "completed"
        aud_done = aud and aud.get("status") == "completed"

        # Update artifact IDs if found
        if vid and not job.get("artifact_id"):
            job["artifact_id"] = vid["id"]
        if aud and not job.get("audio_artifact_id"):
            job["audio_artifact_id"] = aud["id"]

        # Check if video/podcast were even expected
        video_expected = job.get("artifact_id") or not job.get("video_done", False)
        podcast_expected = job.get("audio_artifact_id") is not None

        video_ok = vid_done if video_expected else True
        podcast_ok = aud_done if podcast_expected else True

        if video_ok and podcast_ok:
            job["status"] = "completed"
            if aud_done:
                job["podcast_done"] = True
            if vid_done:
                job["video_done"] = True
            completed += 1
            parts = []
            if vid_done: parts.append("video")
            if aud_done: parts.append("podcast")
            print(f"  {job['label']}: COMPLETED ({' + '.join(parts)})")
        else:
            still_going += 1
            vid_status = vid.get("status", "n/a") if video_expected else "n/a"
            aud_status = aud.get("status", "unknown") if podcast_expected else "n/a"
            print(f"  {job['label']}: video={vid_status}, podcast={aud_status}")

    save_state(state)
    print(f"\nCompleted: {completed}, Still in progress: {still_going}")


def cmd_download(args):
    """Download completed videos + podcasts, upload to R2, and update Supabase."""
    from lib.r2 import get_r2_client, VIDEO_BUCKET, VIDEO_PUBLIC_URL, AUDIO_BUCKET, AUDIO_PUBLIC_URL

    state = load_state()
    sb = get_client()

    completed = [j for j in state["jobs"] if j["status"] == "completed"]
    if not completed:
        print("No completed jobs to download. Run --status first.")
        return

    print(f"Processing {len(completed)} completed jobs...\n")

    download_dir = os.path.join(SCRIPT_DIR, "_cinematic_videos")
    os.makedirs(download_dir, exist_ok=True)

    r2_client = get_r2_client()
    processed = 0

    for job in completed:
        if job.get("published"):
            print(f"  {job['label']}: Already published, skipping")
            continue

        label = job["label"]
        parts = label.split("/")
        lesson_id = job["lesson_id"]

        # ── Video ──────────────────────────────────────────────
        video_filename = f"{label.replace('/', '_')}_cinematic.mp4"
        video_path = os.path.join(download_dir, video_filename)

        if not (os.path.exists(video_path) and os.path.getsize(video_path) > 0):
            print(f"  {label}: Downloading video...")
            try:
                nlm_run([
                    "download", "video", job["notebook_id"],
                    "--id", job["artifact_id"],
                    "--output", video_path,
                    "--no-progress",
                ], timeout=300)
            except Exception:
                pass

        if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
            size_mb = os.path.getsize(video_path) / (1024 * 1024)
            print(f"  {label}: Video downloaded ({size_mb:.1f} MB)")

            r2_key = f"{parts[0]}/{parts[1]}/cinematic_{parts[2].lower()}.mp4"
            print(f"  {label}: Uploading video to R2...")
            with open(video_path, "rb") as f:
                r2_client.put_object(Bucket=VIDEO_BUCKET, Key=r2_key, Body=f.read(), ContentType="video/mp4")
            video_r2_url = f"{VIDEO_PUBLIC_URL}/{r2_key}"

            sb.table("lessons").update({"youtube_video_id": video_r2_url}).eq("id", lesson_id).execute()
            print(f"  {label}: Video published")
            job["r2_url"] = video_r2_url
        else:
            print(f"  {label}: Video download failed")

        # ── Podcast ────────────────────────────────────────────
        audio_artifact_id = job.get("audio_artifact_id")
        if audio_artifact_id:
            audio_filename = f"{label.replace('/', '_')}_podcast.mp3"
            audio_path = os.path.join(download_dir, audio_filename)

            if not (os.path.exists(audio_path) and os.path.getsize(audio_path) > 0):
                print(f"  {label}: Downloading podcast...")
                try:
                    nlm_run([
                        "download", "audio", job["notebook_id"],
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
                lesson = sb.table("lessons").select("related_media").eq("id", lesson_id).single().execute()
                media = lesson.data.get("related_media") or [] if lesson.data else []

                # Find or create Podcasts category
                podcast_cat = None
                for cat in media:
                    if (cat.get("category") or "").lower() == "podcasts":
                        podcast_cat = cat
                        break

                if not podcast_cat:
                    podcast_cat = {"emoji": "\U0001f3a7", "category": "Podcasts", "items": []}
                    media.append(podcast_cat)

                # Find or create Lesson Podcast item
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
                job["podcast_r2_url"] = podcast_r2_url
            else:
                print(f"  {label}: Podcast download failed")

        # Only mark published if at least one asset was successfully uploaded
        video_ok = job.get("r2_url") or not job.get("artifact_id")
        podcast_ok = job.get("podcast_r2_url") or not job.get("audio_artifact_id")
        if video_ok and podcast_ok:
            job["published"] = True
            job["downloaded"] = True
        save_state(state)

        # Clean up notebook
        if args.cleanup:
            try:
                nlm_run(["notebook", "delete", job["notebook_id"], "--confirm"], timeout=30)
                print(f"  {label}: Notebook deleted")
                job["notebook_deleted"] = True
                save_state(state)
            except Exception:
                pass

        processed += 1
        time.sleep(2)

    print(f"\n{'=' * 60}")
    print(f"Published: {processed}/{len(completed)}")
    print(f"Videos + podcasts on R2, lessons updated in Supabase.")


def main():
    parser = argparse.ArgumentParser(description="Generate cinematic video overviews + podcasts via NotebookLM CLI")
    parser.add_argument("--limit", type=int, default=20, help="Max lessons to process (default: 20 for video, 200 for podcast-only)")
    parser.add_argument("--subject", help="Only process a specific subject slug")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated without doing it")
    parser.add_argument("--status", action="store_true", help="Check status of in-progress jobs")
    parser.add_argument("--download", action="store_true", help="Download completed videos + podcasts")
    parser.add_argument("--cleanup", action="store_true", help="Delete notebooks after downloading")
    parser.add_argument("--podcast-only", action="store_true", help="Generate only podcasts (keeps notebooks for later video)")
    parser.add_argument("--video-only", action="store_true", help="Add videos to existing notebooks (from prior podcast-only run)")
    args = parser.parse_args()

    if args.status:
        cmd_status(args)
    elif args.download:
        cmd_download(args)
    else:
        cmd_generate(args)


if __name__ == "__main__":
    main()
