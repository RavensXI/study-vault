import json

ID = "c6b90b84-f603-4dea-8d46-f7205879bc89"
p = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\_pre_fanout_dump.json"
with open(p, encoding="utf-8") as f:
    dump = json.load(f)

# find entry
def find(obj):
    if isinstance(obj, dict):
        if obj.get("id") == ID:
            return obj
        for v in obj.values():
            r = find(v)
            if r: return r
    elif isinstance(obj, list):
        for v in obj:
            r = find(v)
            if r: return r
    return None

entry = None
if isinstance(dump, list):
    for e in dump:
        if isinstance(e, dict) and e.get("id") == ID:
            entry = e; break
if entry is None:
    entry = find(dump)

if entry is None:
    print("NOT FOUND. top type:", type(dump))
    if isinstance(dump, dict):
        print("keys sample:", list(dump.keys())[:10])
        # maybe keyed by id
        if ID in dump:
            entry = {"id": ID, "practice_data": dump[ID]}
            print("found by key")
if entry:
    pd = entry.get("practice_data", entry)
    out = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\_CHK_graphsL03_PREDUMP.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(pd, f, indent=2, ensure_ascii=False)
    print("WROTE predump. keys:", list(pd.keys()) if isinstance(pd, dict) else type(pd))
