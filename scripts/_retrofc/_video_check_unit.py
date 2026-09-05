"""Retro fact-check: run _video_check.py over every lesson of a finished unit and bank the regeneration worklist.

Usage: _video_check_unit.py <subject> <unit> [--force]
Spawned detached by `_unit.py finish` after a successful commit (skip with `finish ... --no-video`); also runnable
by hand, e.g. for the back-fill of units finished before 5 Sep 2026. Idempotent: lessons that already have
units/<subject>__<unit>/_video/L<n>.json are skipped unless --force.
Outputs: units/<subject>__<unit>/_video_check.json (unit summary), _video_check.log, and flagged lessons appended
to scripts/_retrofc/_video_regen_worklist.json (the list of explainer videos to regenerate; one entry per lesson,
replaced if re-checked). Uses the interpreter it is launched with (must be _venv_genai).
"""
import json, os, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
subject, unit = sys.argv[1], sys.argv[2]
force = "--force" in sys.argv
udir = os.path.join(HERE, "units", f"{subject}__{unit}")
os.makedirs(os.path.join(udir, "_video"), exist_ok=True)
log = open(os.path.join(udir, "_video_check.log"), "a", encoding="utf-8")


def say(s):
    log.write(f"{time.strftime('%H:%M:%S')} {s}\n"); log.flush(); print(s, flush=True)


U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}
get = lambda p: json.load(urllib.request.urlopen(urllib.request.Request(f"{U}/rest/v1/{p}", headers=H), timeout=60))
sid = get(f"subjects?slug=eq.{subject}&select=id")[0]["id"]
uid = get(f"units?subject_id=eq.{sid}&slug=eq.{unit}&select=id")[0]["id"]
rows = get(f"lessons?unit_id=eq.{uid}&select=lesson_number,youtube_video_id&order=lesson_number")
say(f"start {subject}/{unit}: {len(rows)} lessons")
results = []
for r in rows:
    n = r["lesson_number"]
    rp = os.path.join(udir, "_video", f"L{n}.json")
    if not (r["youtube_video_id"] and "r2.dev" in r["youtube_video_id"]):
        results.append({"lesson": n, "skipped": "no R2 video"}); continue
    if os.path.exists(rp) and not force:
        results.append(json.load(open(rp, encoding="utf-8"))); say(f"L{n} cached"); continue
    for attempt in (1, 2, 3):
        pr = subprocess.run([sys.executable, os.path.join(HERE, "_video_check.py"), subject, unit, str(n)],
                            capture_output=True, text=True, encoding="utf-8", cwd=HERE)
        if pr.returncode == 0 and os.path.exists(rp):
            res = json.load(open(rp, encoding="utf-8")); results.append(res)
            say(f"L{n} {res['cost_p']}p regenerate={res['regenerate']} MA={len(res['mark_affecting'])} ped={len(res['pedantry'])}")
            break
        err = (pr.stderr or pr.stdout or "")[-300:].replace("\n", " ")
        say(f"L{n} attempt {attempt} failed: {err}")
        if attempt == 3:
            results.append({"lesson": n, "error": err})
        else:
            time.sleep(30 * attempt)

checked = [x for x in results if "cost_p" in x]
flagged = [x for x in checked if x.get("regenerate")]
summary = {"subject": subject, "unit": unit, "checked_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "lessons": len(rows),
           "videos_checked": len(checked), "regenerate": len(flagged), "errors": sum(1 for x in results if "error" in x),
           "total_cost_p": round(sum(x["cost_p"] for x in checked), 1),
           "flagged": [{"lesson": x["lesson"], "title": x["title"], "reason": x["reason"], "mark_affecting": x["mark_affecting"]} for x in flagged]}
json.dump(summary, open(os.path.join(udir, "_video_check.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# bank the worklist (one entry per lesson, replaced on re-check)
wp = os.path.join(HERE, "_video_regen_worklist.json")
wl = json.load(open(wp, encoding="utf-8")) if os.path.exists(wp) else {"items": [], "units_checked": []}
wl["items"] = [i for i in wl["items"] if not (i["subject"] == subject and i["unit"] == unit)]
for x in flagged:
    wl["items"].append({"subject": subject, "unit": unit, "lesson": x["lesson"], "lesson_id": x["lesson_id"], "title": x["title"],
                        "video_url": x["video_url"], "reason": x["reason"], "mark_affecting": x["mark_affecting"], "checked_at": x["checked_at"]})
wl["units_checked"] = [u for u in wl["units_checked"] if not (u["subject"] == subject and u["unit"] == unit)]
wl["units_checked"].append({"subject": subject, "unit": unit, "videos": len(checked), "regenerate": len(flagged),
                            "cost_p": summary["total_cost_p"], "checked_at": summary["checked_at"]})
wl["totals"] = {"units": len(wl["units_checked"]), "videos": sum(u["videos"] for u in wl["units_checked"]),
                "regenerate": len(wl["items"]), "cost_p": round(sum(u["cost_p"] for u in wl["units_checked"]), 1)}
json.dump(wl, open(wp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
say(f"DONE {subject}/{unit}: {len(checked)} videos, {len(flagged)} to regenerate, {summary['total_cost_p']}p; worklist now {wl['totals']}")
