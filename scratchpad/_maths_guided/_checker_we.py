# -*- coding: utf-8 -*-
import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="1c2aa03c-fff3-4f9a-83f6-438c587b8948"
live=json.load(open("_live_L02.json",encoding="utf-8"))
pre=json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\_pre_fanout_dump.json",encoding="utf-8"))
def find(o):
    if isinstance(o,dict):
        if o.get("id")==ID: return o
        for v in o.values():
            r=find(v)
            if r: return r
    elif isinstance(o,list):
        for v in o:
            r=find(v)
            if r: return r
pe=find(pre); ppd=pe["practice_data"]
# flatten strings from worked_examples and compare
def strs(o,p=""):
    out=[]
    if isinstance(o,dict):
        for k,v in o.items(): out+=strs(v,p+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): out+=strs(v,f"{p}[{i}]")
    else: out.append((p,o))
    return out
ps=dict(strs(ppd["worked_examples"],"we"))
ls=dict(strs(live["worked_examples"],"we"))
print("== worked_examples string diffs ==")
for k in ps:
    if k in ls and ps[k]!=ls[k]:
        print("PATH",k,"\n  PRE :",repr(ps[k]),"\n  LIVE:",repr(ls[k]))
# em dash scan across all student-facing strings in live
def scan(o,p=""):
    hits=[]
    if isinstance(o,dict):
        for k,v in o.items(): hits+=scan(v,p+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): hits+=scan(v,f"{p}[{i}]")
    else:
        if isinstance(o,str) and "—" in o: hits.append((p,o))
    return hits
# exclude internal note fields
emd=[h for h in scan(live) if ".note" not in h[0]]
print("\n== EM DASH (U+2014) hits (excl note) ==", len(emd))
for h in emd[:40]: print(h)
