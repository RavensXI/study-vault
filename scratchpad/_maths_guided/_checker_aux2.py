# -*- coding: utf-8 -*-
import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="1c2aa03c-fff3-4f9a-83f6-438c587b8948"
wl=json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\_worklist.json",encoding="utf-8"))
# find entry with this id
def findid(o):
    res=[]
    def rec(o):
        if isinstance(o,dict):
            if o.get("id")==ID or o.get("lesson_id")==ID: res.append(o)
            for v in o.values(): rec(v)
        elif isinstance(o,list):
            for v in o: rec(v)
    rec(o); return res
hits=findid(wl)
print("WORKLIST entry:", json.dumps(hits,ensure_ascii=False)[:600])
aud=json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_audit\_audit_result.json",encoding="utf-8"))
KEY=None
if hits: KEY=hits[0].get("key")
print("KEY=",KEY)
for sec in ["issues","unconfirmed","confirmed"]:
    lst=aud.get(sec,[])
    matched=[e for e in lst if isinstance(e,dict) and e.get("key")==KEY]
    print(f"--- {sec}: {len(matched)} for {KEY} ---")
    for e in matched: print(json.dumps(e,ensure_ascii=False))
