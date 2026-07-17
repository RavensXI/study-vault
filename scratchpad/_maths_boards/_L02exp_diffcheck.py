# -*- coding: utf-8 -*-
import json, io
live=json.load(io.open("_L02exp_live.json",encoding="utf-8"))["practice_data"]
patched=json.load(io.open("_L02exp_patched_pd.json",encoding="utf-8"))
# only worked_examples should differ
assert set(live.keys())==set(patched.keys()), "key sets differ"
for k in live:
    a=json.dumps(live[k],ensure_ascii=False,sort_keys=True)
    b=json.dumps(patched[k],ensure_ascii=False,sort_keys=True)
    same = a==b
    print(f"{k:16} {'SAME' if same else 'CHANGED'}")
# maths recompute of restored worked_examples
print("--- recompute worked_examples ---")
we=patched["worked_examples"]
# [0] 3(x+4) -> 3x+12
print("[0]", we[0]["question"], "-> answer step:", we[0]["steps"][-1]["content"])
# [1] (x+2)(x+5)=x^2+7x+10
print("[1]", we[1]["question"], "-> answer step:", we[1]["steps"][-1]["content"])
# [2] (2x-1)(3x+4)=6x^2+5x-4
print("[2]", we[2]["question"], "-> answer step:", we[2]["steps"][-1]["content"])
# mojibake / dash scan on worked_examples only
s=json.dumps(we,ensure_ascii=False)
print("em-dash:", s.count("—"), "en-dash:", s.count("–"), "replacement-char:", s.count("�"))
