"""E1 - Badge-vs-scheme adjudication. Ground truth: the Opus rulings of 18 Sep 2026
(scripts/_retrofc/_badges/*_patch.json = badge or scheme changed; *_ok.json = left alone).
Jev sees the question text, badge, scheme text and the parsed scheme total, and picks
which is right. Agreement with Opus is the measure."""
import glob, io, json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jev import ask_many, answers, save, Choice, Noul

B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_retrofc", "_badges")
items = []
for f in glob.glob(os.path.join(B, "*.json")):
    name = os.path.basename(f)
    if name.endswith("_patch.json") or name.endswith("_ok.json"): continue
    inputs = json.load(io.open(f, encoding="utf-8"))
    stem = name[:-5]
    patch = {(p["lesson_id"], p["i"]): p for p in json.load(io.open(os.path.join(B, stem + "_patch.json"), encoding="utf-8"))} if os.path.exists(os.path.join(B, stem + "_patch.json")) else {}
    ok = {(p["lesson_id"], p["i"]): p for p in json.load(io.open(os.path.join(B, stem + "_ok.json"), encoding="utf-8"))} if os.path.exists(os.path.join(B, stem + "_ok.json")) else {}
    for it in inputs:
        key = (it["lesson_id"], it["i"])
        if key in patch:
            p = patch[key]
            truth = "badge_wrong" if p.get("new_type") else ("scheme_wrong" if p.get("new_marks") else "both_wrong")
            if p.get("new_type") and p.get("new_marks"): truth = "both_wrong"
        elif key in ok:
            truth = "consistent"
        else:
            continue
        items.append({"file": stem, "lesson_id": it["lesson_id"], "i": it["i"], "subject": it.get("subject"), "type": it.get("type"), "text": it.get("text"),
                      "marks": it.get("marks"), "badge": it.get("badge"), "scheme_signal": it.get("scheme_signal"), "kind": it.get("kind"), "truth": truth,
                      "opus_reason": (patch.get(key) or ok.get(key) or {}).get("reason")})

print("items with a ruling:", len(items), collections.Counter(i["truth"] for i in items))

def build(it):
    state = {"subject": it["subject"], "question": it["text"], "type_badge": it["type"],
             "badge_marks": it["badge"], "mark_scheme": it["marks"], "scheme_total_parsed_by_code": it["scheme_signal"]}
    q = {"verdict": Choice(instructions="The badge states the marks for this question; the mark scheme decides them. Which is right?",
             criteria={"consistent": "the badge marks equal the total the scheme can award (allowing for the scheme listing bands, per-point marks, or a SPaG/technical accuracy extra that the badge names)",
                       "badge_wrong": "the scheme's total is credible for this question and the badge should change to match it",
                       "scheme_wrong": "the badge is credible for this question and the scheme's marks are wrong or incomplete",
                       "both_wrong": "neither the badge nor the scheme total fits the question as asked"}),
         "spag_extra": Noul(instructions="The scheme awards separate marks for spelling, punctuation and grammar or technical accuracy on top of the content marks")}
    return state, q

res = ask_many(items, build, tag="badges", workers=8)
out, agree, n = [], 0, 0
conf = collections.defaultdict(lambda: [0, 0])
for it, r, err in res:
    row = dict(it)
    if r:
        a = answers(r); row["jev"] = a["verdict"]["choice"]; row["jev_conf"] = a["verdict"]["confidence"]; row["jev_probs"] = a["verdict"]["probabilities"]; row["spag"] = a["spag_extra"]["noul"]
        n += 1
        hit = (row["jev"] == it["truth"]) or (it["truth"] == "both_wrong" and row["jev"] in ("badge_wrong", "scheme_wrong"))
        agree += hit
        b = "high" if row["jev_conf"] >= 0.8 else ("mid" if row["jev_conf"] >= 0.5 else "low")
        conf[b][0] += hit; conf[b][1] += 1
    else:
        row["error"] = err
    out.append(row)
cm = collections.Counter((r["truth"], r.get("jev")) for r in out if r.get("jev"))
summary = {"n": n, "agree": agree, "agreement": round(agree / max(n, 1), 3), "by_confidence": {k: {"agree": v[0], "n": v[1], "rate": round(v[0] / max(v[1], 1), 3)} for k, v in conf.items()},
           "confusion": {"%s -> %s" % k: v for k, v in sorted(cm.items())}, "binary_needs_change": None}
# the useful operational question: does it need a human at all?
tp = sum(1 for r in out if r.get("jev") and r["truth"] != "consistent" and r["jev"] != "consistent")
fn = sum(1 for r in out if r.get("jev") and r["truth"] != "consistent" and r["jev"] == "consistent")
fp = sum(1 for r in out if r.get("jev") and r["truth"] == "consistent" and r["jev"] != "consistent")
tn = sum(1 for r in out if r.get("jev") and r["truth"] == "consistent" and r["jev"] == "consistent")
summary["binary_needs_change"] = {"tp": tp, "fn": fn, "fp": fp, "tn": tn, "precision": round(tp / max(tp + fp, 1), 3), "recall": round(tp / max(tp + fn, 1), 3)}
print(json.dumps(summary, indent=1))
save("badges.json", {"summary": summary, "rows": out})
