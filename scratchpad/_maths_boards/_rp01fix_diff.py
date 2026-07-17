# -*- coding: utf-8 -*-
import json
old = json.load(open("_chk_eduqasS_rp01_live.json", encoding="utf-8"))
new = json.load(open("lesson_maths-eduqas_ratio-proportion-L01.json", encoding="utf-8"))

def walk(a, b, path=""):
    diffs = []
    if type(a) != type(b):
        diffs.append((path, "TYPE", a, b)); return diffs
    if isinstance(a, dict):
        for k in set(a) | set(b):
            if k not in a: diffs.append((path+"."+k, "ADDED", None, b[k]))
            elif k not in b: diffs.append((path+"."+k, "REMOVED", a[k], None))
            else: diffs += walk(a[k], b[k], path+"."+k)
    elif isinstance(a, list):
        if len(a) != len(b):
            diffs.append((path, "LEN", len(a), len(b)))
        for i in range(min(len(a), len(b))):
            diffs += walk(a[i], b[i], path+"[%d]"%i)
    else:
        if a != b: diffs.append((path, "CHANGED", a, b))
    return diffs

for d in walk(old, new):
    print(d[0], "|", d[1])
    print("   OLD:", repr(d[2])[:200])
    print("   NEW:", repr(d[3])[:200])
print("total diff fields:", len(walk(old, new)))
