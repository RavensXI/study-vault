import json,re
d=json.load(open("_live_canon.json",encoding="utf-8"))
pb=d["problem_bank"]
print("problem_bank keys:", list(pb.keys()))
issues=[]
accs=set(); hos=set()
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0] if p.get("solutions") else None
        acc=p.get("accept"); accs.add(str(acc)); hos.add(str(p.get("higher_only")))
        win=acc if acc is not None else 0.005
        for k,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is not None and sol is not None and abs(e-sol)<=win:
                issues.append(f"{tier}[{i}].misconceptions[{k}] DEAD expect {e} within {win} of sol {sol}")
print("live accept set:", accs)
print("live higher_only set:", hos)
print("DEAD EXPECT ISSUES:", issues if issues else "none")
blob=json.dumps(d,ensure_ascii=False).lower()
for term in ["aqa","edexcel"," ocr","eduqas","wjec","equation sheet","memorise","memorize","on your sheet","em dash"]:
    if term in blob: print("TERM FOUND:", repr(term))
# em dash scan in student-facing
if "—" in json.dumps(d,ensure_ascii=False): print("EM DASH present")
else: print("no em dash")
print("scan done")
