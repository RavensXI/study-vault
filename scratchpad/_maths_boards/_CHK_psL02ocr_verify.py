import json, re

live = json.load(open("_CHK_psL02ocr_live.json", encoding="utf-8"))
pd = live["practice_data"]

# 1. Em-dash scan on student-facing strings (skip internal 'note')
EMDASH = "—"
def walk(o, path):
    if isinstance(o, dict):
        for k,v in o.items():
            if k == "note":  # internal exempt
                continue
            walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o):
            walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        if EMDASH in o:
            print(f"EMDASH at {path}: {o[:80]}")

walk(pd, "pd")
print("em-dash scan done")

# 2. Fraction reduce helper
from math import gcd
def red(n,d):
    g=gcd(n,d); return (n//g, d//g)

# 3. Check misconception expects are plausible numbers / fraction reductions
print("\n--- used_total fraction reductions ---")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        for mc in p.get("misconceptions",[]):
            exp = mc.get("expect")
            print(f"{tier}[{i}] {mc.get('pattern')}: expect={exp}")
