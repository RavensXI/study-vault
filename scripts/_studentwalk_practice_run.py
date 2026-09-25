"""Run the student walk over the practice-format subjects (25 Sep 2026), one subject row at a time.

Every subject row gets its own walk directory and is pinned by its subject id (SV_WALK_SID), because
several slugs exist twice (a school copy and the free tier). Click-and-choose / number questions only
(--no-ai): translate, role play and dictation are not walked.

  python scripts/_studentwalk_practice_run.py canary <dir-name> <slug> <unit/n> [<unit/n> ...]
  python scripts/_studentwalk_practice_run.py all [--from <dir-name>]
"""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SUBJECTS = {s["slug"] + ("-unity" if s["school_id"] else ""): s for s in
            json.load(open(os.path.join(HERE, "_studentwalk_practice_subjects.json"), encoding="utf-8"))}
ORDER = ["maths-aqa", "maths-edexcel", "maths-ocr", "maths-eduqas",
         "spanish-aqa", "spanish-edexcel", "french-aqa", "french-edexcel", "german-aqa", "german-edexcel",
         "spanish-unity", "french-unity", "german-unity",
         "science-aqa", "science-edexcel", "science-ocr", "science-ocr-b", "science-unity",
         "separate-sciences", "separate-sciences-unity", "separate-sciences-edexcel", "separate-sciences-ocr",
         "separate-sciences-ocr-b",
         "geography-aqa", "geography-edexcel-a", "geography-edexcel-b", "geography-eduqas", "geography-ocr", "geography-unity",
         "statistics-aqa", "statistics-edexcel",
         "music-aqa", "music-edexcel", "music-eduqas", "music-ocr", "latin-eduqas"]


def run(name, *args, extra=None):
    s = SUBJECTS[name]
    env = dict(os.environ, PYTHONIOENCODING="utf-8", SV_QA_BASE="http://127.0.0.1:8910", SV_WALK_BUDGET="100000",
               SV_WALK_SID=s["id"], SV_WALK_DIR=os.path.join(HERE, "_studentwalk_" + name))
    env.update(extra or {})
    cmd = [sys.executable, os.path.join(HERE, "_qa_student_walk.py")] + list(args)
    r = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8")
    tail = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()][-3:]
    print("  %-16s %s" % (args[0], " | ".join(tail)), flush=True)


def walk(name, lessons=None):
    print("######## %s %s" % (name, time.strftime("%H:%M")), flush=True)
    slug = SUBJECTS[name]["slug"]
    if lessons:
        for l in lessons: run(name, "extract", "--subject", slug, "--lesson", l)
    elif not os.path.exists(os.path.join(HERE, "_studentwalk_" + name, "views.json")):
        run(name, "extract", "--subject", slug)
    run(name, "attempt-sub", "--no-ai")
    run(name, "attempt-sub", "--no-ai")
    run(name, "attempt-sub", "--no-ai", extra={"SV_WALK_CHUNK": "1"})
    run(name, "mark", "--no-ai")
    run(name, "mark", "--no-ai")
    run(name, "adjudicate", "--sub", "--no-ai")
    run(name, "report")


if __name__ == "__main__":
    if sys.argv[1] == "canary":
        name = sys.argv[2]
        SUBJECTS[name] = SUBJECTS[sys.argv[3]]
        walk(name, sys.argv[4:])
    else:
        order = ORDER[ORDER.index(sys.argv[sys.argv.index("--from") + 1]):] if "--from" in sys.argv else ORDER
        for n in order: walk(n)
        print("######## all done %s" % time.strftime("%H:%M"), flush=True)
