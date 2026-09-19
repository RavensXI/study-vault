"""E18 - Higher-tier tagging. Science lessons wrap Higher-only chunks in <div class="higher-only">.
Ground truth: chunks inside the wrapper vs sibling chunks outside it, same lesson. Jev sees the
chunk and the subject and says whether it is Higher-tier-only content. If this works it is a
fleet-wide audit of tier wrappers (and a way to tag maths/science content we never wrapped)."""
import io, json, os, sys, re, html, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jev import ask_many, answers, save, sb_all, Noul
def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()
random.seed(9)
rows = sb_all("lessons?select=id,title,lesson_number,content_html,units!inner(slug,subjects!inner(slug,school_id))&status=eq.live&units.subjects.school_id=is.null&units.subjects.slug=in.(science-aqa,science-edexcel,science-ocr,separate-sciences,maths-edexcel,maths-aqa)&content_html=like.*higher-only*")
items = []
for r in rows:
    h = r["content_html"] or ""
    # crude but robust: find higher-only divs (non-nested) and take their paragraphs; take other paragraphs as 'both'
    hi = re.findall(r'<div class="higher-only">(.*?)</div>', h, re.S)
    hi_paras = [strip(p) for blk in hi for p in re.findall(r"<p[^>]*>(.*?)</p>", blk, re.S)]
    rest = re.sub(r'<div class="higher-only">.*?</div>', " ", h, flags=re.S)
    both_paras = [strip(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", rest, re.S)]
    hi_paras = [p for p in hi_paras if 120 <= len(p) <= 900]; both_paras = [p for p in both_paras if 120 <= len(p) <= 900]
    if not hi_paras or not both_paras: continue
    subj = r["units"]["subjects"]["slug"]
    for p in random.sample(hi_paras, min(2, len(hi_paras))): items.append({"subject": subj, "unit": r["units"]["slug"], "n": r["lesson_number"], "title": r["title"], "para": p, "truth": "higher"})
    for p in random.sample(both_paras, min(2, len(both_paras))): items.append({"subject": subj, "unit": r["units"]["slug"], "n": r["lesson_number"], "title": r["title"], "para": p, "truth": "both"})
random.shuffle(items); items = items[:900]
print("lessons with wrappers", len(rows), "chunks", len(items), collections.Counter(i["truth"] for i in items))
def build(it):
    return ({"subject": it["subject"], "lesson": it["title"], "paragraph": it["para"]},
            {"higher_only": Noul(instructions="This content is examined only on the Higher tier paper of this GCSE; Foundation tier students are not required to learn it")})
res = ask_many(items, build, tag="tier", workers=8)
out = []
for it, r, err in res:
    if not r: continue
    a = answers(r); it["p"] = a["higher_only"]["noul"]; out.append(it)
def at(th):
    hi = [o for o in out if o["truth"] == "higher"]; bo = [o for o in out if o["truth"] == "both"]
    tp = sum(1 for o in hi if o["p"] >= th); fp = sum(1 for o in bo if o["p"] >= th)
    return {"threshold": th, "higher_caught": "%d/%d" % (tp, len(hi)), "both_flagged": "%d/%d" % (fp, len(bo)), "precision": round(tp / max(tp + fp, 1), 3), "recall": round(tp / max(len(hi), 1), 3)}
pairs = [(a["p"], b["p"]) for a in out if a["truth"] == "higher" for b in out if b["truth"] == "both" and b["unit"] == a["unit"] and b["n"] == a["n"]]
auc = (sum(1 for x, y in pairs if x > y) + 0.5 * sum(1 for x, y in pairs if x == y)) / max(len(pairs), 1)
by_subj = {}
for s in set(o["subject"] for o in out):
    hi = [o for o in out if o["subject"] == s and o["truth"] == "higher"]; bo = [o for o in out if o["subject"] == s and o["truth"] == "both"]
    by_subj[s] = {"higher_mean_p": round(sum(o["p"] for o in hi) / max(len(hi), 1), 2), "both_mean_p": round(sum(o["p"] for o in bo) / max(len(bo), 1), 2), "n": len(hi) + len(bo)}
summary = {"chunks": len(out), "within_lesson_auc": round(auc, 3), "by_threshold": [at(t) for t in (0.5, 0.7, 0.85)], "by_subject": by_subj,
           "confident_misses": [{"subject": o["subject"], "unit": o["unit"], "n": o["n"], "para": o["para"][:160]} for o in out if o["truth"] == "higher" and o["p"] < 0.2][:10],
           "confident_false_alarms": [{"subject": o["subject"], "unit": o["unit"], "n": o["n"], "para": o["para"][:160]} for o in out if o["truth"] == "both" and o["p"] >= 0.85][:10]}
print(json.dumps(summary, indent=1, ensure_ascii=False)); save("tier.json", {"summary": summary, "rows": out})
