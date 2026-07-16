# -*- coding: utf-8 -*-
import json, io, re

live=json.load(io.open("_chk_live_fresh.json",encoding="utf-8"))

# --- em dash scan (student-facing; note fields exempt) ---
EM="—"
hits=[]
def walk(o, path, in_note=False):
    if isinstance(o, dict):
        for k,v in o.items():
            walk(v, f"{path}.{k}", in_note=(k=="note"))
    elif isinstance(o, list):
        for i,v in enumerate(o):
            walk(v, f"{path}[{i}]", in_note)
    elif isinstance(o, str):
        if not in_note and EM in o:
            hits.append((path,o))
print("EM DASH student-facing hits:", len(hits))
for p,s in hits: print("  ",p,"::",s[:80])

# --- preservation vs pre-dump ---
try:
    dump=json.load(io.open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\_pre_fanout_dump.json",encoding="utf-8"))
    # find the lesson entry
    ID="d9df7fae-d515-4c06-94b6-9068029bd037"
    entry=None
    if isinstance(dump, dict):
        if ID in dump: entry=dump[ID]
        else:
            for k,v in dump.items():
                if isinstance(v,dict) and v.get("id")==ID: entry=v; break
    elif isinstance(dump, list):
        for v in dump:
            if isinstance(v,dict) and v.get("id")==ID: entry=v; break
    if entry is None:
        print("PRE-DUMP: entry not found; dump type", type(dump).__name__,
              "top keys sample:", (list(dump.keys())[:3] if isinstance(dump,dict) else "list len %d"%len(dump)))
    else:
        pd_old = entry.get("practice_data", entry)
        for f in ["related_videos","topic_links","worked_examples"]:
            same = json.dumps(pd_old.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
            print(f"PRESERVE {f}: {'UNCHANGED' if same else 'CHANGED'}")
            if not same:
                print("   OLD:", json.dumps(pd_old.get(f),ensure_ascii=False)[:300])
                print("   NEW:", json.dumps(live.get(f),ensure_ascii=False)[:300])
except FileNotFoundError:
    print("PRE-DUMP file not found")
