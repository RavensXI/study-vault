import json

live = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\_live_geometry-L07.json", encoding="utf-8"))
dump = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\_pre_fanout_dump.json", encoding="utf-8"))

# find pre-dump entry
pre = None
ID = "aee11210-c33f-4e61-a25e-1ef101e95ab3"
def find(o):
    if isinstance(o, dict):
        if o.get("id") == ID and "practice_data" in o:
            return o["practice_data"]
        for v in o.values():
            r = find(v)
            if r: return r
    elif isinstance(o, list):
        for v in o:
            r = find(v)
            if r: return r
    return None
pre = find(dump)
if pre is None:
    # maybe dump keyed by id
    if ID in dump:
        pre = dump[ID].get("practice_data", dump[ID])
    else:
        for k,v in (dump.items() if isinstance(dump,dict) else []):
            if isinstance(v,dict) and v.get("id")==ID:
                pre = v.get("practice_data")
print("pre found:", pre is not None)
if pre:
    for fld in ["related_videos","topic_links","worked_examples"]:
        a = json.dumps(pre.get(fld), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(fld), sort_keys=True, ensure_ascii=False)
        print(f"{fld}: {'SAME' if a==b else 'DIFFERENT'}")
        if a != b:
            print("  PRE :", a[:400])
            print("  LIVE:", b[:400])
    print("pre keys:", sorted(pre.keys()))
    print("live keys:", sorted(live.keys()))

# em dash scan in student-facing strings
def walk(o, path=""):
    if isinstance(o, dict):
        for k,v in o.items():
            walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o):
            walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        if "—" in o or "–" in o:
            # exempt internal note
            if not path.endswith(".note"):
                print("DASH at", path, ":", o[:80])
walk(live)
print("dash scan done")
