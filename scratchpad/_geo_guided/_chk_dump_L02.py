import json, sys
io = open(r"_CHK_L02_dump.txt","w",encoding="utf-8")
def p(*a):
    print(*a, file=io)
live = json.load(open(r"_CHK_L02_live.json", encoding="utf-8"))
for t in ("bronze","silver","gold"):
    for i,q in enumerate(live["problem_bank"][t]):
        p("="*70)
        p(f"{t}[{i}] input_type={q.get('input_type')}")
        p("DISPLAY:", q.get("display"))
        if q.get("options"): p("OPTIONS:", json.dumps(q["options"],ensure_ascii=False))
        p("SOLUTIONS:", json.dumps(q.get("solutions"),ensure_ascii=False))
        if q.get("chart"): p("CHART:", json.dumps(q["chart"],ensure_ascii=False))
        if q.get("image"): p("IMAGE:", q["image"])
        p("HINT:", q.get("hint"))
        for k,v in q.items():
            if k in ("display","options","solutions","chart","image","hint","guided_steps","misconceptions","input_type"): continue
            p(f"  other {k}:", json.dumps(v,ensure_ascii=False)[:300])
        p("MISCONCEPTIONS:")
        for j,m in enumerate(q.get("misconceptions",[])):
            p(f"  [{j}]", json.dumps(m,ensure_ascii=False))
        p("GUIDED_STEPS:")
        for j,s in enumerate(q.get("guided_steps",[])):
            p(f"  [{j}]", json.dumps(s,ensure_ascii=False))
p("="*70); p("GUIDED OPENER/TEACH")
p(json.dumps(live["guided"],ensure_ascii=False,indent=1))
p("="*70); p("TIER GUIDES")
p(json.dumps(live["tier_guides"],ensure_ascii=False,indent=1))
p("="*70); p("METHOD CARD")
p(json.dumps(live["method_card"],ensure_ascii=False,indent=1))
p("="*70); p("DESCRIPTIONS")
for k,v in live["problem_bank"].items():
    if k.endswith("_description"): p(k, v)
io.close()
print("done")
