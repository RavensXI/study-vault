"""E13 - Widget matching. Ground truth: the 279 wired lessons in js/widget-embed.js MAP.
For each wired lesson, Jev chooses the best widget from the 91-entry catalogue (name + what it
teaches + keywords), seeing only the lesson's title, description and headings. Top-1 accuracy
against the wired file. Then the same call on 300 UNWIRED lessons with a "none fits" option,
to see what a queue for the 3-lesson band would look like."""
import io, json, os, re, sys, random, html, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jev import ask_many, answers, save, sb_all, Choice, Noul
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()

cat = json.load(io.open(os.path.join(ROOT, "scripts", "widget_pipeline", "widget_catalogue.json"), encoding="utf-8"))["widgets"]
criteria = {w["file"]: (w["name"] + ": " + (w["teaches"] or w["targets"] or "") + " [" + ", ".join((w["concept_keywords"] or [])[:8]) + "]")[:300] for w in cat}
criteria["none"] = "no interactive in the list teaches this lesson's central idea"
src = io.open(os.path.join(ROOT, "js", "widget-embed.js"), encoding="utf-8").read()
wired = {}
for m in re.finditer(r'"([a-z0-9\-]+/[a-z0-9\-]+/\d+)":\s*\{[^}]*?file:\s*"([^"]+)"', src, re.S):
    wired.setdefault(m.group(1), m.group(2))
print("catalogue", len(cat), "wired keys", len(wired))

rows = sb_all("lessons?select=id,title,description,lesson_number,content_html,units!inner(slug,subjects!inner(slug,school_id))&status=eq.live&is_listening=eq.false&content_html=not.is.null&units.subjects.school_id=is.null")
bykey = {}
for r in rows:
    bykey[r["units"]["subjects"]["slug"] + "/" + r["units"]["slug"] + "/" + str(r["lesson_number"])] = r
def headings(h): return [strip(x) for x in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", h or "", re.S)][:12]
def build(it):
    l = it["row"]
    return ({"subject": l["units"]["subjects"]["slug"], "title": l["title"], "description": l["description"], "headings": headings(l["content_html"]), "opening": strip(l["content_html"])[:700]},
            {"widget": Choice(instructions="Which interactive from the fleet teaches this lesson's central idea or misconception? Pick none if nothing in the list does.", criteria=criteria)})

wired_items = [{"key": k, "truth": f, "row": bykey[k]} for k, f in wired.items() if k in bykey]
random.seed(5); random.shuffle(wired_items)
res = ask_many(wired_items, build, tag="widgets_wired", workers=6)
hit = n = 0; out = []; byconf = collections.defaultdict(lambda: [0, 0])
for it, r, err in res:
    if not r: continue
    a = answers(r); pick = a["widget"]["choice"]; conf = a["widget"]["confidence"]; probs = a["widget"]["probabilities"]
    top3 = [k for k, _ in sorted(probs.items(), key=lambda kv: -kv[1])[:3]]
    ok = pick == it["truth"]; hit += ok; n += 1
    band = "high" if conf >= 0.7 else ("mid" if conf >= 0.4 else "low"); byconf[band][0] += ok; byconf[band][1] += 1
    out.append({"key": it["key"], "wired": it["truth"], "jev": pick, "conf": conf, "in_top3": it["truth"] in top3, "hit": ok})
top3 = sum(1 for o in out if o["in_top3"])
summary_w = {"wired_checked": n, "top1": hit, "top1_rate": round(hit / max(n, 1), 3), "top3": top3, "top3_rate": round(top3 / max(n, 1), 3), "by_confidence": {k: {"hit": v[0], "n": v[1], "rate": round(v[0] / max(v[1], 1), 3)} for k, v in byconf.items()},
             "said_none": sum(1 for o in out if o["jev"] == "none")}

unwired = [{"key": k, "row": r} for k, r in bykey.items() if k not in wired]
random.shuffle(unwired); unwired = unwired[:400]
res2 = ask_many(unwired, build, tag="widgets_unwired", workers=6)
cand = []
for it, r, err in res2:
    if not r: continue
    a = answers(r); pick = a["widget"]["choice"]; conf = a["widget"]["confidence"]
    if pick != "none": cand.append({"key": it["key"], "title": it["row"]["title"], "widget": pick, "conf": conf})
cand.sort(key=lambda x: -x["conf"])
summary_u = {"unwired_checked": len(res2), "with_candidate": len(cand), "confident_candidates": sum(1 for c in cand if c["conf"] >= 0.7), "top_20": cand[:20]}
print(json.dumps({"wired": summary_w, "unwired": summary_u}, indent=1, ensure_ascii=False))
save("widgets.json", {"wired": summary_w, "unwired": summary_u, "wired_rows": out, "candidates": cand})
