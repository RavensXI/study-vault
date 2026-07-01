"""Assemble the per-short question map the feed consumes, from:
  - scratchpad/_shorts_picks.json  (workflow output: {results:[{lesson_id,picks:[{topic_index,kc_index}]}]})
  - scratchpad/_shorts_qbank.json   (the fetched QA'd question bank)
Writes scripts/_shorts_questions.json = { lesson_id: { "<topic_index>": {q,opts,correct,type} } }.
Deterministic; the model work already happened in the workflow.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PICKS = os.path.join(ROOT, "scratchpad", "_shorts_picks.json")
QBANK = os.path.join(ROOT, "scratchpad", "_shorts_qbank.json")
OUT = os.path.join(ROOT, "scripts", "_shorts_questions.json")

def main():
    picks = json.load(open(PICKS, encoding="utf-8"))
    qbank = json.load(open(QBANK, encoding="utf-8"))
    kcs_by_lesson = {l["lesson_id"]: l["kcs"] for l in qbank["lessons"]}

    results = picks.get("results", picks) if isinstance(picks, dict) else picks
    mapping, n_q, skipped = {}, 0, []
    for r in results:
        lid = r["lesson_id"]; kcs = kcs_by_lesson.get(lid, [])
        m = {}
        for p in r["picks"]:
            ti, ki = p["topic_index"], p["kc_index"]
            if 0 <= ki < len(kcs):
                kc = kcs[ki]
                m[str(ti)] = {"q": kc["q"], "opts": kc["options"], "correct": kc["correct"], "type": kc.get("type")}
                n_q += 1
            else:
                skipped.append((lid, ti, ki))
        if m:
            mapping[lid] = m

    json.dump(mapping, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(mapping)} lessons, {n_q} short->question mappings -> {OUT}")
    if skipped:
        print("out-of-range kc_index (skipped):", skipped)

if __name__ == "__main__":
    main()
