import json

ID = "769be867-fe49-4cf1-b45f-1308b21e81dd"
live = json.load(open("_chk_number_L05_live.json", encoding="utf-8"))["practice_data"]

# 1. Em-dash sweep on student-facing strings (exclude internal 'note')
def walk(obj, path=""):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "note":
                continue
            out += walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += walk(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if "—" in obj:
            out.append(("EMDASH", path, obj))
    return out

emdash = walk(live)
print("EM DASHES:", len(emdash))
for _, p, s in emdash:
    print("  ", p, "::", s[:80])

# 2. Preservation vs pre-dump
pre = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))
# find entry for this ID
entry = None
if isinstance(pre, dict):
    if ID in pre:
        entry = pre[ID]
    else:
        for k, v in pre.items():
            if isinstance(v, dict) and v.get("id") == ID:
                entry = v; break
elif isinstance(pre, list):
    for v in pre:
        if v.get("id") == ID:
            entry = v; break
print("\nPRE-DUMP entry found:", entry is not None)
if entry is not None:
    pdpre = entry.get("practice_data", entry)
    for fld in ("related_videos", "topic_links", "worked_examples"):
        a = json.dumps(pdpre.get(fld), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(fld), sort_keys=True, ensure_ascii=False)
        print(f"  {fld}: {'SAME' if a==b else 'CHANGED'}")
        if a != b:
            print("    PRE :", a[:300])
            print("    LIVE:", b[:300])
    print("  pre keys:", list(pdpre.keys()))
