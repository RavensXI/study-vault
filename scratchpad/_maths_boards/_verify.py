import json,io
built=json.load(io.open("lesson_maths-aqa_algebra-L14.json",encoding="utf-8"))
# preservation vs predump
dump=json.load(io.open("_pre_dump_maths-aqa.json",encoding="utf-8"))
ID="f4814142-6434-44c9-9458-6b95f1e27ec6"
entry=None
if isinstance(dump,dict):
    entry=dump.get(ID) or (dump.get("lessons",{}) if False else None)
    if entry is None:
        for k,v in dump.items():
            if isinstance(v,dict) and v.get("id")==ID: entry=v.get("practice_data"); break
if entry is None and isinstance(dump,list):
    for row in dump:
        if row.get("id")==ID: entry=row.get("practice_data"); break
print("predump found:", entry is not None)
if entry:
    for f in ("related_videos","topic_links","worked_examples"):
        print(f,"preserved:", json.dumps(entry.get(f),sort_keys=True)==json.dumps(built.get(f),sort_keys=True))
# structure summary
pb=built["problem_bank"]
for t in ("bronze","silver","gold"):
    print(t, [p["solutions"] for p in pb[t]])
print("has guided:", "guided" in built, "tier_guides:", "tier_guides" in built)
print("keys:", sorted(built.keys()))
