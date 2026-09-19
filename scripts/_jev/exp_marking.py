"""E5 - Marking-adjacent judgements. Ground truth: 40 questions x 4 answers written and marked
by an Opus agent (_results/marking_set.json). Three things, none of which is "write feedback":
  band    : Score the answer on the scheme's bands -> compare to the mark (exact band, +-1 band)
  gates   : before spending a big-model call: is it off-topic / too short / a scheme paste?
  points  : per creditable point, has the answer hit it? (a live checklist while typing)
"""
import io, json, os, sys, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jev import ask_many, answers, save, Choice, Score, Noul
HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(io.open(os.path.join(HERE, "_results", "marking_set.json"), encoding="utf-8"))
items = []
for q in data:
    for a in q["answers"]:
        items.append({"q": q, "a": a})
print("questions", len(data), "answers", len(items))
BANDS = ["nothing creditable or off the question", "a weak answer: one or two relevant points, thin or undeveloped", "a middling answer: relevant, some development, gaps or imbalance", "a strong answer: full coverage, developed, meets the top descriptors"]
def build(it):
    q, a = it["q"], it["a"]
    pts = q["answers"][0].get("points_hit") or []          # the top answer's hit list is the fullest list of creditable points we have
    qs = {"band": Score(instructions="Judge the student's answer against the mark scheme. Where does it sit?", criteria=BANDS),
          "off_topic": Noul(instructions="The answer does not address the question that was asked (wrong topic, misread task, or generic content)"),
          "too_short": Noul(instructions="The answer is too brief to earn more than a low mark for a question of this size"),
          "scheme_paste": Noul(instructions="The answer reads like mark-scheme phrases or lesson headings reproduced without application")}
    for i, p in enumerate(pts[:10]): qs["pt%d" % i] = Noul(instructions="The answer makes this creditable point (in its own words is fine): " + str(p))
    it["_pts"] = pts[:10]
    return ({"question": q["question"], "marks_available": q["max_marks"], "mark_scheme": q["scheme"], "student_answer": a["text"]}, qs)
res = ask_many(items, build, tag="marking", workers=8)
rows = []
for it, r, err in res:
    if not r: continue
    a = answers(r); q, ans = it["q"], it["a"]
    frac = ans["mark"] / max(q["max_marks"], 1)
    truth_band = 0 if ans["mark"] == 0 else (1 if frac < 0.45 else (2 if frac < 0.75 else 3))
    band = a["band"]["score"]; nearest = int(round(band))
    hits = {p: a["pt%d" % i]["noul"] for i, p in enumerate(it["_pts"])}
    rows.append({"subject": q["subject"], "label": ans["label"], "mark": ans["mark"], "max": q["max_marks"], "truth_band": truth_band, "jev_band": round(band, 2), "band_hit": nearest == truth_band, "band_within1": abs(nearest - truth_band) <= 1,
                 "off_topic": a["off_topic"]["noul"], "too_short": a["too_short"]["noul"], "paste": a["scheme_paste"]["noul"],
                 "points_hit_truth": ans.get("points_hit") or [], "points_hit_jev": [p for p, v in hits.items() if v >= 0.6], "points_all": it["_pts"]})
n = len(rows)
# band agreement and rank-order within each question (does it order the four answers correctly?)
order_ok = 0; qn = 0
byq = collections.defaultdict(list)
for r_ in rows: byq[(r_["subject"], r_["max"], r_["label"])]  # placeholder
grouped = collections.defaultdict(list)
for it, r, err in res:
    if r: grouped[it["q"]["question"]].append((it["a"]["mark"], answers(r)["band"]["score"]))
for qtext, lst in grouped.items():
    if len(lst) < 3: continue
    qn += 1
    pairs = [(a, b) for i, a in enumerate(lst) for b in lst[i + 1:] if a[0] != b[0]]
    if pairs and all((a[1] > b[1]) == (a[0] > b[0]) for a, b in pairs): order_ok += 1
conc = sum(1 for lst in grouped.values() for i, a in enumerate(lst) for b in lst[i + 1:] if a[0] != b[0] and (a[1] > b[1]) == (a[0] > b[0]))
tot = sum(1 for lst in grouped.values() for i, a in enumerate(lst) for b in lst[i + 1:] if a[0] != b[0])
lab = collections.defaultdict(lambda: [0, 0, 0.0])
for r_ in rows: lab[r_["label"]][0] += 1; lab[r_["label"]][1] += r_["off_topic"] >= 0.6; lab[r_["label"]][2] += r_["jev_band"]
# point checklist: precision/recall against the agent's points_hit for the same answer (matching by exact string)
tp = fp = fn = 0
for r_ in rows:
    truth = set(r_["points_hit_truth"]) & set(r_["points_all"]); got = set(r_["points_hit_jev"])
    tp += len(truth & got); fp += len(got - truth); fn += len(truth - got)
summary = {"answers": n, "band_exact": round(sum(r_["band_hit"] for r_ in rows) / max(n, 1), 3), "band_within_one": round(sum(r_["band_within1"] for r_ in rows) / max(n, 1), 3),
           "pairwise_order_concordance": round(conc / max(tot, 1), 3), "questions_fully_ordered": "%d/%d" % (order_ok, qn),
           "by_label": {k: {"n": v[0], "flagged_off_topic": v[1], "mean_jev_band": round(v[2] / max(v[0], 1), 2)} for k, v in lab.items()},
           "off_topic_gate": {"offtopic_caught": "%d/%d" % (lab["offtopic"][1], lab["offtopic"][0]), "others_flagged": "%d/%d" % (sum(v[1] for k, v in lab.items() if k != "offtopic"), sum(v[0] for k, v in lab.items() if k != "offtopic"))},
           "point_checklist": {"tp": tp, "fp": fp, "fn": fn, "precision": round(tp / max(tp + fp, 1), 3), "recall": round(tp / max(tp + fn, 1), 3)}}
print(json.dumps(summary, indent=1, ensure_ascii=False)); save("marking.json", {"summary": summary, "rows": rows})
