import json
data=json.load(open("_live_canonical.json"))[0]
pd=data["practice_data"]
s=json.dumps(pd, ensure_ascii=False)
# em dash search
import re
print("EM DASH count (—):", s.count("—"))
# board names
for term in ["AQA","Edexcel","OCR","WJEC","Eduqas","equation sheet","memorise this","on your"]:
    if term.lower() in s.lower():
        print("BOARD/SHEET TERM FOUND:", term)
print("done term scan")
# list accept fields per problem
pb=pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        acc=p.get("accept","NONE")
        exps=[m.get("expect") for m in p.get("misconceptions",[])]
        print(tier,i,"sol",p.get("solutions"),"accept",acc,"unit",p.get("unit","-"),"expects",exps)
