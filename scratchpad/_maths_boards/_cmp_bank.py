# -*- coding: utf-8 -*-
import json,re
pre=json.load(open("_pre_pd.json",encoding="utf-8"))["problem_bank"]
live=json.load(open("_checker_live.json",encoding="utf-8"))["problem_bank"]
def strip_svg(s): return re.sub(r"<svg.*?</svg>","[SVG]",s or "",flags=re.S).strip()
for t in ["bronze","silver","gold"]:
    print("=====",t)
    pa,la=pre[t],live[t]
    print(" pre count",len(pa),"live count",len(la))
    for i,(p,l) in enumerate(zip(pa,la)):
        pd_=strip_svg(p.get("display",""))
        ld_=strip_svg(l.get("display",""))
        ds = "SAME" if pd_==ld_ else "DIFF"
        ss = "SAME" if p.get("solutions")==l.get("solutions") else "DIFF"
        line=f"  [{i}] disp={ds} sol={ss} live_sol={l.get('solutions')} it={l.get('input_type')}"
        try: print(line)
        except: print(line.encode('ascii','replace').decode())
        if ds=="DIFF":
            try: print("     PRE :",pd_); print("     LIVE:",ld_)
            except: print("     (diff, non-ascii)")
        if ss=="DIFF":
            print("     PRE sol:",p.get("solutions"),"LIVE sol:",l.get("solutions"))
