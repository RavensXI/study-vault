import json

live = json.load(open("_CHK_L03_live.json", encoding="utf-8"))

# ---- em dash scan (student-facing strings; skip internal 'note') ----
EM = "—"
hits = []
def walk(o, path, in_note=False):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, f"{path}.{k}", in_note=(k == "note"))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{path}[{i}]", in_note)
    elif isinstance(o, str):
        if not in_note and EM in o:
            hits.append((path, o))
walk(live, "root")
print("EM DASH HITS:", len(hits))
for p, s in hits:
    print("  ", p, "::", s[:80])

# ---- preservation vs pre-dump ----
dump = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
# find entry for this lesson id
ID = "36364705-212f-4a63-a56c-839f1e986dc2"
entry = None
if isinstance(dump, list):
    for e in dump:
        if e.get("id") == ID or e.get("lesson_id") == ID:
            entry = e; break
elif isinstance(dump, dict):
    entry = dump.get(ID) or dump.get("algebra-L03")
    if entry is None:
        # maybe dict keyed by id -> practice_data
        for k, v in dump.items():
            if isinstance(v, dict) and v.get("id") == ID:
                entry = v; break
print("\nPRE-DUMP entry found:", entry is not None)
if entry is not None:
    pd = entry.get("practice_data", entry)
    for fld in ("related_videos", "topic_links", "worked_examples"):
        a = json.dumps(pd.get(fld), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(fld), sort_keys=True, ensure_ascii=False)
        print(f"  {fld}: {'UNCHANGED' if a==b else 'CHANGED'}")
        if a != b:
            print("    PRE :", a[:300])
            print("    LIVE:", b[:300])
