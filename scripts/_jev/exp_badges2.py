"""E1b - Badge adjudication, second framing. v1 asked a four-way choice and Jev leaned to
"scheme wrong" on 332 consistent cases. Here the arithmetic is done in code (the parsed scheme
total is given as a fact) and Jev is asked two narrow things: is the mismatch explained by an
extra the scheme lists (SPaG / technical accuracy / a per-part split), and, if not, which side
fits the question as asked. Same ground truth."""
import io, json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jev import ask_many, answers, save, Choice, Noul
d = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_results", "badges.json"), encoding="utf-8"))
items = [r for r in d["rows"] if r.get("truth")]
def build(it):
    state = {"subject": it["subject"], "question": it["text"], "badge_label": it["type"], "badge_marks": it["badge"], "mark_scheme": it["marks"],
             "fact": "Code has parsed the scheme's highest total as %s; the badge says %s." % (it["scheme_signal"], it["badge"])}
    return (state, {"mismatch_explained": Noul(instructions="The difference between the badge marks and the parsed scheme total is explained by something the scheme or badge names explicitly, such as SPaG or technical-accuracy marks, a two-part question, or a band ladder whose top band the parser missed"),
                    "which_fits": Choice(instructions="Judged only from the question wording and the subject's usual exam format, which mark total is the plausible one for this question?",
                                         criteria={"badge": "the badge's marks", "scheme": "the scheme's parsed total", "neither": "neither total fits the question as asked"})})
res = ask_many(items, build, tag="badges2", workers=8)
out = []; tp = fp = fn = tn = 0
for it, r, err in res:
    if not r: continue
    a = answers(r); ex = a["mismatch_explained"]["noul"]; fit = a["which_fits"]["choice"]; conf = a["which_fits"]["confidence"]
    needs = ex < 0.5                     # mismatch not explained -> something needs changing
    truth_needs = it["truth"] != "consistent"
    if needs and truth_needs: tp += 1
    elif needs: fp += 1
    elif truth_needs: fn += 1
    else: tn += 1
    side = None
    if needs: side = "badge_wrong" if fit == "scheme" else ("scheme_wrong" if fit == "badge" else "both_wrong")
    out.append({"truth": it["truth"], "explained": ex, "fit": fit, "conf": conf, "jev": side or "consistent"})
agree = sum(1 for o in out if o["jev"] == o["truth"] or (o["truth"] == "both_wrong" and o["jev"] in ("badge_wrong", "scheme_wrong")))
summary = {"n": len(out), "needs_change": {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "precision": round(tp / max(tp + fp, 1), 3), "recall": round(tp / max(tp + fn, 1), 3)},
           "four_way_agreement": round(agree / max(len(out), 1), 3), "confusion": {"%s -> %s" % k: v for k, v in sorted(collections.Counter((o["truth"], o["jev"]) for o in out).items())}}
print(json.dumps(summary, indent=1)); save("badges2.json", {"summary": summary, "rows": out})
