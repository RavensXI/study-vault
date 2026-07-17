# -*- coding: utf-8 -*-
import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_CHK_L04_live.json",encoding="utf-8"))["practice_data"]
pb=pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    sols=[p["solutions"][0] for p in pb[tier]]
    print(tier,"solutions:",sols,"dups:",len(sols)!=len(set(sols)))
    for i,p in enumerate(pb[tier]):
        d=p["display"]
        claims = ("graph shows" in d.lower()) or ("graph:" in d.lower())
        hasfig = ("chart" in p) or ("<svg" in d)
        if claims and not hasfig:
            print(f"  !! {tier}[{i}] text claims a graph but NO figure: {d[:90]!r}")
