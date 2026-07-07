"""
Hardened batch generator for NotebookLM SHORT-FORM videos (nlm video create --format short).

Built to run UNATTENDED once per day and reliably produce the day's output. It is a
single self-contained loop (generate -> poll -> download -> R2 -> delete notebook),
not the three-manual-phase design of batch_explainer_videos.py / batch_podcasts.py
(which is why those stall when run headless).

Hardening baked in (from the scars of the podcast/explainer batches):
  * SINGLE-INSTANCE LOCK          — no overlapping runs => no state-file race.
  * WAVE PROCESSING              — only WAVE_SIZE notebooks alive at once, each deleted
                                    the moment its video downloads => never hits NotebookLM's
                                    notebook cap.
  * STARTUP SWEEP               — deletes orphaned "SVSHORT" notebooks left by a crashed run.
  * FAIL-SAFE AUTH              — detects expiry and EXITS CLEANLY (never launches the
                                    interactive `nlm login`, which hangs a headless run).
  * "unknown" != failed         — treated as still-processing until a per-video timeout.
  * DATE-STAMPED DAILY QUOTA     — respects the ~180/day cap across re-runs on the same day.
  * APPEND-ONLY MANIFEST         — the durable record of finished shorts; also the "done" set,
                                    so it's inherently resumable and race-free.
  * MIXED SELECTION             — round-robins across subjects so each day's batch is a
                                    diverse feed, not one subject at a time.

Storage: MP4 -> R2 studyvault-video at shorts/{subject}/{unit}/L{NN}.mp4.
         Record -> scripts/_shorts_manifest.json  (the lessons table is NOT touched — shorts
         are a separate feed from the explainer/cinematic youtube_video_id slot).

Usage:
    python scripts/batch_short_videos.py                      # one day's run, default cap
    python scripts/batch_short_videos.py --daily-cap 180
    python scripts/batch_short_videos.py --subject science-edexcel
    python scripts/batch_short_videos.py --dry-run --limit 20
    python scripts/batch_short_videos.py --status            # show progress + today's count
    python scripts/batch_short_videos.py --sweep-only        # just clear orphan notebooks
"""

import argparse
import datetime
import html as html_mod
import json
import os
import re
import subprocess
import sys
import tempfile
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
from lib.r2 import get_r2_client, VIDEO_BUCKET, VIDEO_PUBLIC_URL

# ── config ──────────────────────────────────────────────────────────────────
NLM_ENV = {**os.environ, "NO_COLOR": "1", "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
NB_PREFIX = "SVSHORT"                                   # marks our notebooks (sweep target)
MANIFEST = os.path.join(SCRIPT_DIR, "_shorts_manifest.json")
DAILY_FILE = os.path.join(SCRIPT_DIR, "_shorts_daily.json")
LOCK_FILE = os.path.join(SCRIPT_DIR, "_batch_short.lock")
DOWNLOAD_DIR = os.path.join(tempfile.gettempdir(), "sv_shorts_dl")   # nlm refuses to write under Documents/profile
DEFAULT_CAP = 180                                       # videos/day (safe margin under the 200 quota)
MAX_PER_LESSON = 4                                      # focused shorts per lesson (one per section, capped)
WAVE_SIZE = 6                                           # LESSONS (=notebooks) alive at once; ~WAVE_SIZE*4 videos in flight
PER_VIDEO_TIMEOUT = 40 * 60                             # give up on a single video after this
POLL_INTERVAL = 30
LOCK_STALE_SECS = 6 * 3600                              # reclaim a lock older than this


class AuthExpired(Exception):
    pass


# ── nlm CLI (hardened: NO interactive re-login) ─────────────────────────────
def nlm_run(args, timeout=120):
    try:
        result = subprocess.run(
            ["nlm"] + args, capture_output=True, text=True,
            encoding="utf-8", errors="replace", env=NLM_ENV, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"nlm {args[0] if args else ''} timed out after {timeout}s")
    output = (result.stdout or "") + (result.stderr or "")
    if "Authentication expired" in output or "Authentication Error" in output:
        raise AuthExpired()                            # bubble up — caller exits cleanly
    if result.returncode != 0 and "Error" in (result.stderr or ""):
        raise RuntimeError(f"nlm {' '.join(args[:3])} failed: {result.stderr[:200]}")
    return result.stdout.strip()


def nlm_json(args, timeout=120):
    out = nlm_run(args, timeout)
    for a, b in (("[", "]"), ("{", "}")):
        i = out.find(a)
        if i >= 0:
            j = out.rfind(b)
            if j > i:
                try:
                    return json.loads(out[i:j + 1])
                except json.JSONDecodeError:
                    return None
    return None


def auth_ok():
    try:
        nlm_json(["notebook", "list"])
        return True
    except AuthExpired:
        return False


# ── small state helpers (append-only manifest = source of truth) ────────────
def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return default
    return default


def save_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)                              # atomic


def done_lesson_ids():
    return {e["lesson_id"] for e in load_json(MANIFEST, [])}


def done_topics_by_lesson():
    """{lesson_id: set(topic_index)} — which shorts each lesson already has (1-based).
    A lesson is only 'done' once it has ALL its expected shorts; partial lessons re-queue
    and get topped up with just the missing sections."""
    d = {}
    for e in load_json(MANIFEST, []):
        d.setdefault(e["lesson_id"], set()).add(e.get("topic_index"))
    return d


def append_manifest(entry):
    m = load_json(MANIFEST, [])
    m.append(entry)
    save_json(MANIFEST, m)


def bump_daily(n=1):
    today = datetime.date.today().isoformat()
    d = load_json(DAILY_FILE, {})
    d = {k: v for k, v in d.items() if k == today}      # drop old days
    d[today] = d.get(today, 0) + n
    save_json(DAILY_FILE, d)
    return d[today]


def today_count():
    today = datetime.date.today().isoformat()
    return load_json(DAILY_FILE, {}).get(today, 0)


# ── single-instance lock ────────────────────────────────────────────────────
def _pid_alive(pid):
    try:
        if sys.platform == "win32":
            out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True).stdout
            return str(pid) in out
        os.kill(pid, 0)
        return True
    except Exception:
        return False


def acquire_lock():
    if os.path.exists(LOCK_FILE):
        info = load_json(LOCK_FILE, {})
        pid, ts = info.get("pid"), info.get("ts", 0)
        if pid and _pid_alive(pid) and (time.time() - ts) < LOCK_STALE_SECS:
            print(f"Another run is active (pid {pid}). Exiting."); sys.exit(0)
        print("Reclaiming stale lock.")
    save_json(LOCK_FILE, {"pid": os.getpid(), "ts": time.time()})


def release_lock():
    try:
        os.remove(LOCK_FILE)
    except OSError:
        pass


# ── notify (best-effort email via Resend; never blocks the run) ─────────────
def notify(subject, body):
    key, to, frm = os.environ.get("RESEND_API_KEY"), os.environ.get("NOTIFY_TO"), os.environ.get("NOTIFY_FROM")
    if not (key and to and frm):
        return
    try:
        import urllib.request
        req = urllib.request.Request(
            "https://api.resend.com/emails",
            data=json.dumps({"from": frm, "to": [to], "subject": subject, "text": body}).encode(),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=20)
    except Exception:
        pass


# ── content ─────────────────────────────────────────────────────────────────
def strip_html(content_html):
    c = content_html or ""
    c = re.sub(r'<figure class="diagram">.*?</figure>', "", c, flags=re.DOTALL)
    c = re.sub(r"<img[^>]*>", "", c)
    c = re.sub(r"<h2[^>]*>(.*?)</h2>", r"\n\n## \1\n", c)
    c = re.sub(r"<h3[^>]*>(.*?)</h3>", r"\n### \1\n", c)
    c = re.sub(r"<li>(.*?)</li>", r"- \1", c, flags=re.DOTALL)
    c = re.sub(r"<[^>]+>", "", c)
    c = html_mod.unescape(c)
    c = c.replace("—", " - ").replace("–", "-").replace("’", "'").replace("“", '"').replace("”", '"')
    c = re.sub(r"\\\(.*?\\\)", "", c)
    c = re.sub(r"\$\$.*?\$\$", "", c)
    c = re.sub(r"\n{3,}", "\n\n", c)
    c = re.sub(r"[ \t]+", " ", c)
    return "\n".join(line.strip() for line in c.split("\n")).strip()


def extract_topics(content_html, max_n=MAX_PER_LESSON):
    """The lesson's own section headings ARE its non-overlapping topics. Prefer <h2>;
    if there are too few, fall back to <h3>. Returns up to max_n topic strings."""
    heads = re.findall(r"<h2[^>]*>(.*?)</h2>", content_html or "", re.S | re.I)
    if len(heads) < 2:
        heads += re.findall(r"<h3[^>]*>(.*?)</h3>", content_html or "", re.S | re.I)
    topics = []
    for h in heads:
        t = html_mod.unescape(re.sub(r"<[^>]+>", "", h)).strip()
        if t and t.lower() not in ("key fact", "overview") and t not in topics:
            topics.append(t)
    return topics[:max_n]


def build_section_focus(title, section, subject_name, unit_name, exam_board, all_sections):
    others = [s for s in all_sections if s != section]
    other_note = (f" Companion shorts cover: {', '.join(others)} — do NOT cover those." if others else "")
    return (
        f"Make a punchy ~60-second SHORT-FORM revision video for a 15-16 year old GCSE {exam_board} {subject_name} "
        f"student. It's one of a set of shorts for the lesson \"{title}\" ({unit_name} unit). "
        f"This one must focus ONLY on: \"{section}\".{other_note} "
        f"The source \"Lesson Material\" is the full lesson for context, but cover ONLY \"{section}\". "
        f"Hook in 3 seconds; 1-2 exam-critical points; energetic and simple; keep and define key exam terms fast."
    )


def build_general_focus(title, subject_name, unit_name, exam_board):
    return (
        f"Make a punchy ~60-second SHORT-FORM revision video for a 15-16 year old GCSE {exam_board} {subject_name} "
        f"student, on the lesson \"{title}\" ({unit_name} unit). The source \"Lesson Material\" is the content. "
        f"Hook in 3 seconds; the 2-3 most exam-critical ideas only; energetic and simple; define key terms fast."
    )


def topic_from_instructions(custom_instructions, topics):
    """The artifact echoes its focus prompt in custom_instructions, so we label each short by
    its ACTUAL topic (status order isn't creation order, so this beats positional guessing)."""
    m = re.search(r'focus ONLY on: "([^"]+)"', custom_instructions or "")
    return m.group(1) if m else (topics[0] if topics else "overview")


def get_pending_mixed(sb, subject_filter, limit):
    """Free-tier lessons with a real article body and no short yet, ROUND-ROBINED across
    subjects so a day's batch is a diverse feed. Returns list of entry dicts."""
    have = done_topics_by_lesson()
    q = sb.from_("subjects").select("id, name, slug, exam_board, settings").is_("school_id", "null")
    if subject_filter:
        q = q.eq("slug", subject_filter)
    subjects = q.execute().data or []

    per_subject = []                                    # list of queues, one per subject
    for subj in subjects:
        practice = set((subj.get("settings") or {}).get("practice_units") or [])
        units = sb.from_("units").select("id, name, slug").eq("subject_id", subj["id"]).order("sort_order").execute().data or []
        queue = []
        for unit in units:
            if unit["slug"] in practice:
                continue
            lessons = sb.from_("lessons").select("id, title, lesson_number, content_html").eq(
                "unit_id", unit["id"]).order("lesson_number").execute().data or []
            for L in lessons:
                html = L.get("content_html") or ""
                if not html.strip():
                    continue
                hv = have.get(L["id"], set())
                expected = len(extract_topics(html)) or 1     # min(sections,4), or 1 if no headings
                if None in hv or len(hv) >= expected:          # None = legacy 1-general-short lesson (leave as-is)
                    continue                                   # else: fully covered -> skip; partial -> re-queue
                queue.append({
                    "lesson_id": L["id"], "title": L["title"], "lesson_number": L["lesson_number"],
                    "content_html": L["content_html"], "subject_slug": subj["slug"],
                    "subject_name": subj["name"], "unit_slug": unit["slug"], "unit_name": unit["name"],
                    "exam_board": subj.get("exam_board") or "AQA",
                })
        if queue:
            per_subject.append(queue)

    # round-robin interleave
    mixed = []
    while per_subject and len(mixed) < limit:
        for queue in list(per_subject):
            if queue:
                mixed.append(queue.pop(0))
                if len(mixed) >= limit:
                    break
            if not queue:
                per_subject.remove(queue)
    return mixed


# ── notebook management ─────────────────────────────────────────────────────
def sweep_orphan_notebooks():
    """Delete any leftover SVSHORT notebooks (only reachable when no run is active, thanks
    to the lock — so every SVSHORT notebook here is an orphan from a crashed run)."""
    try:
        nbs = nlm_json(["notebook", "list"]) or []
    except AuthExpired:
        raise
    except Exception:
        return 0
    killed = 0
    for nb in nbs:
        if (nb.get("title") or "").startswith(NB_PREFIX):
            try:
                nlm_run(["notebook", "delete", nb["id"], "--confirm"], timeout=30)
                killed += 1
            except AuthExpired:
                raise
            except Exception:
                pass
    if killed:
        print(f"  swept {killed} orphan notebook(s)")
    return killed


def _find_video_artifact(notebook_id):
    st = nlm_json(["studio", "status", notebook_id]) or []
    for s in st:
        if s.get("type") == "video":
            return s.get("id"), s.get("status")
    return None, None


# ── one wave of LESSONS: each = 1 notebook with up to MAX_PER_LESSON focused shorts ──
def run_wave(sb, r2, wave, cap):
    # phase 1: per lesson, create a notebook, add the source once, trigger a focused short per section
    launched = []                                       # {e, nb_id, jobs:[{topic, idx, art_id, started}]}
    have_topics = done_topics_by_lesson()               # {lesson_id: set(topic_index)} already banked
    for e in wave:
        if today_count() >= cap:
            break
        content = strip_html(e["content_html"])
        if not content.strip():
            continue
        topics = extract_topics(e["content_html"])      # full ordered list; positions are the stable idx
        done_idx = have_topics.get(e["lesson_id"], set())   # 1-based indexes this lesson already has
        if topics:
            plan = [t for i, t in enumerate(topics) if (i + 1) not in done_idx]   # only the missing sections
        else:
            plan = [] if 1 in done_idx else [None]       # no headings -> one general short (idx 1)
        if not plan:                                    # nothing missing (guarded by pending filter, but be safe)
            continue
        temp = os.path.join(SCRIPT_DIR, f"_short_src_{e['lesson_id'][:8]}.txt")
        with open(temp, "w", encoding="utf-8") as f:
            f.write(f"{e['title']}\n\n{content}")
        nb_title = f"{NB_PREFIX} {e['subject_slug']} {e['unit_slug']} L{e['lesson_number']:02d}"
        try:
            nlm_run(["notebook", "create", nb_title])
            time.sleep(1.5)
            nbs = nlm_json(["notebook", "list"]) or []
            nb = next((n for n in nbs if n.get("title") == nb_title), None)
            if not nb:
                raise RuntimeError("notebook not found after create")
            nb_id = nb["id"]
            nlm_run(["source", "add", nb_id, "--file", temp, "--title", "Lesson Material", "--wait"], timeout=120)
        except AuthExpired:
            raise
        except Exception as ex:
            print(f"  ! {e['subject_slug']}/L{e['lesson_number']:02d}: setup failed — {str(ex)[:90]}")
            try: os.remove(temp)
            except OSError: pass
            continue
        try: os.remove(temp)
        except OSError: pass

        fired = []                                      # topics of successfully-fired shorts, in creation order
        for topic in plan:
            if today_count() >= cap:
                break
            focus = (build_section_focus(e["title"], topic, e["subject_name"], e["unit_name"], e["exam_board"], topics)
                     if topic else build_general_focus(e["title"], e["subject_name"], e["unit_name"], e["exam_board"]))
            try:
                nlm_run(["video", "create", nb_id, "--format", "short", "--focus", focus, "--confirm"], timeout=120)
                bump_daily(1)                            # each submission counts against the daily quota
                fired.append(topic or "overview")
                time.sleep(2)
            except AuthExpired:
                raise
            except Exception as ex:
                print(f"  ! {e['subject_slug']}/L{e['lesson_number']:02d} [{topic}]: create failed — {str(ex)[:70]}")
        if fired:
            launched.append({"e": e, "nb_id": nb_id, "topics": fired, "all_topics": topics,
                             "n": len(fired), "started": time.time()})
            print(f"  launched {e['subject_slug']}/{e['unit_slug']}/L{e['lesson_number']:02d}: {len(fired)} short(s)")
        else:
            _delete_nb(nb_id)
        time.sleep(2)

    # phase 2: poll each notebook and download whatever is 'completed', using its CURRENT id from a fresh
    # status each pass — NotebookLM re-IDs the artifact between pending and done, so never pre-capture ids.
    # Topic label is by collection order (refined later if the artifact exposes its focus).
    done_ct = 0
    for L in launched:
        e, nb_id, full_topics, n = L["e"], L["nb_id"], L["all_topics"], L["n"]
        got, handled = 0, set()                         # got = accounted (downloaded+failed); handled = terminal ids seen
        while got < n and time.time() - L["started"] < PER_VIDEO_TIMEOUT:
            try:
                vids = [s for s in (nlm_json(["studio", "status", nb_id]) or []) if s.get("type") == "video"]
            except AuthExpired:
                raise
            except Exception:
                vids = []
            for s in vids:
                aid, status = s.get("id"), s.get("status")
                if not aid or aid in handled:
                    continue
                if status == "completed":
                    topic = topic_from_instructions(s.get("custom_instructions"), full_topics)
                    idx = full_topics.index(topic) if topic in full_topics else got   # ORIGINAL section position -> fills the exact gap
                    if _download_and_store(sb, r2, e, nb_id, aid, idx, topic):
                        done_ct += 1
                    handled.add(aid); got += 1
                elif status in ("failed", "error"):
                    print(f"  x {e['subject_slug']}/L{e['lesson_number']:02d}: a short failed")
                    handled.add(aid); got += 1
            if got < n:
                time.sleep(POLL_INTERVAL)
        if got < n:
            print(f"  ~ {e['subject_slug']}/L{e['lesson_number']:02d}: {got}/{n} collected before timeout")
        _delete_nb(nb_id)                               # free the notebook
    return done_ct


def _delete_nb(nb_id):
    try:
        nlm_run(["notebook", "delete", nb_id, "--confirm"], timeout=30)
    except AuthExpired:
        raise
    except Exception:
        pass


def _download_and_store(sb, r2, e, nb_id, art_id, idx, topic):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    stem = f"{e['subject_slug']}_{e['unit_slug']}_L{e['lesson_number']:02d}_{idx + 1}"
    path = os.path.join(DOWNLOAD_DIR, stem + ".mp4")
    try:
        ok = False
        for attempt in range(2):
            nlm_run(["download", "video", nb_id, "--id", art_id, "--output", path, "--no-progress"], timeout=600)
            if os.path.exists(path) and os.path.getsize(path) >= 1024:
                ok = True; break
            time.sleep(5)
        if not ok:
            print(f"  x L{e['lesson_number']:02d} [{topic}]: empty download after retries"); return False
        key = f"shorts/{e['subject_slug']}/{e['unit_slug']}/L{e['lesson_number']:02d}_{idx + 1}.mp4"
        with open(path, "rb") as f:
            r2.put_object(Bucket=VIDEO_BUCKET, Key=key, Body=f.read(), ContentType="video/mp4")
        url = f"{VIDEO_PUBLIC_URL}/{key}"
        append_manifest({
            "lesson_id": e["lesson_id"], "subject": e["subject_slug"], "unit": e["unit_slug"],
            "lesson_number": e["lesson_number"], "title": e["title"], "topic": topic, "topic_index": idx + 1,
            "url": url, "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        })
        print(f"  ✓ {e['subject_slug']}/{e['unit_slug']}/L{e['lesson_number']:02d} [{topic}]  ({os.path.getsize(path)//1024} KB)")
        return True
    except AuthExpired:
        raise
    except Exception as ex:
        print(f"  x L{e['lesson_number']:02d} [{topic}]: store failed — {str(ex)[:110]}"); return False
    finally:
        try: os.remove(path)
        except OSError: pass


# ── commands ────────────────────────────────────────────────────────────────
def cmd_run(args):
    if not auth_ok():
        msg = "NotebookLM auth expired — run `nlm login`, then the daily batch will resume."
        print("AUTH EXPIRED. " + msg)
        notify("StudyVault shorts: auth expired", msg)
        sys.exit(2)

    print("sweeping orphan notebooks…")
    sweep_orphan_notebooks()

    cap = args.daily_cap or DEFAULT_CAP
    already = today_count()
    budget = max(0, cap - already)
    if budget == 0:
        print(f"Daily cap already reached ({already}/{cap}). Nothing to do."); return
    print(f"Today so far: {already}/{cap}. Budget this run: {budget}.")

    sb = get_client()
    # queue lessons (video budget is an upper bound on lessons needed; run_wave caps videos)
    pending = get_pending_mixed(sb, args.subject, args.limit or budget)
    if not pending:
        print("No pending lessons need a short. All done!"); return
    est = sum(min(len(extract_topics(e["content_html"])) or 1, MAX_PER_LESSON) for e in pending)
    print(f"{len(pending)} lessons queued (mixed across subjects), ~{est} shorts if all run.")
    if args.dry_run:
        for e in pending[:30]:
            n = min(len(extract_topics(e["content_html"])) or 1, MAX_PER_LESSON)
            print(f"  [DRY] {e['subject_slug']}/{e['unit_slug']}/L{e['lesson_number']:02d} — {n} short(s) — {e['title']}")
        print(f"  … {len(pending)} lessons total"); return

    r2 = get_r2_client()
    total_done = 0
    for i in range(0, len(pending), WAVE_SIZE):
        if today_count() >= cap:
            print("Hit daily cap mid-run — stopping cleanly."); break
        wave = pending[i:i + WAVE_SIZE]
        print(f"\n── wave {i // WAVE_SIZE + 1} ({len(wave)} lessons) ──")
        total_done += run_wave(sb, r2, wave, cap)

    summary = f"Shorts batch: {total_done} produced this run, {today_count()}/{cap} today, {len(done_lesson_ids())} total banked."
    print("\n" + summary)
    notify("StudyVault shorts: daily run complete", summary)


def cmd_status(args):
    m = load_json(MANIFEST, [])
    import collections
    by_subject = collections.Counter(e["subject"] for e in m)
    print(f"Shorts banked: {len(m)}")
    print(f"Today: {today_count()}")
    for s, n in by_subject.most_common():
        print(f"  {n:4d}  {s}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--daily-cap", type=int, default=None, help=f"Videos/day (default {DEFAULT_CAP})")
    p.add_argument("--limit", type=int, default=None, help="Cap this run's queue size")
    p.add_argument("--subject", help="Restrict to one free-tier subject slug")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--status", action="store_true")
    p.add_argument("--sweep-only", action="store_true", help="Just delete orphan SVSHORT notebooks")
    args = p.parse_args()

    if args.status:
        cmd_status(args); return

    acquire_lock()
    try:
        if args.sweep_only:
            if auth_ok():
                sweep_orphan_notebooks()
            else:
                print("Auth expired — run `nlm login`.")
            return
        cmd_run(args)
    except AuthExpired:
        msg = "Auth expired mid-run — progress saved, notebooks will be swept next run. Run `nlm login`."
        print("\n" + msg); notify("StudyVault shorts: auth expired mid-run", msg); sys.exit(2)
    finally:
        release_lock()


if __name__ == "__main__":
    main()
