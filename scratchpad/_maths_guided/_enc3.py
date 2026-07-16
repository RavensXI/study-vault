import json
pd=json.load(open("_live_check.json",encoding="utf-8"))
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        yield path,o
# True double-encode marker: presence of U+00C2 or U+00C3 (Â/Ã) which only appear in mojibake
bad=[]
for p,s in walk(pd):
    if any(ord(c) in (0xC2,0xC3) for c in s):
        bad.append(p)
print("LIVE double-encoded field count:", len(bad))

# Now the pre-dump for this lesson
import io
dump=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
print("pre-dump top type:", type(dump).__name__)
# find our lesson
ID="bc1ac13e-1cc0-42b3-a805-a8a3f35cbabb"
entry=None
if isinstance(dump,list):
    for e in dump:
        if isinstance(e,dict) and e.get("id")==ID: entry=e
elif isinstance(dump,dict):
    entry=dump.get(ID) or dump.get("lessons",{}).get(ID) if isinstance(dump.get("lessons"),dict) else None
print("found entry:", entry is not None)
if entry:
    ppd=entry.get("practice_data") or entry.get("practice_data".upper()) or entry
    predbad=[]
    for p,s in walk(ppd):
        if any(ord(c) in (0xC2,0xC3) for c in s):
            predbad.append(p)
    print("PRE-DUMP double-encoded count:", len(predbad))
    for b in predbad[:10]: print("   pre:",b)
