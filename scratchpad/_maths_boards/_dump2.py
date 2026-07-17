import json, io
pd=json.load(io.open("_live_graphs-L01.json",encoding="utf-8"))["practice_data"]
out=io.open("_dump2.txt","w",encoding="utf-8")
def p(*a): print(*a,file=out)
g=pd["guided"]
p("### OPENER ###")
op=g.get("opener")
p(json.dumps(op,ensure_ascii=False,indent=1))
p("\n### TEACH ###")
for tier in ["bronze","silver","gold"]:
    t=g.get("teach",{}).get(tier)
    p("--- teach",tier,"---")
    p(json.dumps(t,ensure_ascii=False,indent=1))
p("\n### TIER_GUIDES ###")
p(json.dumps(pd.get("tier_guides"),ensure_ascii=False,indent=1))
p("\n### METHOD_CARD ###")
p(json.dumps(pd.get("method_card"),ensure_ascii=False,indent=1))
out.close()
print("ok")
