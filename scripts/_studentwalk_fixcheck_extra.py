"""Follow-up to the practice fix re-walk (27 Sep 2026): re-mark the four genetics answers the walk
clicked wrongly (case-only option duplicates), finish spanish-aqa (network error), and walk the 7
questions fixed afterwards (6 gap-fill word banks short of a repeated word; 1 sentence-builder)."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SUBJECTS = {s["slug"] + ("-unity" if s["school_id"] else ""): s for s in
            json.load(open(os.path.join(HERE, "_studentwalk_practice_subjects.json"), encoding="utf-8"))}
EXTRA = {"german-unity": ["german/people-and-lifestyle/2/bronze/2"], "german-aqa": ["german-aqa/people-and-lifestyle/2/bronze/2"],
         "french-edexcel": ["french-edexcel/media-and-technology/3/bronze/3", "french-edexcel/my-neighbourhood/3/bronze/3"],
         "german-edexcel": ["german-edexcel/lifestyle-and-wellbeing/1/bronze/2"], "spanish-unity": ["spanish/people-and-lifestyle/10/bronze/2"],
         "spanish-edexcel": ["spanish-edexcel/travel-and-tourism/1/gold/1"]}
REMARK = {"science-ocr": ["science-ocr/biology-data-skills/2/gold/0"], "separate-sciences": ["separate-sciences/biology-data-skills/2/gold/0"],
          "separate-sciences-edexcel": ["separate-sciences-edexcel/biology-data-skills/2/gold/0"],
          "separate-sciences-unity": ["separate-sciences/biology-data-skills/2/gold/0"], "spanish-aqa": []}
for dr in sorted(set(EXTRA) | set(REMARK)):
    wd = os.path.join(HERE, "_studentwalk_fixcheck_" + dr)
    L = lambda f: json.load(open(os.path.join(wd, f + ".json"), encoding="utf-8")) if os.path.exists(os.path.join(wd, f + ".json")) else {}
    S = lambda f, o: json.dump(o, open(os.path.join(wd, f + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    m, a, at, v = L("marks"), L("adjudications"), L("attempts"), L("views")
    for k in REMARK.get(dr, []) + EXTRA.get(dr, []):
        m.pop(k, None); a.pop(k, None)
    for k in EXTRA.get(dr, []):      # the question changed: fresh view and attempt
        v.pop(k, None); at.pop(k, None)
    S("marks", m); S("adjudications", a); S("views", v); S("attempts", at)
    env = dict(os.environ, PYTHONIOENCODING="utf-8", SV_QA_BASE="http://127.0.0.1:8910", SV_WALK_BUDGET="100000",
               SV_WALK_SID=SUBJECTS[dr]["id"], SV_WALK_DIR=wd, SV_WALK_CHUNK="1")
    run = lambda *args: print("  ", dr, args[0], ([l for l in (lambda r: (r.stdout + r.stderr))(subprocess.run(
        [sys.executable, os.path.join(HERE, "_qa_student_walk.py")] + list(args), env=env, capture_output=True, text=True,
        encoding="utf-8")).splitlines() if l.strip()] or [""])[-1], flush=True)
    if EXTRA.get(dr):
        kf = os.path.join(wd, "keys_extra.json"); json.dump(EXTRA[dr], open(kf, "w"))
        run("extract", "--keys", kf); run("attempt-sub", "--no-ai")
    run("mark", "--no-ai"); run("adjudicate", "--sub", "--no-ai")
    m, a = L("marks"), L("adjudications")
    for k in REMARK.get(dr, []) + EXTRA.get(dr, []) or list(m):
        if k in m: print("     ", k, m[k].get("verdict"), (a.get(k) or {}).get("finding", ""))
