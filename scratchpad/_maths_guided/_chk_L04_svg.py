import json,sys,io,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_CHK_L04_live.json",encoding="utf-8"))["practice_data"]
pb=pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        disp=p.get("display","")
        for m in re.finditer(r'<svg.*?</svg>',disp,flags=re.S):
            print(f"\n########## {tier}[{i}] SVG ##########")
            print(m.group(0))
