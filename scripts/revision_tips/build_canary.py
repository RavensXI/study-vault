"""Revision-tip canary (Tom, 3 Oct 2026): a task written for each box, checked by Jev, shown to Tom.

The lightbulb tips are mostly "cover this and recall": docs/CONTENT_PROMPT.md told the builds to write
exactly that, and boxes without their own tip get one generic line per box type. This canary rewrites
the tips for 10 units x 4 lessons from what each box actually says, so the pupil has to DO something
with the idea (rank, predict, argue, connect, sketch...). Nothing is written to the database: the
output is a JSON file and a review page. Opus writes through the subscription (claude -p); Jev checks.

  python scripts/revision_tips/build_canary.py           # build (resumable)
  python scripts/revision_tips/build_canary.py --page    # rebuild the review page only
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from bs4 import BeautifulSoup
from lib.supabase_client import get_client

OUT = os.path.join(HERE, "_canary")
os.makedirs(OUT, exist_ok=True)
RESULTS = os.path.join(OUT, "results.json")
SPEND = os.path.join(OUT, "_spend.json")

CANARY = [("history-aqa", "elizabethan-england"), ("english-literature-aqa", "a-christmas-carol"),
          ("science-aqa", "biology-paper-1"), ("geography-aqa", "paper-1"),
          ("religious-studies-aqa", "judaism-practices"), ("business-aqa", "finance"),
          ("computer-science-aqa", "data-representation"), ("psychology-aqa", "memory"),
          ("physical-education-aqa", "human-body-and-movement"), ("food-preparation-and-nutrition-aqa", "food-science")]
LESSONS_PER_UNIT = 4

# task type -> the revision-technique page it links to (only when the subject has that page)
TECHNIQUE = {"rank": "elaborative-interrogation", "what_if": "elaborative-interrogation", "odd_one_out": "elaborative-interrogation",
             "weak_link": "elaborative-interrogation", "predict": "elaborative-interrogation", "argue": "elaborative-interrogation",
             "apply": "elaborative-interrogation", "connect": "interleaving", "sketch": "dual-coding",
             "exam_question": "retrieval-practice", "explain_simply": "retrieval-practice", "recall_test": "retrieval-practice"}
LABEL = {"elaborative-interrogation": "Elaborative Interrogation", "interleaving": "Interleaving", "dual-coding": "Dual Coding",
         "retrieval-practice": "Retrieval Practice"}

SYSTEM = """You write the revision tasks that sit behind a lightbulb on boxes in a GCSE revision lesson (pupils aged 15-16, UK).
Each task is about ONE box and what it actually says. The aim: the pupil does something with the idea, not just reads or copies it.

Task types (use the id in "type"):
- rank: put 3-4 things from the box or lesson in order by a stated test, and defend the order in a line each
- what_if: change one thing (a decision, a variable, a date, a condition) and say what would follow
- odd_one_out: name the odd one out of 3-4 items from the lesson and say why (only when the box gives 3+ comparable items)
- weak_link: in a chain of causes or steps, find the weakest or missing link
- predict: predict an outcome before checking it against the lesson (sciences, economics, computing, PE)
- argue: make the strongest case for and against a claim drawn from the box, then decide
- apply: use the idea on a new example the pupil chooses (a business they know, a food they eat, a sport they play)
- connect: link the box to an EARLIER lesson in this unit (titles given); only when the link is real
- sketch: a quick diagram, timeline, flow chart or labelled sketch from memory
- exam_question: write the exam question this box answers, then the first sentence of a strong answer
- explain_simply: explain the idea to a Year 7 in 30 words or fewer, or with an everyday comparison
- recall_test: closed-book recall. ONLY where exact recall is the point (a quotation, a formula, a definition, key dates), at most ONE per lesson

Rules for every task:
- Second person, starts with a verb, plain British English, ONE task, under 180 characters.
- Name things outright (\"Cecil and Walsingham\", not \"her two key tools\"); no vague pointers to the box.
- Doable with pen and paper in 2 to 5 minutes, from this box and the lesson alone.
- Name the real things from the box (people, terms, figures), so it could only belong to this box.
- Never add a fact, name, date or figure that is not in the lesson text given.
- Never give the answer away inside the task.
- No exam advice ("In the exam..."), no "delve", no emoji, no exclamation marks.
- Use a DIFFERENT type for every box in a lesson. Prefer thinking types (rank, what_if, argue, weak_link, apply, predict) over recall.
- For a "section" (a dropdown with several points) or a "diagram", the task may use the whole section.

Reply with ONLY JSON: {"tips": [{"anchor": "<anchor id>", "type": "<type id>", "tip": "<the task>"}]} with one item per anchor, in order."""


def claude(system, user, model="opus"):
    p = os.path.join(tempfile.gettempdir(), "sv_tips_sys_%08x.txt" % (hash(system) & 0xffffffff))
    open(p, "w", encoding="utf-8").write(system)
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    for _ in range(4):
        try:
            r = subprocess.run(["claude.cmd", "-p", "--model", model, "--output-format", "json", "--tools", "",
                                "--strict-mcp-config", "--setting-sources", "", "--system-prompt-file", p],
                               input=user, capture_output=True, text=True, encoding="utf-8", env=env, timeout=900)
            out = json.loads(r.stdout)
            led = json.load(open(SPEND)) if os.path.exists(SPEND) else {"calls": 0}
            led["calls"] += 1; json.dump(led, open(SPEND, "w"))
            m = re.search(r"\{[\s\S]*\}", out.get("result") or "")
            return json.loads(m.group(0))
        except Exception as e:
            print("   claude call failed:", str(e)[:140]); time.sleep(8)
    return None


def user_env(n):
    return os.environ.get(n) or subprocess.run(["powershell", "-NoProfile", "-Command",
        "[Environment]::GetEnvironmentVariable('%s','User')" % n], capture_output=True, text=True).stdout.strip()


JEV_KEY = user_env("JEV_API_KEY")
JEV_Q = {
    "doable": {"type": "noul", "instructions": "A GCSE pupil could do this task with pen and paper in about five minutes, using only the box text and the lesson it comes from"},
    "thinking": {"type": "noul", "instructions": "The task makes the pupil think with the idea (rank, predict, argue, apply, connect, draw or explain it), rather than only copying out, re-reading or reciting the box"},
    "new_fact": {"type": "noul", "instructions": "The task itself states a fact, name, date or figure that does not appear anywhere in the box text or the lesson titles given"},
    "clear": {"type": "noul", "instructions": "A 15-year-old would know exactly what to do from the task alone"},
}


def jev(box_text, lesson_title, earlier, tip):
    body = {"model": "jev-latest", "state": {"lesson_title": lesson_title, "earlier_lessons_in_unit": earlier,
                                              "box_text": box_text[:3000], "revision_task": tip}, "questions": JEV_Q}
    for a in range(4):
        try:
            req = urllib.request.Request("https://api.typesafe.ai/v1/systemone", data=json.dumps(body).encode(), method="POST",
                                         headers={"Authorization": "Bearer " + JEV_KEY, "Content-Type": "application/json"})
            ans = json.loads(urllib.request.urlopen(req, timeout=60).read())["answers"]
            return {k: ans[k]["noul"] for k in JEV_Q}
        except Exception as e:
            time.sleep(2 + 3 * a)
    return None


def passes(s, typ):
    """Thresholds from a calibration on 8 hand-made tips (3 Oct 2026): 'thinking' and 'new_fact' separate
    sharply (copying 0.04-0.13 vs 0.81-0.94; an invented fact 0.97 vs < 0.3). 'clear' catches muddle
    (0.12) but also marks good open tasks down to ~0.45, so it fails only below 0.25 and 0.25-0.5 is
    shown as worth a look. 'doable': good 0.68+, muddled 0.45-0.58, invented-fact 0.2."""
    if not s: return False, "no check"
    why = []
    if s["doable"] < 0.5: why.append("not doable from the box")
    if typ != "recall_test" and s["thinking"] < 0.6: why.append("only recall/copying")
    if s["new_fact"] > 0.5: why.append("adds a fact")
    if s["clear"] < 0.25: why.append("unclear")
    return not why, ", ".join(why)


def text_of(el):
    for b in el.select("button svg, .revision-tip-btn, .revision-tip-popup"): b.decompose()
    return re.sub(r"\s+", " ", el.get_text(" ")).strip()


def anchors(html):
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for i, el in enumerate(soup.select(".key-fact"), 1):
        out.append({"anchor": "kf%d" % i, "kind": "key fact", "old": el.get("data-revision-tip"), "text": text_of(el)})
    d = soup.select("figure.diagram")
    if d: out.append({"anchor": "dg1", "kind": "diagram", "old": d[0].get("data-revision-tip"), "text": text_of(d[0])})
    c = soup.select(".collapsible")
    if c: out.append({"anchor": "cs1", "kind": "section", "old": c[0].get("data-revision-tip"), "text": text_of(c[0])})
    t = soup.select(".timeline")
    if t: out.append({"anchor": "tl1", "kind": "timeline", "old": t[0].get("data-revision-tip"), "text": text_of(t[0])})
    return out, re.sub(r"\s+", " ", soup.get_text(" ")).strip()


def technique_pages(sb):
    rows = sb.table("guide_pages").select("slug,subject_id").eq("guide_type", "revision-technique").limit(5000).execute().data
    by = {}
    for r in rows: by.setdefault(r["subject_id"], set()).add(r["slug"])
    return by


def build():
    sb = get_client()
    pages = technique_pages(sb)
    done = json.load(open(RESULTS, encoding="utf-8")) if os.path.exists(RESULTS) else {}
    jobs = []
    for sslug, uslug in CANARY:
        s = sb.table("subjects").select("id,name,exam_board").eq("slug", sslug).is_("school_id", "null").execute().data[0]
        u = sb.table("units").select("id,name").eq("subject_id", s["id"]).eq("slug", uslug).execute().data[0]
        ls = sb.table("lessons").select("id,lesson_number,title,content_html,status").eq("unit_id", u["id"]).order("lesson_number").execute().data
        titles = {l["lesson_number"]: l["title"] for l in ls}
        for l in [l for l in ls if l["status"] == "live" and l.get("content_html")][:LESSONS_PER_UNIT]:
            key = "%s/%s/L%02d" % (sslug, uslug, l["lesson_number"])
            if key in done: continue
            jobs.append((key, s, u, l, [titles[n] for n in sorted(titles) if n < l["lesson_number"]], pages.get(s["id"], set())))
    if os.environ.get("TIPS_LIMIT"): jobs = jobs[:int(os.environ["TIPS_LIMIT"])]
    print("%d lessons to do (%d done)" % (len(jobs), len(done)), flush=True)

    def one(job):
        key, s, u, l, earlier, have = job
        anc, plain = anchors(l["content_html"])
        if not anc: return key, {"title": l["title"], "anchors": [], "note": "no boxes"}
        user = ("Subject: %s (%s)\nUnit: %s\nLesson %d: %s\nEarlier lessons in this unit: %s\n\nLESSON TEXT:\n%s\n\nANCHORS:\n%s"
                % (s["name"], s.get("exam_board") or "", u["name"], l["lesson_number"], l["title"],
                   "; ".join(earlier) or "none (this is the first lesson)", plain[:9000],
                   "\n".join("%s (%s): %s" % (a["anchor"], a["kind"], a["text"][:1500]) for a in anc)))
        res = claude(SYSTEM, user) or {"tips": []}
        got = {t["anchor"]: t for t in res.get("tips", []) if isinstance(t, dict)}
        for attempt in range(2):
            redo = []
            for a in anc:
                t = got.get(a["anchor"])
                if not t: redo.append((a, "missing")); continue
                if "checks" not in t or attempt:
                    t["checks"] = jev(a["text"], l["title"], earlier, t["tip"])
                ok, why = passes(t["checks"], t.get("type"))
                t["pass"], t["why"] = ok, why
                if not ok: redo.append((a, why))
            if not redo or attempt: break
            fix = claude(SYSTEM, user + "\n\nRewrite ONLY these anchors; a checker found these problems:\n" +
                         "\n".join("%s: %s (was: %s)" % (a["anchor"], why, (got.get(a["anchor"]) or {}).get("tip", "")) for a, why in redo) +
                         "\nKeep every other anchor's type in mind so types stay different. Reply with the same JSON shape, only these anchors.")
            for t in (fix or {}).get("tips", []):
                if isinstance(t, dict) and t.get("anchor") in {a["anchor"] for a, _ in redo}:
                    t["rewritten"] = True; got[t["anchor"]] = t
        for a in anc:
            t = got.get(a["anchor"]) or {}
            tech = TECHNIQUE.get(t.get("type"), "retrieval-practice")
            if tech not in have: tech = "retrieval-practice" if "retrieval-practice" in have else None
            a.update({"new": t.get("tip"), "type": t.get("type"), "technique": tech, "checks": t.get("checks"),
                      "pass": t.get("pass", False), "why": t.get("why", "missing"), "rewritten": t.get("rewritten", False)})
        return key, {"title": l["title"], "lesson_id": l["id"], "anchors": anc}

    with ThreadPoolExecutor(3) as ex:
        for key, res in ex.map(one, jobs):
            done[key] = res
            json.dump(done, open(RESULTS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            n = len(res["anchors"]); ok = sum(a.get("pass") for a in res["anchors"])
            print("  %s: %d tips, %d pass" % (key, n, ok), flush=True)
    return done


if __name__ == "__main__":
    if "--page" not in sys.argv:
        build()
    from make_page import make
    make(json.load(open(RESULTS, encoding="utf-8")))
