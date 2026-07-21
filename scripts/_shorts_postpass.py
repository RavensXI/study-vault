"""Nightly shorts post-pass — runs after batch_short_videos.py inside
daily_shorts_build.ps1, so new shorts arrive in the feed with their recall
question and poster the same night they're banked.

Steps (delta-based, idempotent — safe to re-run any time):
  1. Fetch the QA'd question bank for every shorted lesson (_shorts_fetch_qbank).
  2. Find lessons whose shorts lack a valid question pick (new lessons, legacy
     kc_index=-1 "no fit" markers, and lessons previously mapped by the
     fallback heuristic — the model upgrades those next time it's available).
  3. Map them via `claude -p` (headless Claude Code on the subscription — the
     model step canNOT live in this process as an API call). If the CLI is
     missing/fails, a token-overlap heuristic fills in so the feed never lags;
     those lessons are tagged "src":"heuristic" and re-queued for the model.
  4. Merge into scratchpad/_shorts_picks.json, rebuild scripts/_shorts_questions.json.
  5. Extract poster frames for any short without one (_make_short_posters skips
     existing, so this is cheap when there's nothing new).

Usage:
    python scripts/_shorts_postpass.py                 # the nightly call
    python scripts/_shorts_postpass.py --skip-posters
    python scripts/_shorts_postpass.py --force-lessons <id>[,<id>]   # test hook
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
QBANK = os.path.join(ROOT, "scratchpad", "_shorts_qbank.json")
PICKS = os.path.join(ROOT, "scratchpad", "_shorts_picks.json")
CHUNK = 8            # lessons per claude -p call (same shape as the workflow batches)
CLAUDE_TIMEOUT = 600  # per chunk

MAP_PROMPT = """You are tagging GCSE revision shorts with recall questions.

Below is a JSON list of lessons. Each has:
- sections: the lesson's section headings in order
- short_topics: the shorts that exist for this lesson, each {topic (a section heading), topic_index}
- kcs: the lesson's knowledge-check questions, each {kc_index, q}

TASK: for EVERY entry in short_topics of EVERY lesson, choose the kc_index of the
knowledge-check question that best tests the material of that short's section
(match the topic heading to what the question asks about). Rules:
- exactly one pick per short_topic; use its topic_index verbatim
- prefer giving different topics different questions when fit is comparable, but fit beats variety
- if no question is a clean fit, still pick the closest one — NEVER refuse, NEVER use -1
- kc_index must be one of the given indices for THAT lesson

Output ONLY this JSON object — no markdown fences, no commentary:
{"results":[{"lesson_id":"...","picks":[{"topic_index":N,"kc_index":N}]}]}

LESSONS:
"""

STOPWORDS = frozenset(
    "the a an and or of to in on for with what which who how why is are was were "
    "does do did this that these those its it their there from by as at be".split())


def log(msg):
    print(msg, flush=True)


def run_step(script, *args):
    r = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SCRIPT_DIR, script), *args],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r


def load_json(path, default):
    try:
        return json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return default


def slim(lesson):
    return {"lesson_id": lesson["lesson_id"], "subject": lesson["subject"], "title": lesson["title"],
            "sections": lesson["sections"], "short_topics": lesson["short_topics"],
            "kcs": [{"kc_index": k, "q": kc["q"]} for k, kc in enumerate(lesson["kcs"])]}


def build_todo(qbank, picks_by_id, force_ids):
    todo = []
    for l in qbank:
        want = {t["topic_index"] for t in l["short_topics"] if t.get("topic_index") is not None}
        if not want or not l["kcs"]:
            continue
        r = picks_by_id.get(l["lesson_id"])
        covered = {p["topic_index"] for p in r["picks"] if p["kc_index"] >= 0} if r else set()
        needs_model = r is not None and r.get("src") == "heuristic"
        if l["lesson_id"] in force_ids or needs_model or (want - covered):
            todo.append(l)
    return todo


def tokens(s):
    return {w for w in re.findall(r"[a-z0-9']+", s.lower()) if w not in STOPWORDS}


def heuristic_map(lesson):
    """Greedy token-overlap assignment; prefers giving each topic a distinct KC."""
    kc_toks = [tokens(kc["q"]) for kc in lesson["kcs"]]
    used, picks = set(), []
    for t in lesson["short_topics"]:
        if t.get("topic_index") is None:
            continue
        tt = tokens(t["topic"] or "")
        scored = sorted(range(len(kc_toks)),
                        key=lambda k: (len(tt & kc_toks[k]), -(k in used), -k), reverse=True)
        fresh = [k for k in scored if k not in used]
        best = fresh[0] if fresh else scored[0]
        used.add(best)
        picks.append({"topic_index": t["topic_index"], "kc_index": best})
    return {"lesson_id": lesson["lesson_id"], "picks": picks, "src": "heuristic"}


def resolve_claude():
    """Locate the claude CLI without depending on PATH.

    The scheduled task runs with a bare environment in which %APPDATA%\\npm is
    not on PATH, so shutil.which("claude") returned nothing and every night's
    mapping fell back to the heuristic. Check an explicit override, then PATH,
    then the npm global install locations. Prefer claude.cmd on Windows: the
    extensionless shim is a shell script that subprocess.run cannot exec.
    """
    override = os.environ.get("CLAUDE_CLI")
    if override and os.path.isfile(override):
        return override
    for name in ("claude.cmd", "claude.exe", "claude") if sys.platform == "win32" else ("claude",):
        found = shutil.which(name)
        if found:
            return found
    candidates = []
    for base in (os.environ.get("APPDATA"), os.environ.get("USERPROFILE")):
        if not base:
            continue
        candidates += [
            os.path.join(base, "npm", "claude.cmd"),
            os.path.join(base, "AppData", "Roaming", "npm", "claude.cmd"),
        ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def subscription_env():
    """Child env with the API key removed so the CLI uses the Claude Code
    subscription, which is what this step is documented to run on. Leaving
    ANTHROPIC_API_KEY set silently bills API credits for every mapping call,
    against Tom's standing preference; if the subscription login is not present
    in the task context the call just fails and the heuristic covers it -- same
    outcome as before, but never a surprise on the bill."""
    env = os.environ.copy()
    for k in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"):
        env.pop(k, None)
    return env


def claude_map(chunk_lessons):
    """One headless `claude -p` call for a chunk of lessons. Returns validated
    results list or None (caller falls back to the heuristic)."""
    exe = resolve_claude()
    if not exe:
        log("  [postpass] claude CLI not found (PATH, $CLAUDE_CLI, npm global) - using heuristic fallback")
        return None
    prompt = MAP_PROMPT + json.dumps([slim(l) for l in chunk_lessons], ensure_ascii=False)
    try:
        r = subprocess.run([exe, "-p", "--model", "sonnet"], input=prompt,
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=CLAUDE_TIMEOUT, env=subscription_env())
    except (subprocess.TimeoutExpired, OSError) as ex:
        log(f"  [postpass] claude -p failed ({ex.__class__.__name__}) - heuristic fallback")
        return None
    if r.returncode != 0:
        log(f"  [postpass] claude -p exit {r.returncode} - heuristic fallback")
        return None
    m = re.search(r"\{.*\}", r.stdout, re.S)
    if not m:
        log("  [postpass] no JSON in claude output - heuristic fallback")
        return None
    try:
        results = json.loads(m.group(0))["results"]
    except (ValueError, KeyError, TypeError):
        log("  [postpass] unparseable claude output - heuristic fallback")
        return None

    by_id = {l["lesson_id"]: l for l in chunk_lessons}
    ok = []
    for res in results:
        l = by_id.get(res.get("lesson_id"))
        if not l:
            continue
        want = {t["topic_index"] for t in l["short_topics"] if t.get("topic_index") is not None}
        got = {p["topic_index"] for p in res.get("picks", [])
               if isinstance(p.get("kc_index"), int) and 0 <= p["kc_index"] < len(l["kcs"])}
        if want <= got:
            ok.append({"lesson_id": res["lesson_id"],
                       "picks": [p for p in res["picks"] if p["topic_index"] in want]})
    return ok  # lessons the model missed/mangled just stay in the todo shape


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-posters", action="store_true")
    ap.add_argument("--force-lessons", default="", help="comma-separated lesson_ids to re-map (test hook)")
    args = ap.parse_args()
    force_ids = {x for x in args.force_lessons.split(",") if x}

    # 1. refresh the question bank
    r = run_step("_shorts_fetch_qbank.py")
    first = (r.stdout or "").strip().splitlines()
    log(f"[postpass] qbank: {first[0] if first else 'no output'}" + ("" if r.returncode == 0 else f" (EXIT {r.returncode})"))
    if r.returncode != 0:
        log((r.stderr or "")[-400:])
        sys.exit(1)

    qbank = load_json(QBANK, {"lessons": []})["lessons"]
    picks = load_json(PICKS, {"results": []})
    picks_by_id = {x["lesson_id"]: x for x in picks["results"]}

    # 2. what needs mapping?
    todo = build_todo(qbank, picks_by_id, force_ids)
    log(f"[postpass] {len(todo)} lesson(s) need question mapping")

    # 3. map: claude -p per chunk, heuristic for whatever that doesn't cover
    n_model = n_heur = 0
    for i in range(0, len(todo), CHUNK):
        chunk = todo[i:i + CHUNK]
        results = claude_map(chunk) or []
        mapped = {res["lesson_id"] for res in results}
        for res in results:
            res.pop("src", None)          # model picks carry no src tag
            picks_by_id[res["lesson_id"]] = res
            n_model += 1
        for l in chunk:
            if l["lesson_id"] not in mapped:
                picks_by_id[l["lesson_id"]] = heuristic_map(l)
                n_heur += 1
    if todo:
        picks["results"] = list(picks_by_id.values())
        json.dump(picks, open(PICKS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        log(f"[postpass] mapped: {n_model} by model, {n_heur} by heuristic (re-queued for model)")

    # 4. rebuild the questions file the feed loads
    r = run_step("_shorts_assemble_questions.py")
    log(f"[postpass] assemble: {(r.stdout or '').strip().splitlines()[0] if r.stdout else 'no output'}"
        + ("" if r.returncode == 0 else f" (EXIT {r.returncode})"))

    # 5. posters for anything new
    if not args.skip_posters:
        r = run_step("_make_short_posters.py")
        lines = (r.stdout or "").splitlines()
        n_ok = sum(1 for x in lines if x.startswith("  ok"))
        n_skip = sum(1 for x in lines if x.startswith("  skip"))
        fails = [x.strip() for x in lines if "FAIL" in x]
        log(f"[postpass] posters: {n_ok} new, {n_skip} existing, {len(fails)} failed")
        for x in fails[:5]:
            log("  " + x)

    log("[postpass] done")


if __name__ == "__main__":
    main()
