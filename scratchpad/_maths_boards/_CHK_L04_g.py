# -*- coding: utf-8 -*-
import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_CHK_L04_live.json",encoding="utf-8"))["practice_data"]
g=pd["guided"]
print("### OPENER ###")
op=g["opener"]
print(json.dumps(op,ensure_ascii=False,indent=1))
print("\n### TEACH ###")
for tier in ["bronze","silver","gold"]:
    t=g["teach"][tier]
    print(f"\n--- teach.{tier} ---")
    print(json.dumps(t,ensure_ascii=False,indent=1))
