# -*- coding: utf-8 -*-
import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_CHK_L04_live.json",encoding="utf-8"))["practice_data"]
# write practice_data alone for validator
json.dump(pd,open("_CHK_L04_pdonly.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
# check descriptions for mojibake / bad chars
pb=pd["problem_bank"]
for key in ["bronze_description","silver_description","gold_description"]:
    s=pb[key]
    print(key,"=>",repr(s))
    for ch in s:
        if ord(ch)>0x2500 or ch=="�":
            print("   NON-STD CHAR:",repr(ch),hex(ord(ch)))
# em dash sweep across all student-facing strings
import re
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,path+"/"+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o or "–" in o:
            # skip internal note fields
            if not path.endswith("/note"):
                print("DASH at",path,":",repr(o[:80]))
walk(pd)
print("em-dash sweep done")
