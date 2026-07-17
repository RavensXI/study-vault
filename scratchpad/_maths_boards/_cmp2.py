# -*- coding: utf-8 -*-
import json,re
pre=json.load(open("_pre_pd.json",encoding="utf-8"))["problem_bank"]
live=json.load(open("_checker_live.json",encoding="utf-8"))["problem_bank"]
def strip_svg(s): return re.sub(r"<svg.*?</svg>","",s or "",flags=re.S).strip()
for t,i in [("gold",0),("gold",3),("silver",3),("silver",4)]:
    p=strip_svg(pre[t][i]["display"]); l=strip_svg(live[t][i]["display"])
    print(t,i,"text-match:",p==l)
    # also confirm options preserved for MC
    if pre[t][i].get("options"):
        print("   options-match:", pre[t][i]["options"]==live[t][i]["options"])
