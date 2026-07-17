import json, io

ID = "5cfec765-3128-469b-9d6a-626f042d6161"
pre = json.load(io.open("_pre_dump_maths-aqa.json", encoding="utf-8"))
# pre could be list of rows or dict
def find(obj):
    if isinstance(obj, list):
        for r in obj:
            if isinstance(r, dict) and r.get("id") == ID:
                return r
    if isinstance(obj, dict):
        if obj.get("id") == ID:
            return obj
        for v in obj.values():
            r = find(v)
            if r: return r
    return None

row = find(pre)
print("found pre row:", bool(row))
if row:
    pd = row.get("practice_data") or {}
    print("pre keys:", list(pd.keys()))
    for k in ("related_videos","topic_links","worked_examples"):
        print("---", k, "---")
        print(json.dumps(pd.get(k), ensure_ascii=False)[:1500])
    # dump the pre problem_bank displays and solutions for comparison
    pb = pd.get("problem_bank") or {}
    for t in ("bronze","silver","gold"):
        arr = pb.get(t) or []
        print(f"=== pre {t} ({len(arr)}) ===")
        for i,p in enumerate(arr):
            print(f"  {t}[{i}] sols={p.get('solutions')} disp={p.get('display')}")
