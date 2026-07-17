import json
pre=json.load(open("_pre_dump_maths-aqa.json",encoding="utf-8"))
live=json.load(open("_live_gl02.json",encoding="utf-8"))
ID="96f5aef3-e4c8-4faf-ba82-1d587dc4e10e"
entry=[r["practice_data"] for r in pre if r.get("id")==ID][0]
for tier in ["bronze","silver","gold"]:
    pb=entry["problem_bank"][tier]; lb=live["problem_bank"][tier]
    print(f"=== {tier}: pre {len(pb)} live {len(lb)}")
    for i,(p,l) in enumerate(zip(pb,lb)):
        pd=p.get("display","").replace("\n"," ")
        ld=l.get("display","")
        # strip svg
        import re
        ld_txt=re.sub(r"<svg.*?</svg>","[SVG]",ld,flags=re.S)
        if pd!=ld_txt or p.get("solutions")!=l.get("solutions"):
            print(f" [{i}] DISPLAY/SOL CHANGED")
            print(f"   pre sol {p.get('solutions')} disp: {pd[:120]}")
            print(f"   liv sol {l.get('solutions')} disp: {ld_txt[:120]}")
