"""Second pass over the practice walk (27 Sep 2026) after the walk's own entry faults were fixed:
LaTeX options (\\pounds, ^\\circ), answers sent as a JSON string, number boxes given a unit, and
screenshots taken mid-transition or before a map loaded. For every walked subject (music listening
questions aside: the student cannot hear them):
  - answers the page could not take (no verdict / not entered): mark and ruling dropped, re-marked;
  - answers the student could not give because the screenshot was unreadable: shot retaken, asked again.
Then re-mark, re-judge, report.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SUBJECTS = {s["slug"] + ("-unity" if s["school_id"] else ""): s for s in
            json.load(open(os.path.join(HERE, "_studentwalk_practice_subjects.json"), encoding="utf-8"))}
SHOT_WORDS = re.compile(r"screenshot|blank|overlap|on top of each other|too (small|tiny|blurry)|cannot (see|read)|can't (see|read)|not visible|unreadable|cut off", re.I)


def run(d, *args, extra=None):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", SV_QA_BASE="http://127.0.0.1:8910", SV_WALK_BUDGET="100000",
               SV_WALK_SID=SUBJECTS[d]["id"], SV_WALK_DIR=os.path.join(HERE, "_studentwalk_" + d), **(extra or {}))
    r = subprocess.run([sys.executable, os.path.join(HERE, "_qa_student_walk.py")] + list(args), env=env,
                       capture_output=True, text=True, encoding="utf-8")
    print("  %-12s %s" % (args[0], ([l for l in (r.stdout + r.stderr).splitlines() if l.strip()] or [""])[-1]), flush=True)


for d in json.load(open(os.path.join(HERE, "_studentwalk_practice_dirs.json"))):
    p = os.path.join(HERE, "_studentwalk_" + d)
    L = lambda f: json.load(open(os.path.join(p, f + ".json"), encoding="utf-8")) if os.path.exists(os.path.join(p, f + ".json")) else {}
    v, at, m, a = L("views"), L("attempts"), L("marks"), L("adjudications")
    listening = lambda k: "LISTENING" in (v[k].get("panel_label") or "").upper()
    reask = [k for k, x in at.items() if k in v and v[k].get("shot") and not listening(k)
             and not str(x.get("answer") or "").strip("[]{} \"'") and SHOT_WORDS.search((x.get("cannot_answer") or "") + (x.get("unsure_because") or ""))]
    remark = [k for k, x in m.items() if k in v and not listening(k) and (x.get("unapplied") or x.get("verdict") == "no verdict")]
    if not reask and not remark: continue
    print("#### %s: re-ask %d, re-mark %d" % (d, len(reask), len(remark)), flush=True)
    for k in set(reask) | set(remark):
        m.pop(k, None); a.pop(k, None)
    for k in reask: at.pop(k, None)
    for f, o in (("attempts", at), ("marks", m), ("adjudications", a)):
        json.dump(o, open(os.path.join(p, f + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if reask:
        kf = os.path.join(p, "_reshoot_keys.json"); json.dump(reask, open(kf, "w"))
        run(d, "reshoot", "--keys", kf)
        run(d, "attempt-sub", "--no-ai", extra={"SV_WALK_CHUNK": "1"})
    run(d, "mark", "--no-ai")
    run(d, "adjudicate", "--sub", "--no-ai")
    run(d, "report")
print("#### redo done", flush=True)
