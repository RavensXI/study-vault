"""
Batch NotebookLM explainer-video generator for free-tier article lessons.

Mirror of batch_podcasts.py but for `nlm video create --format explainer`.
Stores the resulting MP4 in R2 (studyvault-video) and writes the public URL
into lessons.youtube_video_id (replacing the cinematic slot for free-tier).

Skips practice units (settings.practice_units list) and Unity-only subjects.

State file: _batch_explainer_state.json (separate from podcast state — no race).

Usage:
    python scripts/batch_explainer_videos.py --subject hospitality-catering
    python scripts/batch_explainer_videos.py --daily-cap 180
    python scripts/batch_explainer_videos.py --status
    python scripts/batch_explainer_videos.py --download --cleanup
    python scripts/batch_explainer_videos.py --dry-run --limit 10
"""

import argparse
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
from lib.r2 import get_r2_client, VIDEO_BUCKET, VIDEO_PUBLIC_URL

STATE_FILE = os.path.join(SCRIPT_DIR, "_batch_explainer_state.json")
DOWNLOAD_DIR = os.path.join(SCRIPT_DIR, "_explainer_videos")
NLM_ENV = {**os.environ, "NO_COLOR": "1", "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}


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
    c = c.replace('—', ' - ').replace('–', '-').replace('’', "'")
    c = c.replace('“', '"').replace('”', '"')
    c = re.sub(r'\\\(.*?\\\)', '', c)
    c = re.sub(r'\$\$.*?\$\$', '', c)
    c = re.sub(r'\n{3,}', '\n\n', c)
    c = re.sub(r'[ \t]+', ' ', c)
    return '\n'.join(line.strip() for line in c.split('\n')).strip()


def build_explainer_focus(lesson, subject_name, unit_name, exam_board, unit_lessons):
    n = lesson["lesson_number"]
    total = len(unit_lessons)
    ordinal = {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")

    lesson_list = []
    for ul in unit_lessons:
        num = ul["lesson_number"]
        marker = " <-- THIS LESSON" if num == n else " (covered)" if num < n else " (upcoming)"
        lesson_list.append(f"{num}. {ul['title']}{marker}")

    return (
        f"This is an explainer video for the {ordinal} of {total} GCSE revision "
        f"lessons in the {unit_name} unit, for students studying {exam_board} "
        f"{subject_name}. The lesson is called \"{lesson['title']}\".\n\n"
        f"UNIT CONTEXT — here is where this lesson sits in the sequence:\n"
        + "\n".join(lesson_list) + "\n\n"
        f"The source titled \"Lesson Material\" is the focus of this video. Treat "
        f"lessons before this one as things students have already covered and "
        f"lessons after it as things still to come. Reference earlier topics as "
        f"assumed knowledge and tease future ones briefly, but do not teach "
        f"content from other lessons in detail — that is what those lessons are for.\n\n"
        f"TONE AND LANGUAGE:\n"
        f"- Clear, focused explanation suitable for a 15-16 year old GCSE student.\n"
        f"- Preserve key subject-specific terms students need for exams. Define "
        f"them when first introduced.\n"
        f"- Use relatable examples or analogies to make abstract concepts concrete.\n"
        f"- Stay anchored to the lesson content; don't drift into general overview.\n"
    )


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"jobs": []}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def has_explainer_video(lesson):
    """A lesson already has an explainer video if youtube_video_id points to studyvault-video R2."""
    url = lesson.get("youtube_video_id") or ""
    return "studyvault-video" in url or "pub-157a3979382e4f98b51f7f868078e5a3.r2.dev" in url


def _fetch_subject_lessons(sb, slug, subject, limit, all_pending):
    practice_units = set((subject.get('settings') or {}).get('practice_units') or [])
    units = sb.from_('units').select('id, name, slug').eq('subject_id', subject['id']).order('sort_order').execute()
    for unit in (units.data or []):
        if unit['slug'] in practice_units:
            continue
        all_unit_lessons = sb.from_('lessons').select(
            'id, title, lesson_number, content_html, youtube_video_id'
        ).eq('unit_id', unit['id']).order('lesson_number').execute()

        for lesson in (all_unit_lessons.data or []):
            if has_explainer_video(lesson):
                continue
            if not (lesson.get('content_html') or '').strip():
                continue  # No article body — skip practice/empty shells
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


def get_pending_lessons(sb, limit, subject_filter=None):
    """Free-tier only (school_id IS NULL). Optional subject filter.

    Without --subject filter, iterates subjects in ascending-remaining-count order
    so smaller subjects ship complete before larger ones.
    """
    all_pending = []
    query = sb.from_('subjects').select('id, name, slug, exam_board, settings').is_('school_id', 'null')
    if subject_filter:
        query = query.eq('slug', subject_filter)
    subjects = query.execute().data or []

    if not subject_filter:
        # Count pending per subject and sort ascending (smallest first)
        counts = []
        for subj in subjects:
            scratch = []
            _fetch_subject_lessons(sb, subj['slug'], subj, 10_000, scratch)
            if scratch:
                counts.append((len(scratch), subj))
        counts.sort(key=lambda x: x[0])
        subjects = [s for _, s in counts]

    for subj in subjects:
        _fetch_subject_lessons(sb, subj['slug'], subj, limit, all_pending)
        if len(all_pending) >= limit:
            break
    return all_pending[:limit]


def cmd_generate(args):
    sb = get_client()
    state = load_state()
    active_ids = {j["lesson_id"] for j in state["jobs"] if j.get("status") == "in_progress"}

    pending = get_pending_lessons(sb, args.limit, args.subject)
    pending = [p for p in pending if p["lesson"]["id"] not in active_ids]

    if not pending:
        print("No lessons pending explainer video generation!")
        return

    print(f"Generating explainer videos for {len(pending)} lessons")
    print("=" * 60)

    created = 0
    for entry in pending:
        lesson = entry["lesson"]
        label = f"{entry['subject_slug']}/{entry['unit_slug']}/L{lesson['lesson_number']:02d}"
        print(f"\n  {label}: {lesson['title']}")

        if args.dry_run:
            print(f"  [DRY RUN] Would create notebook + generate explainer video")
            created += 1
            continue

        content = strip_html(lesson["content_html"] or "")
        if not content.strip():
            print(f"  SKIP: empty content_html")
            continue

        safe_label = label.replace("/", "_")
        temp_path = os.path.join(SCRIPT_DIR, f"_temp_explainer_{safe_label}.txt")
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(content)

        notebook_title = f"{entry['subject_name']} - {entry['unit_name']} - L{lesson['lesson_number']:02d} - {lesson['title']} [explainer]"
        try:
            nlm_run(["notebook", "create", notebook_title])
        except Exception as e:
            print(f"  ERROR creating notebook: {e}")
            try:
                os.remove(temp_path)
            except OSError:
                pass
            continue

        time.sleep(2)
        notebooks = nlm_json(["notebook", "list"])
        nb = next((n for n in notebooks if n["title"] == notebook_title), None) if notebooks else None
        if not nb:
            print(f"  ERROR: Could not find notebook by title")
            try:
                os.remove(temp_path)
            except OSError:
                pass
            continue
        notebook_id = nb["id"]

        try:
            nlm_run(["source", "add", notebook_id, "--file", temp_path, "--title", "Lesson Material", "--wait"], timeout=90)
        except Exception as e:
            print(f"  WARN: source add raised: {str(e)[:120]}")

        try:
            os.remove(temp_path)
        except OSError:
            pass
        time.sleep(2)

        focus = build_explainer_focus(lesson, entry["subject_name"], entry["unit_name"],
                                       entry["exam_board"], entry["unit_lessons"])
        try:
            nlm_run(["video", "create", notebook_id, "--format", "explainer", "--focus", focus, "--confirm"], timeout=90)
        except Exception as e:
            print(f"  WARN: video create raised: {str(e)[:120]}")
        time.sleep(2)

        artifact_id = None
        status = nlm_json(["studio", "status", notebook_id])
        if status:
            for s in status:
                if s.get("type") == "video" and s.get("status") in ("in_progress", "completed"):
                    artifact_id = s["id"]
                    break

        state["jobs"].append({
            "lesson_id": lesson["id"],
            "label": label,
            "notebook_id": notebook_id,
            "artifact_id": artifact_id,
            "status": "in_progress",
        })
        save_state(state)
        created += 1
        print(f"  LAUNCHED (artifact: {artifact_id})")
        time.sleep(3)

    print(f"\n{'=' * 60}")
    print(f"Launched {created} explainer video generations")
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
            if s.get("type") == "video":
                print(f"  {job['label']}: {s['status']}")
                if s["status"] == "completed":
                    job["status"] = "completed"
                    job["artifact_id"] = s["id"]
                    completed += 1
                elif s["status"] == "failed":
                    # NLM gave up. Mark terminal so the poll loop and re-queue
                    # logic both move on. The lesson will surface in next dry-run.
                    job["status"] = "failed"
                break
    save_state(state)
    still_active = sum(1 for j in active if j.get("status") == "in_progress")
    failed = sum(1 for j in active if j.get("status") == "failed")
    print(f"\n{completed} newly completed, {still_active} still in progress, {failed} failed")


def cmd_download(args):
    sb = get_client()
    r2 = get_r2_client()
    state = load_state()
    completed = [j for j in state["jobs"] if j.get("status") == "completed"]

    if not completed:
        print("No completed jobs to download.")
        return

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    print(f"Downloading {len(completed)} explainer videos...\n")
    downloaded = 0

    for job in completed:
        label = job["label"]
        notebook_id = job["notebook_id"]
        artifact_id = job.get("artifact_id")

        try:
            parts = label.split("/")
            video_filename = f"{label.replace('/', '_')}_explainer.mp4"
            video_path = os.path.join(DOWNLOAD_DIR, video_filename)
            if os.path.exists(video_path):
                os.remove(video_path)

            nlm_run([
                "download", "video", notebook_id,
                "--id", artifact_id,
                "--output", video_path,
                "--no-progress",
            ], timeout=600)

            if not os.path.exists(video_path) or os.path.getsize(video_path) == 0:
                print(f"  {label}: Download failed (empty/missing file)")
                continue

            r2_key = f"{parts[0]}/{parts[1]}/explainer_{parts[2].lower()}.mp4"
            with open(video_path, "rb") as f:
                r2.put_object(Bucket=VIDEO_BUCKET, Key=r2_key, Body=f.read(), ContentType="video/mp4")
            video_url = f"{VIDEO_PUBLIC_URL}/{r2_key}"

            sb.table("lessons").update({"youtube_video_id": video_url}).eq("id", job["lesson_id"]).execute()

            os.remove(video_path)
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
            print(f"  {label}: ERROR — {str(e)[:200]}")

    print(f"\nDownloaded {downloaded}/{len(completed)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=200, help="Max lessons to queue (default 200)")
    parser.add_argument("--daily-cap", type=int, dest="daily_cap", help="Cap based on remaining 200/day quota — convenience alias for --limit")
    parser.add_argument("--subject", help="Free-tier subject slug to target")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--cleanup", action="store_true")
    args = parser.parse_args()

    if args.daily_cap and not (args.status or args.download):
        args.limit = args.daily_cap

    if args.status:
        cmd_status(args)
    elif args.download:
        cmd_download(args)
    else:
        cmd_generate(args)


if __name__ == "__main__":
    main()
