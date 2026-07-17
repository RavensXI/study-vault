# -*- coding: utf-8 -*-
import json, io
live = json.load(io.open("_CHK_graphsL08_live.json", encoding="utf-8"))
pb = live["problem_bank"]

def show(tier,i):
    p=pb[tier][i]
    print(f"\n== {tier}[{i}] sol={p.get('solutions')} it={p.get('input_type')}")
    print("  disp:", p['display'][:90].replace(chr(10)," "))
    for m in p.get('misconceptions',[]):
        print(f"   [{m['pattern']}] expect={m['expect']} note={m.get('note')}")

for tier in ['gold','bronze','silver']:
    for i in range(len(pb[tier])):
        show(tier,i)
