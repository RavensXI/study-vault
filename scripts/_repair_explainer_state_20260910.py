# -*- coding: utf-8 -*-
"""One-off repair, 10 Sep 2026. The explainer state file was truncated mid-write (a --refire-missing
run was killed by a shell timeout while save_state() was writing), losing the tail ~850 job records
including the 36 in_progress jobs launched 9 Sep 18:02-18:07. Downloaded records are harmless to
lose (those lessons carry a video URL and are never re-queued). This rebuilds the in_progress
records by matching the NotebookLM notebooks that still exist against the lessons that are still
pending, so tonight's run re-fires on the EXISTING notebooks instead of creating 36 duplicates.
Read-only against Supabase; writes only scripts/_batch_explainer_state.json (backup taken first)."""
import json, os, re, shutil, sys, time, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import batch_explainer_videos as B

STATE = os.path.join(B.SCRIPT_DIR, "_batch_explainer_state.json")
NB_LIST = os.path.join(B.SCRIPT_DIR, "_explainer_daily_logs", "_nlm_notebooks_20260910.json")
shutil.copy(STATE, STATE + ".bak-20260910-prerepair")

state = B.load_state()
known = {j["notebook_id"] for j in state["jobs"]}
known_lessons = {j["lesson_id"] for j in state["jobs"] if j.get("status") == "in_progress"}
notebooks = json.load(open(NB_LIST, encoding="utf-8"))

sb = B.get_client()
pending = B.get_pending_lessons(sb, 2000)   # every lesson without a video, with names + unit context
by_title = {}
for e in pending:
    l = e["lesson"]
    t = f"{e['subject_name']} - {e['unit_name']} - L{l['lesson_number']:02d} - {l['title']} [explainer]"
    by_title[t] = e

launched = datetime.datetime(2026, 9, 9, 18, 2).timestamp()
added = 0
for nb in notebooks:
    if nb["id"] in known:
        continue
    e = by_title.get(nb["title"])
    if not e:
        continue
    l = e["lesson"]
    if l["id"] in known_lessons:
        continue
    focus = B.build_explainer_focus(l, e["subject_name"], e["unit_name"], e.get("exam_board"), e.get("unit_lessons"))
    state["jobs"].append({
        "lesson_id": l["id"],
        "label": f"{e['subject_slug']}/{e['unit_slug']}/L{l['lesson_number']:02d}",
        "notebook_id": nb["id"],
        "artifact_id": None,
        "status": "in_progress",
        "focus": focus,
        "launched_ts": launched,
        "repaired": "2026-09-10 rebuilt from NLM notebook list after state-file truncation",
    })
    added += 1
B.save_state(state)
print(f"pending lessons {len(pending)}; notebooks {len(notebooks)}; in_progress records rebuilt {added}")
