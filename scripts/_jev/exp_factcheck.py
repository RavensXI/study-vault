"""E2 - Fact-check triage. Ground truth: the retro fact-check corpus (scripts/_retrofc/units/*/
_edits.json), where `find` is the text the checker changed and `replace` what it became, with a
severity and a note. Two tests:
  (a) blind single-sentence: "this passage contains a factual or specification error" on the
      BEFORE and on the AFTER text separately (does the probability separate them?)
  (b) pairwise: shown both, which is correct?
Only edits that look like content corrections (not rewordings) are used: severity HIGH/MEDIUM,
find and replace both 40-600 chars, note not about style. Sample capped for spend."""
import glob, io, json, os, sys, random, re, collections, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jev import ask_many, answers, save, Choice, Noul

U = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_retrofc", "units")
def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()
items = []
for f in glob.glob(os.path.join(U, "*", "_edits.json")):
    unit_dir = os.path.basename(os.path.dirname(f))
    try: edits = json.load(io.open(f, encoding="utf-8"))
    except Exception: continue
    if not isinstance(edits, list): continue
    for e in edits:
        if e.get("severity") not in ("HIGH", "MEDIUM"): continue
        a, b = strip(e.get("find")), strip(e.get("replace"))
        if not (40 <= len(a) <= 600 and 40 <= len(b) <= 600) or a == b: continue
        note = (e.get("note") or "")
        if re.search(r"\b(style|wording|reword|tone|typo|grammar|board name|names the board|Eduqas|AQA|OCR|Edexcel)\b", note, re.I): continue
        items.append({"unit": unit_dir, "lesson": e.get("lesson"), "field": e.get("field"), "before": a, "after": b, "severity": e["severity"], "note": note[:300]})
random.seed(7); random.shuffle(items)
SAMPLE = 700
items = items[:SAMPLE]
print("candidate edits:", len(items), collections.Counter(i["severity"] for i in items))

# (a) blind, each text on its own; order randomised so position cannot leak
blind = []
for i, it in enumerate(items):
    blind.append({"idx": i, "which": "before", "text": it["before"], "unit": it["unit"], "field": it["field"]})
    blind.append({"idx": i, "which": "after", "text": it["after"], "unit": it["unit"], "field": it["field"]})
random.shuffle(blind)
def build_blind(b):
    subj = b["unit"].split("__")[0].replace("@unity", "")
    return ({"subject": subj, "passage": b["text"], "passage_role": "a passage from a GCSE revision lesson" if b["field"] != "exam_tip_html" else "an exam tip from a GCSE revision lesson"},
            {"error": Noul(instructions="The passage contains a factual error, an invented claim about marks or examiners, or content outside the GCSE course for this subject"),
             "unsupported_marks_claim": Noul(instructions="The passage asserts that a specific thing will lose or gain marks without a basis in a published mark scheme")})
resb = ask_many(blind, build_blind, tag="factcheck_blind", workers=8)
p_before, p_after = {}, {}
for b, r, err in resb:
    if not r: continue
    a = answers(r)
    (p_before if b["which"] == "before" else p_after)[b["idx"]] = (a["error"]["noul"], a["unsupported_marks_claim"]["noul"])
pairs = [(p_before[i][0], p_after[i][0]) for i in p_before if i in p_after]
sep = sum(1 for x, y in pairs if x > y); ties = sum(1 for x, y in pairs if x == y)
# AUC-style: probability a random before outranks a random after
auc = (sep + 0.5 * ties) / max(len(pairs), 1)
thr = {}
for t in (0.5, 0.7, 0.85):
    tp = sum(1 for x, y in pairs if x >= t); fp = sum(1 for x, y in pairs if y >= t)
    thr[str(t)] = {"flag_rate_on_wrong": round(tp / max(len(pairs), 1), 3), "flag_rate_on_corrected": round(fp / max(len(pairs), 1), 3)}

# (b) pairwise, order randomised
def build_pair(it):
    flip = random.random() < 0.5
    A, Bt = (it["after"], it["before"]) if flip else (it["before"], it["after"])
    it["_flip"] = flip
    subj = it["unit"].split("__")[0].replace("@unity", "")
    return ({"subject": subj, "field": it["field"], "version_A": A, "version_B": Bt},
            {"correct": Choice(instructions="Two versions of the same passage from a GCSE revision lesson differ in a detail. Which version is factually correct and within the course?",
                               criteria={"A": "version A is the correct one", "B": "version B is the correct one"})})
random.seed(11)
resp = ask_many(items, build_pair, tag="factcheck_pair", workers=8)
pair_rows, right, n = [], 0, 0
byconf = collections.defaultdict(lambda: [0, 0])
for it, r, err in resp:
    if not r: continue
    a = answers(r); pick = a["correct"]["choice"]; conf = a["correct"]["confidence"]
    truth = "A" if it["_flip"] else "B"          # the corrected text
    hit = pick == truth; right += hit; n += 1
    band = "high" if conf >= 0.8 else ("mid" if conf >= 0.55 else "low"); byconf[band][0] += hit; byconf[band][1] += 1
    pair_rows.append({"unit": it["unit"], "lesson": it["lesson"], "field": it["field"], "severity": it["severity"], "before": it["before"][:300], "after": it["after"][:300], "note": it["note"], "jev_picked_corrected": hit, "conf": conf,
                      "p_error_before": p_before.get(items.index(it), (None,))[0], "p_error_after": p_after.get(items.index(it), (None,))[0]})
summary = {"edits_used": len(items), "blind": {"pairs": len(pairs), "before_scores_higher": sep, "ties": ties, "auc": round(auc, 3), "thresholds": thr},
           "pairwise": {"n": n, "picked_corrected": right, "accuracy": round(right / max(n, 1), 3), "by_confidence": {k: {"right": v[0], "n": v[1], "rate": round(v[0] / max(v[1], 1), 3)} for k, v in byconf.items()}}}
print(json.dumps(summary, indent=1))
save("factcheck.json", {"summary": summary, "rows": pair_rows})
