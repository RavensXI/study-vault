"""Re-mark tile answers after the exact-text tile fix (26 Sep 2026): the walk had clicked 'la' for 'La'."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
subs = {s["slug"] + ("-unity" if s["school_id"] else ""): s for s in json.load(open(os.path.join(HERE, "_studentwalk_practice_subjects.json")))}
for d in json.load(open(os.path.join(HERE, "_studentwalk_tile_remark.json"))):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", SV_QA_BASE="http://127.0.0.1:8910", SV_WALK_BUDGET="100000", SV_WALK_CHUNK="1",
               SV_WALK_SID=subs[d]["id"], SV_WALK_DIR=os.path.join(HERE, "_studentwalk_" + d))
    print("####", d, flush=True)
    for c in (["mark", "--no-ai"], ["adjudicate", "--sub", "--no-ai"], ["report"]):
        r = subprocess.run([sys.executable, os.path.join(HERE, "_qa_student_walk.py")] + c, env=env, capture_output=True, text=True, encoding="utf-8")
        print("  ", c[0], [l for l in (r.stdout + r.stderr).splitlines() if l.strip()][-1:], flush=True)
