"""Second pass on the canary (3 Oct 2026):
1. Jev re-checks every tip WITH the lesson text: the first pass showed it only the box, so a tip using a
   fact from elsewhere in the lesson (Tesco, the Newquay surf shop's figures) was marked "adds a fact".
2. A lesson that used one task type twice gets its later duplicate rewritten as a different type.
"""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import build_canary as B
from bs4 import BeautifulSoup
from lib.supabase_client import get_client

B.JEV_Q["new_fact"] = {"type": "noul", "instructions": "The task itself states a fact, name, date or figure that does not appear anywhere in the lesson text given (the box or the rest of the lesson) or the lesson titles"}
B.JEV_Q["doable"] = {"type": "noul", "instructions": "A GCSE pupil could do this task with pen and paper in about five minutes, using only the lesson text given"}


def jev(lesson_text, box_text, title, earlier, tip):
    import urllib.request, time
    body = {"model": "jev-latest", "state": {"lesson_title": title, "earlier_lessons_in_unit": earlier, "box_text": box_text[:3000],
                                              "lesson_text": lesson_text[:12000], "revision_task": tip}, "questions": B.JEV_Q}
    for a in range(4):
        try:
            req = urllib.request.Request("https://api.typesafe.ai/v1/systemone", data=json.dumps(body).encode(), method="POST",
                                         headers={"Authorization": "Bearer " + B.JEV_KEY, "Content-Type": "application/json"})
            ans = json.loads(urllib.request.urlopen(req, timeout=60).read())["answers"]
            return {k: ans[k]["noul"] for k in B.JEV_Q}
        except Exception:
            time.sleep(2 + 3 * a)
    return None


def main():
    sb = get_client()
    d = json.load(open(B.RESULTS, encoding="utf-8"))
    for key, v in d.items():
        r = sb.table("lessons").select("content_html,lesson_number,title,unit_id,units!inner(name,subjects!inner(name,exam_board))").eq("id", v["lesson_id"]).execute().data[0]
        earlier = [x["title"] for x in sb.table("lessons").select("title,lesson_number").eq("unit_id", r["unit_id"]).lt("lesson_number", r["lesson_number"]).order("lesson_number").execute().data]
        plain = re.sub(r"\s+", " ", BeautifulSoup(r["content_html"], "html.parser").get_text(" ")).strip()
        # 2. duplicate types: rewrite the later one(s)
        seen = {}
        for a in v["anchors"]:
            if a.get("type") in seen:
                others = [x.get("type") for x in v["anchors"] if x is not a]
                user = ("Subject: %s\nLesson %d: %s\nEarlier lessons in this unit: %s\n\nLESSON TEXT:\n%s\n\nANCHORS:\n%s (%s): %s\n\n"
                        "Write a task for this ONE anchor. Its type must NOT be any of: %s."
                        % (r["units"]["subjects"]["name"], r["lesson_number"], r["title"], "; ".join(earlier) or "none",
                           plain[:9000], a["anchor"], a["kind"], a["text"][:1500], ", ".join(sorted(set(t for t in others if t)))))
                res = B.claude(B.SYSTEM, user)
                t = next((t for t in (res or {}).get("tips", []) if isinstance(t, dict)), None)
                if t and t.get("type") not in others:
                    a.update({"new": t["tip"], "type": t["type"], "rewritten": True,
                              "technique": B.TECHNIQUE.get(t["type"], a.get("technique"))})
                    print("  %s %s: new type %s" % (key, a["anchor"], t["type"]))
            seen[a.get("type")] = True
        # 1. re-check with the lesson text
        for a in v["anchors"]:
            if not a.get("new"): continue
            a["checks"] = jev(plain, a["text"], r["title"], earlier, a["new"])
            a["pass"], a["why"] = B.passes(a["checks"], a.get("type"))
        print("%s: %d/%d pass" % (key, sum(a["pass"] for a in v["anchors"]), len(v["anchors"])), flush=True)
        json.dump(d, open(B.RESULTS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from make_page import make
    make(d)


if __name__ == "__main__":
    main()
