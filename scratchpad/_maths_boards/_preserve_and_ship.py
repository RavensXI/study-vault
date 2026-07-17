import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
live = json.load(open("_L09_live_fresh.json", encoding="utf-8"))["practice_data"]

# Preservation check vs pre-dump
pre = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))
# pre may be list or dict keyed by id/slug
entry = None
if isinstance(pre, list):
    for r in pre:
        if r.get("id")=="5ff3e1eb-2284-4096-af06-4bcb6754b0e1" or r.get("slug")=="simultaneous-equations-linear":
            entry = r; break
elif isinstance(pre, dict):
    entry = pre.get("5ff3e1eb-2284-4096-af06-4bcb6754b0e1") or pre.get("simultaneous-equations-linear")
    if entry is None:
        # maybe keyed differently
        for k,v in pre.items():
            if isinstance(v,dict) and (v.get("slug")=="simultaneous-equations-linear"):
                entry=v; break
print("pre-dump entry found:", entry is not None, "| pre type:", type(pre).__name__)
if entry is not None:
    ppd = entry.get("practice_data", entry)
    for f in ("related_videos","topic_links","worked_examples"):
        same = json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"  {f} preserved byte-equal: {same}")
        if not same:
            print("    PRE:", json.dumps(ppd.get(f),ensure_ascii=False)[:200])
            print("    NOW:", json.dumps(live.get(f),ensure_ascii=False)[:200])

# Em dash scan on all student-facing strings (skip 'note')
EM="—"
hits=[]
def scan(o,p):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,p+"."+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,p+f"[{i}]")
    elif isinstance(o,str) and EM in o:
        hits.append(p)
scan(live,"pd")
print("em-dash hits:", hits)

# Write shard from verified live data
json.dump(live, open("lesson_maths-aqa_algebra-L09.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("shard written.")
