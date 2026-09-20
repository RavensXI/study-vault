"""Widget matching over the whole fleet (Jev). For every live article lesson that carries no
interactive, choose the portable widget that teaches its central idea (or none), then gate the
confident picks against the FULL lesson text and choose the heading the strip should follow.

  python scripts/_jev/widget_match_fleet.py            # both tiers; writes _results/widget_queue.json

Pass 1  Choice over the 81 portable widgets + none, from title / description / headings / opening.
Pass 2  (conf >= 0.70) Noul: the lesson teaches, as a central idea, exactly what the widget teaches,
        so the widget fits without a change to its content; Choice: after which heading, or $end.
Keep    gate >= 0.70. Label and line are copied from the widget's first existing placement.
Nothing is wired here; wire_widget_queue.py reads the queue and edits js/widget-embed.js.
"""
import io, json, os, re, sys, html, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jev
from jev import ask_many, answers, save, sb_all, Choice, Noul
jev.BUDGET_USD = 20.0
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
UNITY = "a5414d1c-8841-4bc5-8573-a9756752361b"
def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()
def headings(h): return [strip(x) for x in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", h or "", re.S)][:14]

cat = json.load(io.open(os.path.join(ROOT, "scripts", "widget_pipeline", "widget_catalogue.json"), encoding="utf-8"))["widgets"]
portable = [w for w in cat if w["reuse"] == "portable"]
byfile = {w["file"]: w for w in cat}
criteria = {w["file"]: (w["name"] + ": " + (w["teaches"] or w["targets"] or "") + " [" + ", ".join((w["concept_keywords"] or [])[:8]) + "]")[:300] for w in portable}
criteria["none"] = "no interactive in the list teaches this lesson's central idea"

# the wiring map: keys already placed, and each widget's first label / line to reuse
src = io.open(os.path.join(ROOT, "js", "widget-embed.js"), encoding="utf-8").read()
wired = {}; copy = {}
for m in re.finditer(r'"([a-z0-9\-]+/[a-z0-9\-]+/\d+)":\s*\{(.*?)\n\s*\}', src, re.S):
    body = m.group(2); f = re.search(r'file:\s*"([^"]+)"', body); lab = re.search(r'label:\s*"([^"]*)"', body); line = re.search(r'line:\s*"([^"]*)"', body)
    if not f: continue
    wired[m.group(1)] = f.group(1)
    if f.group(1) not in copy and lab and line: copy[f.group(1)] = {"label": lab.group(1), "line": line.group(1)}
print("catalogue", len(cat), "portable", len(portable), "wired keys", len(wired), "widgets with copy", len(copy), flush=True)

rows = sb_all("lessons?select=id,title,description,lesson_number,content_html,units!inner(slug,subjects!inner(slug,school_id))&status=eq.live&is_listening=eq.false&content_html=not.is.null&order=id")
rows = [r for r in rows if len(r.get("content_html") or "") > 1500 and (r["units"]["subjects"]["school_id"] in (None, UNITY))]
bykey = collections.defaultdict(list)
for r in rows: bykey[r["units"]["subjects"]["slug"] + "/" + r["units"]["slug"] + "/" + str(r["lesson_number"])].append(r)
items = []
for k, rs in bykey.items():
    if k in wired: continue
    if len(rs) > 1: continue                     # the same key in both tiers: leave it alone
    items.append({"key": k, "row": rs[0], "tier": "unity" if rs[0]["units"]["subjects"]["school_id"] else "free"})
print("unwired lessons to judge", len(items), flush=True)

def build1(it):
    l = it["row"]
    return ({"subject": l["units"]["subjects"]["slug"], "title": l["title"], "description": l["description"], "headings": headings(l["content_html"]), "opening": strip(l["content_html"])[:1200]},
            {"widget": Choice(instructions="Which interactive from the fleet teaches this lesson's central idea or misconception? Pick none if nothing in the list does.", criteria=criteria)})
res = ask_many(items, build1, tag="widgets_fleet_pick", workers=6)
cands = []
for it, r, err in res:
    if not r: continue
    a = answers(r)["widget"]; pick = a["choice"]; conf = a.get("confidence") or (a.get("probabilities") or {}).get(pick, 0)
    if pick != "none" and pick in byfile and conf >= 0.70 and pick in copy: cands.append(dict(it, widget=pick, conf=round(conf, 3)))
print("pass 1 done: candidates", len(cands), "of", len(res), flush=True)

def build2(it):
    l = it["row"]; w = byfile[it["widget"]]; hs = headings(l["content_html"])
    anchors = {h: None for h in hs}; anchors["$end"] = "at the end of the lesson, because the whole lesson builds to it"
    return ({"lesson_title": l["title"], "lesson_text": strip(l["content_html"])[:30000],
             "interactive": {"name": w["name"], "teaches": w["teaches"], "targets": w["targets"], "keywords": w["concept_keywords"]}},
            {"fits": Noul(instructions="The lesson teaches, as one of its central ideas, exactly what this interactive teaches, so the interactive would sit in this lesson without any change to its own content (its examples, scenario and vocabulary would still make sense to a student who has just read the lesson)"),
             "after": Choice(instructions="After which section should the interactive sit? Right after the part that teaches its idea.", criteria=anchors)})
res2 = ask_many(cands, build2, tag="widgets_fleet_gate", workers=6)
queue = []; held = []
for it, r, err in res2:
    if not r: continue
    a = answers(r); fit = a["fits"]["noul"]; after = a["after"]["choice"]; pa = (a["after"].get("probabilities") or {}).get(after, a["after"].get("confidence", 0))
    rec = {"key": it["key"], "tier": it["tier"], "title": it["row"]["title"], "subject": it["row"]["units"]["subjects"]["slug"], "widget": it["widget"], "widget_name": byfile[it["widget"]]["name"],
           "pick_conf": it["conf"], "fit": round(fit, 3), "after": after, "after_conf": round(pa, 3), "label": copy[it["widget"]]["label"], "line": copy[it["widget"]]["line"]}
    (queue if fit >= 0.70 else held).append(rec)
queue.sort(key=lambda x: (x["subject"], x["key"]))
per_widget = collections.Counter(q["widget"] for q in queue)
save("widget_queue.json", {"judged": len(res), "candidates": len(cands), "queue": queue, "held": held, "per_widget": per_widget})
print("queue", len(queue), "| held by the gate", len(held), "| widgets used", len(per_widget), "| jev spent $%.2f" % jev.spent()[0], flush=True)
