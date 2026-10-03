"""'Check your thinking' notes for the canary tips (Tom, 3 Oct 2026).

A thinking task needs feedback, but not a live AI reply that scales with use. So each tip gets a short
note written now, shown after the pupil taps "I've had a go": the points a strong answer weighs and the
common trap, or the answer itself where there is one (predict, explain). Opus writes a lesson's notes in
one call; Jev checks each for facts the lesson does not contain. Then each lesson's tips + notes are
exported as /revision-tips/<subject>/<unit>/lNN.json for the preview branch.

  python scripts/revision_tips/add_notes.py [--export DIR]
"""
import json, os, re, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import build_canary as B
from bs4 import BeautifulSoup
from lib.supabase_client import get_client

SYSTEM = """You write the short feedback a GCSE pupil (aged 15-16, UK) reads straight after trying a revision task on paper.
For each task you get the task and its box; you also get the whole lesson.

The note:
- Where the task has a right answer (a prediction, a calculation, an explanation, a recall), give it plainly first, then the reason.
- Where it is a judgement (rank, what if, argue, weak link, apply, odd one out), there is no single right answer: give the 2-3 points a strong answer weighs, the view most would reach and why, and the trap a weaker answer falls into.
- For "apply" or "sketch" tasks, say what a good answer must include so the pupil can check their own.
- Speak to the pupil ("A strong answer...", "If you put..."). Plain British English, short sentences, 40-80 words, no lists, no headings.
- Use ONLY facts in the lesson text. Never add a fact, name, date or figure the lesson does not contain.
- No exam advice, no praise, no emoji, no exclamation marks.

Reply with ONLY JSON: {"notes": [{"anchor": "<anchor id>", "note": "<the note>"}]}, one per task, in order."""

NEW_FACT = {"type": "noul", "instructions": "The feedback note states a fact, name, date or figure that does not appear anywhere in the lesson text given"}
WRONG = {"type": "noul", "instructions": "The feedback note says something that the lesson text contradicts"}


def jev_note(lesson_text, tip, note):
    body = {"model": "jev-latest", "state": {"lesson_text": lesson_text[:12000], "revision_task": tip, "feedback_note": note},
            "questions": {"new_fact": NEW_FACT, "contradicts": WRONG}}
    for a in range(4):
        try:
            req = urllib.request.Request("https://api.typesafe.ai/v1/systemone", data=json.dumps(body).encode(), method="POST",
                                         headers={"Authorization": "Bearer " + B.JEV_KEY, "Content-Type": "application/json"})
            ans = json.loads(urllib.request.urlopen(req, timeout=60).read())["answers"]
            return {"new_fact": ans["new_fact"]["noul"], "contradicts": ans["contradicts"]["noul"]}
        except Exception:
            time.sleep(2 + 3 * a)
    return None


def main():
    sb = get_client()
    d = json.load(open(B.RESULTS, encoding="utf-8"))
    todo = [(k, v) for k, v in d.items() if any(a.get("new") and not a.get("note") for a in v["anchors"])]
    print("%d lessons need notes" % len(todo), flush=True)

    def one(kv):
        key, v = kv
        r = sb.table("lessons").select("content_html,title").eq("id", v["lesson_id"]).execute().data[0]
        plain = re.sub(r"\s+", " ", BeautifulSoup(r["content_html"], "html.parser").get_text(" ")).strip()
        anc = [a for a in v["anchors"] if a.get("new")]
        user = ("Lesson: %s\n\nLESSON TEXT:\n%s\n\nTASKS:\n%s" % (r["title"], plain[:10000], "\n\n".join(
            "%s (type %s)\nTask: %s\nBox: %s" % (a["anchor"], a.get("type"), a["new"], a["text"][:1200]) for a in anc)))
        for attempt in range(2):
            res = B.claude(SYSTEM, user) or {}
            got = {n["anchor"]: n["note"] for n in res.get("notes", []) if isinstance(n, dict) and n.get("note")}
            bad = []
            for a in anc:
                if a.get("note_ok"): continue
                if a["anchor"] in got:
                    a["note"] = got[a["anchor"]]
                    a["note_checks"] = jev_note(plain, a["new"], a["note"])
                    c = a["note_checks"] or {}
                    a["note_ok"] = bool(c) and c["new_fact"] <= 0.5 and c["contradicts"] <= 0.5
                if not a.get("note_ok"): bad.append(a["anchor"])
            if not bad: break
            user += "\n\nRewrite ONLY: %s. A checker found a fact not in the lesson, or a claim the lesson contradicts." % ", ".join(bad)
        return key, v

    with ThreadPoolExecutor(3) as ex:
        for key, v in ex.map(one, todo):
            d[key] = v
            json.dump(d, open(B.RESULTS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("  %s: %d/%d notes pass" % (key, sum(bool(a.get("note_ok")) for a in v["anchors"]), len(v["anchors"])), flush=True)

    if "--export" in sys.argv:
        out = sys.argv[sys.argv.index("--export") + 1]
        n = 0
        for key, v in d.items():
            s, u, l = key.split("/")
            tips = {a["anchor"]: {"tip": a["new"], "technique": a.get("technique"), "note": a.get("note") if a.get("note_ok") else None}
                    for a in v["anchors"] if a.get("new") and a.get("pass")}
            if not tips: continue
            p = os.path.join(out, s, u, "l%02d.json" % int(l[1:]))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            json.dump({"tips": tips}, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            n += 1
        print("exported %d lessons to %s" % (n, out))


if __name__ == "__main__":
    main()
