import json
# Read raw bytes of a known money string
pd=json.load(open("_live_check.json",encoding="utf-8"))
s=pd["problem_bank"]["gold"][0]["hint"]
print("HINT repr:", repr(s))
print("Chars:", [hex(ord(c)) for c in s if ord(c)>127])
# check em dash and minus signs
import re
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        yield path,o
emdash=[]; mojibake=[]
for p,s in walk(pd):
    if "—" in s: emdash.append(p)
    if "Â" in s or "Ã" in s or "ƒ" in s: mojibake.append((p,s[:40]))
print("EMDASH paths:",emdash)
print("MOJIBAKE count:",len(mojibake))
for m in mojibake[:5]: print("  ",m)
