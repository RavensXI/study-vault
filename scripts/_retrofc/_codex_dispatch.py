"""Hand the next tail-of-queue unit to the Codex pool and launch the wrapper detached.

Usage: python scripts/_retrofc/_codex_dispatch.py [--model gpt-5.6-terra] [--effort xhigh]
Writes _loop.json.codex.in_progress; prints the launch record. Refuses to launch
while codex.in_progress is set (finish that unit first) or resume_after is in the future.
"""
import datetime
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
LOOP = os.path.join(HERE, "_loop.json")
UNIT = os.path.join(HERE, "_unit.py")
WRAPPER = os.path.join(HERE, "_run_codex_checker.py")
GENERIC = ("read the spec's assessment section before asserting any exam claim (paper names, durations, marks, sections, "
           "assessment objectives); verify every date, name, value, definition and term against the spec and reliable fetched "
           "sources; a house practice question's mark allocation is ours, not the board's - do not rewrite it unless it states "
           "another board's format; never paste board wording")
SCIENCE = ("AQA Trilogy 8464: 6 papers 1h15 70 marks F/H; AQA separate 8461/8462/8463: 2 papers each 1h45 100 marks; Edexcel 1SC0: "
           "6 papers 1h10 60 marks, separate 1BI0/1CH0/1PH0 2 papers 1h45 100 marks; OCR Gateway A J250: 6 papers 1h10 60 marks, "
           "separate J247/J248/J249 2 papers 1h45 90 marks; OCR 21st Century B J260/J257-J259: read the spec, do not assert from memory. "
           "Verify tier flags (HT only), required practicals and the equations list in the spec; recompute every worked example.")
FACTS = {
    "music-aqa": ("AQA 8271 Music. Verify every exam claim in the spec before asserting it: Component 1 Understanding Music is a "
                  "listening exam (about 1 hour 30 minutes, 96 marks, 40 per cent) with Section A unfamiliar listening and Section B "
                  "on the study pieces; Components 2 and 3 are performing and composing coursework. Check every composer, date, work "
                  "title, movement, key, metre, instrumentation and terminology claim against the spec's content list and reliable "
                  "fetched sources; never paste board wording."),
}
FAMILY_MAP = {"english-literature": "english-literature", "science": "science", "history": "history"}


def arg(name, default=None):
    a = sys.argv
    return a[a.index(name) + 1] if name in a else default


def main():
    model, effort = arg("--model", "gpt-5.6-terra"), arg("--effort", "xhigh")
    L = json.load(open(LOOP, encoding="utf-8"))
    cx = L.setdefault("codex", {"in_progress": None, "units_done": 0, "resume_after": None, "audits": []})
    if cx.get("in_progress"):
        print(json.dumps({"refused": "codex.in_progress is set", "in_progress": cx["in_progress"]}))
        return
    ra = cx.get("resume_after")
    if ra and datetime.datetime.fromisoformat(ra) > datetime.datetime.now():
        print(json.dumps({"refused": "resume_after in the future", "resume_after": ra}))
        return
    nxt = json.loads(subprocess.check_output([sys.executable, UNIT, "next", "--pool", "codex"], text=True, encoding="utf-8", cwd=ROOT))
    if nxt.get("done"):
        print(json.dumps({"done": True}))
        return
    subject, unit = nxt["subject"], nxt["unit"]
    subprocess.check_call([sys.executable, UNIT, "prep", subject, unit, "--pool", "codex"], stdout=subprocess.DEVNULL, cwd=ROOT)
    d = os.path.join(HERE, "units", f"{subject}__{unit}")
    for stale in ("_codex_done.json", "_report.json", "_edits.json", "_codex_last_message.md"):
        p = os.path.join(d, stale)
        if os.path.exists(p):
            os.remove(p)
    brief = json.load(open(os.path.join(d, "_brief.json"), encoding="utf-8"))
    family = brief.get("family") or "generic"
    facts = FACTS.get(subject) or (SCIENCE if family == "science" else GENERIC)
    cmd = [sys.executable, WRAPPER, d, "--model", model, "--effort", effort, "--family", FAMILY_MAP.get(family, "generic"),
           "--facts", facts, "--timeout-min", "40"]
    flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
    p = subprocess.Popen(cmd, cwd=ROOT, stdout=open(os.path.join(d, "_launcher_stdout.txt"), "w"),
                         stderr=open(os.path.join(d, "_launcher_stderr.txt"), "w"), stdin=subprocess.DEVNULL, creationflags=flags, close_fds=True)
    cx["in_progress"] = {"subject": subject, "unit": unit, "model": model, "effort": effort, "family": family,
                         "launched_at": datetime.datetime.now().isoformat(timespec="seconds"), "attempts": 1, "pid": p.pid}
    L = json.load(open(LOOP, encoding="utf-8"))   # re-read: prep does not touch it, but stay safe
    L["codex"] = cx
    json.dump(L, open(LOOP, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({"launched": cx["in_progress"], "lessons": nxt.get("lessons"), "remaining_free": nxt.get("remaining")}))


if __name__ == "__main__":
    main()
