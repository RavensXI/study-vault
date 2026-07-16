import json

LID = "ab716e12-4427-45e8-9796-a9343073968a"
KEY = "algebra-L14"

live = json.load(open("_live_l14.json", encoding="utf-8"))

# Load pre-dump
pre = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
# find entry
entry = None
if isinstance(pre, list):
    for e in pre:
        if e.get("id") == LID or e.get("key") == KEY:
            entry = e
            break
elif isinstance(pre, dict):
    entry = pre.get(LID) or pre.get(KEY)
    if entry is None:
        # maybe keyed differently
        for k, v in pre.items():
            if isinstance(v, dict) and (v.get("id") == LID):
                entry = v
                break
print("pre-dump type:", type(pre).__name__)
if isinstance(pre, list):
    print("list len", len(pre), "sample keys", list(pre[0].keys())[:8] if pre else None)
elif isinstance(pre, dict):
    print("dict keys sample:", list(pre.keys())[:5])
print("entry found:", entry is not None)
if entry:
    print("entry keys:", list(entry.keys()))
