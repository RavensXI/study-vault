import json,re
pd=json.load(open("_live_48cb4395.json",encoding="utf-8"))
s=json.dumps(pd,ensure_ascii=False)
# board names / equation-sheet claims
for term in ["AQA","Edexcel","OCR","Eduqas","WJEC","equation sheet","memorise","on your sheet","formula sheet","given to you in the exam"]:
    if term.lower() in s.lower():
        print("BOARD/SHEET TERM FOUND:",term)
# em dash in student-facing (rough: any em dash)
if "—" in s: print("EM DASH found")
else: print("no em dash")
# expects vs accept
def check(prob,path):
    sol=prob.get("solutions",[None])[0]
    acc=prob.get("accept",0)
    for i,m in enumerate(prob.get("misconceptions",[])):
        e=m.get("expect")
        if e is None: continue
        if sol is not None and abs(e-sol)<=acc:
            print(f"DEAD EXPECT {path}.misc[{i}] expect={e} sol={sol} accept={acc}")
pb=pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        check(p,f"{tier}[{i}]")
print("expect check done")
