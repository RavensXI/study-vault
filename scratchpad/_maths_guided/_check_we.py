import json
LID = "ab716e12-4427-45e8-9796-a9343073968a"
live = json.load(open("_live_l14.json", encoding="utf-8"))
pre = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
entry = next(e for e in pre if e["id"] == LID)
prewe = entry["practice_data"]["worked_examples"]
livwe = live["worked_examples"]

def flat(we):
    out=[]
    for ex in we:
        out.append(("Q", ex.get("question"), ex.get("difficulty")))
        for s in ex["steps"]:
            out.append(("S", s.get("label"), s.get("content")))
    return out

pf, lf = flat(prewe), flat(livwe)
print("same length:", len(pf)==len(lf))
for i,(a,b) in enumerate(zip(pf,lf)):
    if a!=b:
        print("DIFF", i)
        print("  pre:", a)
        print("  liv:", b)
