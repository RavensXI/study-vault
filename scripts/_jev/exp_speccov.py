"""E8 - Specification coverage matrix. OCR Computer Science J277: 236 spec statements x every
live free-tier computer-science lesson (plus the two new lessons still pending review). For
each lesson, one call carries the lesson text and asks a Noul per statement in its section
group. Output: per statement the best-covering lesson and its probability; the statements no
lesson covers; per lesson what it covers. Ground truth check: the 2.2.3 SQL / string handling /
random-number statements should land on lessons 12 and 13 only (the gap found on 18 Sep)."""
import io, json, os, sys, re, html, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jev import ask_many, answers, save, sb_all, Noul
HERE = os.path.dirname(os.path.abspath(__file__))
def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()

SPEC = sys.argv[1] if len(sys.argv) > 1 else "spec_j277.json"; SUBJ = sys.argv[2] if len(sys.argv) > 2 else "computer-science"; OUT = sys.argv[3] if len(sys.argv) > 3 else "speccov.json"; SCHOOL = sys.argv[4] if len(sys.argv) > 4 else None
spec = json.load(io.open(os.path.join(HERE, "_results", SPEC), encoding="utf-8"))
rows = sb_all("lessons?select=id,title,description,lesson_number,content_html,glossary_terms,status,units!inner(slug,name,subjects!inner(slug,school_id))&units.subjects.slug=eq." + SUBJ + "&units.subjects.school_id=" + ("eq." + SCHOOL if SCHOOL else "is.null") + "&status=in.(live,pending_review)")
rows.sort(key=lambda r: (r["units"]["slug"], r["lesson_number"]))
print("lessons", len(rows), "statements", len(spec))
# group statements by code so each call carries <= 20 questions
bycode = collections.defaultdict(list)
for i, s in enumerate(spec): bycode[s["code"]].append((i, s))
jobs = []
for r in rows:
    text = strip(r["content_html"])[:40000]
    gl = ", ".join(g.get("term", "") for g in (r.get("glossary_terms") or [])[:25])
    for code, group in bycode.items():
        for k in range(0, len(group), 18):
            jobs.append({"lesson": r, "text": text, "glossary": gl, "code": code, "group": group[k:k + 18]})
def build(j):
    qs = {"s%d" % i: Noul(instructions="The lesson teaches this specification point well enough that a student could answer an exam question on it: " + s["statement"]) for i, s in j["group"]}
    return ({"unit": j["lesson"]["units"]["name"], "lesson_title": j["lesson"]["title"], "lesson_description": j["lesson"]["description"], "glossary": j["glossary"], "lesson_text": j["text"]}, qs)
res = ask_many(jobs, build, tag="speccov", workers=8)
matrix = collections.defaultdict(dict)   # statement idx -> lesson key -> p
for j, r, err in res:
    if not r: continue
    key = "%s/%d" % (j["lesson"]["units"]["slug"], j["lesson"]["lesson_number"])
    for name, a in answers(r).items():
        matrix[int(name[1:])][key] = a["noul"]
per_stmt = []
for i, s in enumerate(spec):
    m = matrix.get(i, {})
    best = sorted(m.items(), key=lambda kv: -kv[1])[:3]
    per_stmt.append({"i": i, "code": s["code"], "statement": s["statement"], "best": best, "covered": bool(best) and best[0][1] >= 0.6})
gaps = [p for p in per_stmt if not p["covered"]]
per_lesson = collections.defaultdict(list)
for p in per_stmt:
    for key, v in p["best"][:1]:
        if v >= 0.6: per_lesson[key].append(p["code"] + " " + p["statement"][:70])
sql = [p for p in per_stmt if re.search(r"\bSQL\b|string manipulation|random number", p["statement"], re.I)]
summary = {"lessons": len(rows), "statements": len(spec), "covered": len(per_stmt) - len(gaps), "gaps": len(gaps),
           "gaps_by_code": dict(collections.Counter(g["code"] for g in gaps)),
           "gap_list": [{"code": g["code"], "statement": g["statement"][:120], "best": g["best"][:1]} for g in gaps],
           "sql_strings_random_check": [{"statement": p["statement"][:90], "best": p["best"][:2]} for p in sql],
           "coverage_per_lesson": {k: len(v) for k, v in sorted(per_lesson.items())}}
print(json.dumps(summary, indent=1, ensure_ascii=False)[:6000])
save(OUT, {"summary": summary, "per_statement": per_stmt, "per_lesson": dict(per_lesson)})
