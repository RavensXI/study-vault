import json
pre = json.load(open("_pre_dump_all.json", encoding="utf-8"))
live = json.load(open("_live_3c4aa292.json", encoding="utf-8"))
# pre_dump keyed by id?
cid = "3c4aa292-cf3a-4cda-876d-25b030880bb5"
entry = None
if isinstance(pre, dict):
    entry = pre.get(cid)
    if entry is None:
        # maybe keyed by workkey
        for k,v in pre.items():
            if isinstance(v,dict) and (v.get("id")==cid or v.get("canonical_id")==cid):
                entry=v; break
print("pre entry found:", entry is not None, "| top keys of pre:", list(pre.keys())[:5] if isinstance(pre,dict) else type(pre))
