import json
LID="fe5f6191-4452-4313-934d-8e5d16ba1032"
pre=[x for x in json.load(open("_pre_fanout_dump.json",encoding="utf-8")) if x["id"]==LID][0]["practice_data"]
live=json.load(open("_CHK_live_geomL02.json",encoding="utf-8"))
for i,(a,b) in enumerate(zip(pre["worked_examples"],live["worked_examples"])):
    for j,(sa,sb) in enumerate(zip(a["steps"],b["steps"])):
        if sa!=sb:
            print(f"WE[{i}].steps[{j}] label: PRE={sa['label']!r} LIVE={sb['label']!r}")
            if sa.get('content')!=sb.get('content'):
                print("   content differs PRE:",sa['content'],"LIVE:",sb['content'])
# em dash scan in live student-facing
import re
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            yield from walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            yield from walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o or "–" in o:
            yield (path,o)
print("\n--- em/en dashes in live (excluding note) ---")
for p,s in walk(live):
    print(p, repr(s[:80]))
