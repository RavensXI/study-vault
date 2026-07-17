import json, re

ID = "f4f1368e-d7c2-41f1-8459-de2c0d500c3b"
live = json.load(open("_CHK_aqaL01_live.json", encoding="utf-8"))

# --- pre-dump lookup ---
pre_raw = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))
def find_entry(obj):
    # pre-dump could be list of rows or dict keyed by id
    if isinstance(obj, list):
        for r in obj:
            if isinstance(r, dict) and r.get("id") == ID:
                return r
    if isinstance(obj, dict):
        if ID in obj:
            return obj[ID]
        # maybe keyed differently
        for k, v in obj.items():
            if isinstance(v, dict) and v.get("id") == ID:
                return v
    return None
entry = find_entry(pre_raw)
print("pre-dump type:", type(pre_raw).__name__, "len:", len(pre_raw) if hasattr(pre_raw,'__len__') else '?')
if entry is None:
    print("!! could not find pre entry by id; top-level sample keys:")
    if isinstance(pre_raw, dict):
        print(list(pre_raw.keys())[:5])
    elif isinstance(pre_raw, list) and pre_raw:
        print("first row keys:", list(pre_raw[0].keys())[:10])
else:
    pre_pd = entry.get("practice_data", entry)
    print("pre keys:", list(pre_pd.keys()))
    for f in ["related_videos", "topic_links", "worked_examples"]:
        a = json.dumps(pre_pd.get(f), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
        print(f"{f}: {'SAME' if a==b else 'CHANGED'}")
        if a != b:
            print("  PRE :", a[:400])
            print("  LIVE:", b[:400])

# --- em dash scan across student-facing strings ---
print("\n=== EM DASH / style scan ===")
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            # skip internal note fields
            if k == "note":
                continue
            walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        if "—" in o:  # em dash
            print(f"EM DASH at {path}: {o[:80]}")
        if "–" in o:  # en dash
            print(f"EN DASH at {path}: {o[:80]}")
walk(live)
print("(scan done)")
