"""E7 - "What do you want to revise?" router. Two-stage cascade: pick the subject (Choice over
the free-tier subjects, grouped by family with board), then pick the lesson within that subject
(Choice over its lessons, title + description; up to 255 options). Ground truth: 120 queries
written by an Opus agent with the intended lesson. Measures: subject accuracy, lesson top-1,
lesson top-3, and what confidence says about the misses."""
import io, json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jev import ask_many, answers, save, sb_all, Choice, Noul
HERE = os.path.dirname(os.path.abspath(__file__))
queries = json.load(io.open(os.path.join(HERE, "_results", "search_queries.json"), encoding="utf-8"))
subs = sb_all("subjects?select=id,slug,name,exam_board&school_id=is.null&status=eq.live")
subj_criteria = {s["slug"]: "%s (%s)" % (s["name"], s["exam_board"] or "") for s in subs}
lessons = sb_all("lessons?select=id,title,description,lesson_number,units!inner(slug,name,subjects!inner(slug,school_id))&status=eq.live&units.subjects.school_id=is.null")
bysub = collections.defaultdict(list)
for l in lessons: bysub[l["units"]["subjects"]["slug"]].append(l)
print("subjects", len(subj_criteria), "lessons", len(lessons), "queries", len(queries))

# stage 1: subject. The student's own picked subjects would normally narrow this; here it is open.
def build1(q):
    return ({"student_query": q["query"], "note": "GCSE revision site; the student may misspell or be vague; pick the subject whose lessons answer the query"},
            {"subject": Choice(instructions="Which subject is this query about", criteria=subj_criteria)})
res1 = ask_many(queries, build1, tag="search_subject", workers=8)
stage1 = {}
for q, r, err in res1:
    if not r: continue
    a = answers(r); stage1[q["query"]] = (a["subject"]["choice"], a["subject"]["confidence"], sorted(a["subject"]["probabilities"].items(), key=lambda kv: -kv[1])[:3])
# a family-level match counts too (history-aqa vs history-edexcel is the board picker's job, not the router's)
def fam(s): import re; return re.sub(r"-(aqa|edexcel|edexcel-a|edexcel-b|ocr|ocr-b|eduqas|b-edexcel)$", "", s)
subj_hit = sum(1 for q in queries if q["query"] in stage1 and stage1[q["query"]][0] == q["subject"])
fam_hit = sum(1 for q in queries if q["query"] in stage1 and fam(stage1[q["query"]][0]) == fam(q["subject"]))

# stage 2: lesson within the TRUE subject (so the two stages are measured independently), then within the chosen one
def build2(item):
    q, sub = item["q"], item["sub"]
    ls = bysub.get(sub, [])[:250]
    crit = {l["id"]: (l["units"]["name"] + " / " + l["title"] + ": " + (l["description"] or ""))[:220] for l in ls}
    item["_ids"] = list(crit)
    return ({"student_query": q["query"]}, {"lesson": Choice(instructions="Which lesson best answers this student's query", criteria=crit)})
items_true = [{"q": q, "sub": q["subject"], "mode": "true_subject"} for q in queries]
items_pred = [{"q": q, "sub": stage1[q["query"]][0], "mode": "predicted_subject"} for q in queries if q["query"] in stage1]
res2 = ask_many(items_true + items_pred, build2, tag="search_lesson", workers=6)
stats = {"true_subject": [0, 0, 0], "predicted_subject": [0, 0, 0]}
rows = []
bystyle = collections.defaultdict(lambda: [0, 0])
byconf = collections.defaultdict(lambda: [0, 0])
for it, r, err in res2:
    if not r: continue
    a = answers(r); pick = a["lesson"]["choice"]; conf = a["lesson"]["confidence"]
    top3 = [k for k, _ in sorted(a["lesson"]["probabilities"].items(), key=lambda kv: -kv[1])[:3]]
    truth = it["q"]["lesson_id"]; hit = pick == truth; s = stats[it["mode"]]
    s[0] += 1; s[1] += hit; s[2] += truth in top3
    if it["mode"] == "true_subject":
        bystyle[it["q"]["style"]][0] += hit; bystyle[it["q"]["style"]][1] += 1
        band = "high" if conf >= 0.7 else ("mid" if conf >= 0.4 else "low"); byconf[band][0] += hit; byconf[band][1] += 1
        rows.append({"query": it["q"]["query"], "style": it["q"]["style"], "truth": it["q"]["title"], "subject_pick": stage1.get(it["q"]["query"], ("?",))[0], "subject_truth": it["q"]["subject"], "lesson_hit": hit, "in_top3": truth in top3, "conf": conf})
summary = {"queries": len(queries), "subject_exact": subj_hit, "subject_family": fam_hit, "subject_family_rate": round(fam_hit / max(len(queries), 1), 3),
           "lesson_given_true_subject": {"n": stats["true_subject"][0], "top1": stats["true_subject"][1], "top1_rate": round(stats["true_subject"][1] / max(stats["true_subject"][0], 1), 3), "top3_rate": round(stats["true_subject"][2] / max(stats["true_subject"][0], 1), 3)},
           "lesson_end_to_end": {"n": stats["predicted_subject"][0], "top1": stats["predicted_subject"][1], "top1_rate": round(stats["predicted_subject"][1] / max(stats["predicted_subject"][0], 1), 3), "top3_rate": round(stats["predicted_subject"][2] / max(stats["predicted_subject"][0], 1), 3)},
           "by_style": {k: {"hit": v[0], "n": v[1], "rate": round(v[0] / max(v[1], 1), 2)} for k, v in bystyle.items()},
           "by_confidence": {k: {"hit": v[0], "n": v[1], "rate": round(v[0] / max(v[1], 1), 2)} for k, v in byconf.items()},
           "misses": [{"query": r["query"], "wanted": r["truth"], "conf": r["conf"]} for r in rows if not r["lesson_hit"]][:20]}
print(json.dumps(summary, indent=1, ensure_ascii=False)); save("search.json", {"summary": summary, "rows": rows})
