import json, re

live=json.load(open("_LIVE_eduqas_probstat_L02.json",encoding="utf-8"))

# 1. Em dash scan across all student-facing strings
EM="—"
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            # skip internal note fields
            if k=="note": continue
            walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if EM in o:
            print("EMDASH:",path,repr(o[:80]))
walk(live)
print("emdash scan done")

# 2. Check pre-dump preservation
pre=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
# pre may be a list of rows or dict
print("pre type:",type(pre))
if isinstance(pre,dict):
    print("pre keys sample:",list(pre.keys())[:5])
