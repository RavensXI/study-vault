import json, re
live = json.load(open("_checker_live_L06.json",encoding="utf-8"))

# 1. em dash scan (student-facing). Exclude internal 'note' fields.
emdash_hits=[]
def scan(obj, path, in_note=False):
    if isinstance(obj, dict):
        for k,v in obj.items():
            scan(v, f"{path}.{k}", in_note=(k=="note"))
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            scan(v, f"{path}[{i}]", in_note)
    elif isinstance(obj, str):
        if not in_note and "—" in obj:
            emdash_hits.append(path)
scan(live,"root")
print("EM DASH hits:", emdash_hits)

# 2. Preservation vs pre-dump
dump = json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
# find L06 entry
entry=None
if isinstance(dump, list):
    for e in dump:
        if e.get("id")=="f6f5708d-edf9-42e6-81d8-49c3cf282310":
            entry=e; break
elif isinstance(dump, dict):
    entry = dump.get("f6f5708d-edf9-42e6-81d8-49c3cf282310")
print("dump type:", type(dump).__name__, "found entry:", entry is not None)
if entry:
    pdold = entry.get("practice_data", entry)
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(pdold.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
