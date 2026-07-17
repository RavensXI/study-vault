import json, re
live=json.load(open("_CK_geoL08_live.json",encoding="utf-8"))["practice_data"]
pre=json.load(open("_pre_dump_maths-aqa.json",encoding="utf-8"))
ID="3e214279-84c2-41dc-a639-94bda78e2da8"
pp=[r for r in pre if r["id"]==ID][0]["practice_data"]
def strip(s):
    s=re.sub(r'<svg.*?</svg>','[SVG]',s,flags=re.S)
    s=re.sub(r'<span class="figure-caption">.*?</span>','',s)
    return s.strip()
for tier in ["bronze","silver","gold"]:
    lb=live["problem_bank"][tier]; pb=pp["problem_bank"].get(tier,[])
    print(f"\n=== {tier}: live {len(lb)} pre {len(pb)} ===")
    for i,p in enumerate(lb):
        disp=strip(p["display"])
        sol=p.get("solutions")
        # find matching pre by fuzzy display (strip svg)
        pre_sol=None
        if i < len(pb):
            pre_disp=strip(pb[i]["display"])
            pre_sol=pb[i].get("solutions")
            changed = pre_disp!=disp or pre_sol!=sol
            flag="CHANGED" if changed else "same"
        else:
            flag="NEW"
        print(f"[{i}] sol={sol} pre_sol={pre_sol} {flag}")
        print("     Q:", disp[:110])
