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


def nlm_run(args, timeout=120):
    """Run an nlm CLI command and return stdout."""
    result = subprocess.run(
        ["nlm"] + args,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=NLM_ENV, timeout=timeout,
    )
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


def build_focus_prompt(lesson, subject_name, unit_name, exam_board):
    """Build the NotebookLM focus prompt from the template."""
    # Get ordinal
    n = lesson["lesson_number"]
    ordinal = {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")

    # Build topic summary from h2 headings in the content
    headings = re.findall(r'<h2[^>]*>(.*?)</h2>', lesson.get("content_html", ""))
    if headings:
        topic_list = ", ".join(headings[:6])
        topic_summary = f"the key topics covered include {topic_list}"
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


def get_pending_lessons(sb, limit, subject_filter=None):
    """Get lessons without cinematic video overviews, ordered by subject priority."""
    all_pending = []

    for subject_slug in SUBJECT_ORDER:
        if subject_filter and subject_slug != subject_filter:
            continue

        # Get subject
        subj = sb.table("subjects").select("id, name, exam_board").eq("slug", subject_slug).execute()
        if not subj.data:
            continue
        subject = subj.data[0]

        # Get units
        units = sb.table("units").select("id, name, slug, accent").eq(
            "subject_id", subject["id"]
        ).order("sort_order").execute()

        for unit in (units.data or []):
            # Get lessons without video
            lessons = sb.table("lessons").select(
                "id, title, lesson_number, content_html, youtube_video_id"
            ).eq("unit_id", unit["id"]).order("lesson_number").execute()

            for lesson in (lessons.data or []):
                # Skip if already has a video
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
                })

        if len(all_pending) >= limit:
            break

    return all_pending[:limit]


def cmd_generate(args):
    """Generate cinematic videos for pending lessons."""
    sb = get_client()
    state = load_state()

    # Check for already in-progress jobs
    active = [j for j in state["jobs"] if j["status"] == "in_progress"]
    if active:
        print(f"WARNING: {len(active)} jobs still in progress. Run --status to check or --download to complete them first.")
        print("Continuing with new jobs anyway...\n")

    pending = get_pending_lessons(sb, args.limit, args.subject)
    if not pending:
        print("No lessons pending cinematic video overviews!")
        return

    print(f"Generating cinematic videos for {len(pending)} lessons")
    print("=" * 60)

    created = 0
    for entry in pending:
        lesson = entry["lesson"]
        label = f"{entry['subject_slug']}/{entry['unit_slug']}/L{lesson['lesson_number']:02d}"

        print(f"\n  {label}: {lesson['title']}")

        if args.dry_run:
            print(f"  [DRY RUN] Would create notebook, add source, generate cinematic video")
            created += 1
            continue

        # 1. Export content to temp file
        content = strip_html(lesson["content_html"])
        temp_path = os.path.join(SCRIPT_DIR, "_temp_nlm_source.txt")
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(content)

        # 2. Create notebook
        notebook_title = f"{entry['subject_name']} - {entry['unit_name']} - L{lesson['lesson_number']:02d} - {lesson['title']}"
        try:
            nlm_run(["notebook", "create", notebook_title])
        except Exception as e:
            print(f"  ERROR creating notebook: {e}")
            continue

        # 3. Get the notebook ID (it'll be the most recent one)
        time.sleep(2)
        notebooks = nlm_json(["notebook", "list"])
        if not notebooks:
            print(f"  ERROR: Could not list notebooks")
            continue

        # Find our notebook by title
        nb = next((n for n in notebooks if n["title"] == notebook_title), None)
        if not nb:
            # Fallback: most recent
            nb = notebooks[0]
        notebook_id = nb["id"]
        print(f"  Notebook: {notebook_id}")

        # 4. Add source
        try:
            nlm_run(["source", "add", notebook_id, "--file", temp_path, "--title", "Lesson Material", "--wait"], timeout=60)
        except Exception as e:
            # May crash on Windows encoding but still succeed
            pass

        time.sleep(2)

        # 5. Verify source was added
        sources = nlm_json(["source", "list", notebook_id])
        if not sources:
            print(f"  WARNING: Could not verify source was added, proceeding anyway")

        # 6. Check no video already generating for this notebook
        status = nlm_json(["studio", "status", notebook_id])
        if status and any(s.get("status") == "in_progress" for s in status):
            print(f"  SKIP: Video already in progress for this notebook")
            continue

        # 7. Build focus prompt and create cinematic video + podcast
        focus = build_focus_prompt(lesson, entry["subject_name"], entry["unit_name"], entry["exam_board"])

        try:
            nlm_run(["video", "create", notebook_id, "--format", "cinematic", "--focus", focus, "--confirm"], timeout=60)
        except Exception:
            pass

        time.sleep(2)

        # Also generate podcast audio from the same notebook
        try:
            nlm_run(["audio", "create", notebook_id, "--focus", focus, "--confirm"], timeout=60)
        except Exception:
            pass

        time.sleep(2)

        # 8. Get artifact IDs (video + audio)
        status = nlm_json(["studio", "status", notebook_id])
        video_artifact_id = None
        audio_artifact_id = None
        if status:
            for s in status:
                if s.get("type") == "video" and s.get("status") in ("in_progress", "completed") and not video_artifact_id:
                    video_artifact_id = s["id"]
                elif s.get("type") == "audio" and s.get("status") in ("in_progress", "completed") and not audio_artifact_id:
                    audio_artifact_id = s["id"]

        # 9. Save to state
        job = {
            "lesson_id": lesson["id"],
            "lesson_title": lesson["title"],
            "label": label,
            "notebook_id": notebook_id,
            "notebook_title": notebook_title,
            "artifact_id": video_artifact_id,
            "audio_artifact_id": audio_artifact_id,
            "status": "in_progress",
        }
        state["jobs"].append(job)
        save_state(state)

        created += 1
        print(f"  LAUNCHED (artifact: {artifact_id})")

        # Brief pause between creates
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

        # Mark complete only when both are done (or audio wasn't requested)
        if vid_done and (aud_done or not job.get("audio_artifact_id")):
            job["status"] = "completed"
            completed += 1
            print(f"  {job['label']}: COMPLETED (video + podcast)")
        else:
            still_going += 1
            vid_status = vid.get("status", "unknown") if vid else "unknown"
            aud_status = aud.get("status", "unknown") if aud else "n/a"
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
    parser = argparse.ArgumentParser(description="Generate cinematic video overviews via NotebookLM CLI")
    parser.add_argument("--limit", type=int, default=20, help="Max lessons to process (default: 20)")
    parser.add_argument("--subject", help="Only process a specific subject slug")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated without doing it")
    parser.add_argument("--status", action="store_true", help="Check status of in-progress jobs")
    parser.add_argument("--download", action="store_true", help="Download completed videos")
    parser.add_argument("--cleanup", action="store_true", help="Delete notebooks after downloading")
    args = parser.parse_args()

    if args.status:
        cmd_status(args)
    elif args.download:
        cmd_download(args)
    else:
        cmd_generate(args)


if __name__ == "__main__":
    main()
