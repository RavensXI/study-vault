import json
ID="7f378aaa-68dc-4420-b952-f56d8349b1ed"
dump=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
# dump could be list or dict
entry=None
if isinstance(dump,list):
    for r in dump:
        if r.get("id")==ID: entry=r; break
elif isinstance(dump,dict):
    entry=dump.get(ID) or (dump if dump.get("id")==ID else None)
    if entry is None:
        # maybe keyed by id
        for k,v in dump.items():
            if isinstance(v,dict) and (v.get("id")==ID or k==ID): entry=v;break
print("found entry:",entry is not None, "type:",type(dump).__name__)
if entry is None:
    print("top type keys sample:", list(dump)[:3] if isinstance(dump,dict) else [r.get('id') for r in dump[:3]])
    raise SystemExit
pdold=entry.get("practice_data",entry)
live=json.load(open("_rechk_live.json",encoding="utf-8"))
for f in ["related_videos","topic_links","worked_examples"]:
    o=pdold.get(f); n=live.get(f)
    same=json.dumps(o,sort_keys=True,ensure_ascii=False)==json.dumps(n,sort_keys=True,ensure_ascii=False)
    print(f"\n{f}: present_old={o is not None} present_live={n is not None} IDENTICAL={same}")
    if not same:
        print("  OLD:",json.dumps(o,ensure_ascii=False)[:400])
        print("  NEW:",json.dumps(n,ensure_ascii=False)[:400])
print("\nold top keys:",list(pdold.keys()))
print("live top keys:",list(live.keys()))
