import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
live = json.load(open("_ck_L01_live.json", encoding="utf-8"))

hits=[]
def walk(o, path):
    if isinstance(o, dict):
        for k,v in o.items():
            # note fields are exempt
            if k == "note":
                continue
            walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o):
            walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        if "—" in o or "–" in o:
            hits.append((path, o))

walk(live, "root")
print("EM/EN DASH hits (excl note):", len(hits))
for p,s in hits:
    print(" ", p, "::", s[:80])

# entity check
import re
ent=[]
def walk2(o,path):
    if isinstance(o,dict):
        for k,v in o.items(): walk2(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): walk2(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if re.search(r"&[a-z]+;|&#\d+;", o): ent.append((path,o))
walk2(live,"root")
print("\nHTML entity hits:", len(ent))
for p,s in ent: print(" ",p,"::",s[:80])

# hints plain text (no latex/html)
print("\n-- hint checks --")
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        h=p.get("hint","")
        bad = ("\\(" in h) or ("<" in h)
        if bad: print("  BAD hint", tier, i, h)
print("hints scanned")
