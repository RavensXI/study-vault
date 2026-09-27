"""Re-walk every practice-walk correction applied on 27 Sep 2026, blind, one subject row at a time:
extract only the corrected questions, a fresh student answers them, the page marks, the examiner
judges anything marked wrong. Summary -> scripts/_studentwalk_fixcheck_practice.json

  python scripts/_studentwalk_fixcheck_practice.py
"""
import json, os, subprocess, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SUBJECTS = {s["slug"] + ("-unity" if s["school_id"] else ""): s for s in
            json.load(open(os.path.join(HERE, "_studentwalk_practice_subjects.json"), encoding="utf-8"))}
drafts = json.load(open(os.path.join(HERE, "_studentwalk_fixdrafts_practice.json"), encoding="utf-8"))
by_dir = defaultdict(list)
for k, d in drafts.items():
    if d.get("applied"):
        dr, key = k.split("::", 1)
        by_dir[dr].append(key)

summary = {}
for dr, keys in sorted(by_dir.items()):
    wd = os.path.join(HERE, "_studentwalk_fixcheck_" + dr)
    os.makedirs(wd, exist_ok=True)
    kf = os.path.join(wd, "keys.json")
    json.dump(keys, open(kf, "w"))
    env = dict(os.environ, PYTHONIOENCODING="utf-8", SV_QA_BASE="http://127.0.0.1:8910", SV_WALK_BUDGET="100000",
               SV_WALK_SID=SUBJECTS[dr]["id"], SV_WALK_DIR=wd)

    def run(*args, extra=None):
        r = subprocess.run([sys.executable, os.path.join(HERE, "_qa_student_walk.py")] + list(args),
                           env=dict(env, **(extra or {})), capture_output=True, text=True, encoding="utf-8")
        return ([l for l in (r.stdout + r.stderr).splitlines() if l.strip()] or [""])[-1]

    print("#### %s (%d)" % (dr, len(keys)), flush=True)
    for step in (("extract", "--keys", kf), ("attempt-sub", "--no-ai"), ("attempt-sub", "--no-ai")):
        print("  ", run(*step), flush=True)
    print("  ", run("attempt-sub", "--no-ai", extra={"SV_WALK_CHUNK": "1"}), flush=True)
    print("  ", run("mark", "--no-ai"), flush=True)
    print("  ", run("adjudicate", "--sub", "--no-ai"), flush=True)
    L = lambda f: json.load(open(os.path.join(wd, f + ".json"), encoding="utf-8")) if os.path.exists(os.path.join(wd, f + ".json")) else {}
    m, a = L("marks"), L("adjudications")
    summary[dr] = {"corrected": len(keys), "walked": len(m),
                   "right": sum(1 for x in m.values() if x.get("verdict") == "right"),
                   "findings": {k: (x or {}).get("finding") for k, x in a.items()}}
    json.dump(summary, open(os.path.join(HERE, "_studentwalk_fixcheck_practice.json"), "w", encoding="utf-8"), indent=1)
    print("   %(walked)d walked, %(right)d right" % summary[dr], flush=True)
print("done")
