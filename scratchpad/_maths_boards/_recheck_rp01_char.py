import json
pre = json.load(open("_recheck_rp01_pre.json", encoding="utf-8"))
live = json.load(open("_recheck_rp01_live.json", encoding="utf-8"))
p=pre["method_card"]["content"]
# context around 392
seg=p[380:410]
print("PRE method_card ctx:", repr(seg))
print("codepoints:", [hex(ord(c)) for c in p[390:396]])
# worked example 0 question and steps raw
for idx in range(3):
    pe=pre["worked_examples"][idx]
    le=live["worked_examples"][idx]
    print(f"\n--- WE[{idx}] question PRE: {pe['question']!r}")
    print(f"--- WE[{idx}] question LIVE: {le['question']!r}")
    for s in pe["steps"]:
        if any(ord(c)>0x2000 and ord(c)<0x2030 for c in s.get('content','')):
            pass
# Find all chars in 0x2010-0x2015 range (dashes) anywhere in pre worked_examples/method_card
import re
def scan(obj,path=""):
    if isinstance(obj,str):
        for c in obj:
            if 0x2010<=ord(c)<=0x2015:
                print(f"  DASH {hex(ord(c))} at {path}: ...{obj[max(0,obj.index(c)-15):obj.index(c)+15]!r}")
                break
    elif isinstance(obj,dict):
        for k,v in obj.items(): scan(v,path+"."+k)
    elif isinstance(obj,list):
        for i,v in enumerate(obj): scan(v,f"{path}[{i}]")
print("\n=== dash scan in PRE method_card + worked_examples ===")
scan(pre["method_card"],"method_card")
scan(pre["worked_examples"],"worked_examples")
print("=== dash scan in LIVE (should be none in student-facing) ===")
scan(live,"")
