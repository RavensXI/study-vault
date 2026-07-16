import json, re

ID = "4d1ac99e-f293-4cce-a4d3-c276c5f8f24b"
live = json.load(open("_CHK_algL08_live.json", encoding="utf-8"))

# ---- em dash search in student-facing strings ----
EM = "—"
def walk(obj, path):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            # note fields are exempt
            if k == "note":
                continue
            hits += walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += walk(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if EM in obj:
            hits.append((path, obj))
    return hits

emhits = walk(live, "root")
print("EM DASH HITS:", len(emhits))
for p, s in emhits:
    print("  ", p, "::", s[:80])

# ---- preservation: find pre-dump entry ----
pre = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
entry = None
if isinstance(pre, dict):
    if ID in pre:
        entry = pre[ID]
    else:
        for k, v in pre.items():
            if isinstance(v, dict) and v.get("id") == ID:
                entry = v
                break
elif isinstance(pre, list):
    for v in pre:
        if isinstance(v, dict) and v.get("id") == ID:
            entry = v
            break
print("\nPredump entry found:", entry is not None)
if entry is not None:
    pd = entry.get("practice_data", entry)
    for f in ["related_videos", "topic_links", "worked_examples"]:
        a = json.dumps(pd.get(f), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
        print(f"  {f}: {'UNCHANGED' if a==b else 'CHANGED'}")
        if a != b:
            print("    PRE:", a[:300])
            print("    NOW:", b[:300])
    print("  predump keys:", list(pd.keys()))
