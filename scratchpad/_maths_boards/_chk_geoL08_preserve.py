import json

LID = "7f378aaa-68dc-4420-b952-f56d8349b1ed"
live = json.load(open("_chk_geoL08_live.json", encoding="utf-8"))["practice_data"]

# Load pre-dump
pre = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))
# figure out structure
if isinstance(pre, dict):
    print("pre-dump top type dict, keys sample:", list(pre.keys())[:5])
    entry = None
    if LID in pre:
        entry = pre[LID]
    else:
        for k,v in pre.items():
            if isinstance(v, dict) and v.get("id")==LID:
                entry = v; break
elif isinstance(pre, list):
    entry = None
    for v in pre:
        if v.get("id")==LID or (v.get("slug")=="vectors" and "geometry" in str(v.get("unit",""))):
            entry = v; break
    print("pre-dump is list, len", len(pre))
    # show sample entry keys
    if pre:
        print("sample entry keys:", list(pre[0].keys()))

print("entry found:", entry is not None)
if entry:
    pd = entry.get("practice_data", entry)
    for f in ["related_videos","topic_links","worked_examples"]:
        pv = pd.get(f, "MISSING")
        lv = live.get(f, "MISSING")
        same = json.dumps(pv, sort_keys=True, ensure_ascii=False)==json.dumps(lv, sort_keys=True, ensure_ascii=False)
        print(f"\n=== {f}: preserved={same}")
        if not same:
            print(" PRE:", json.dumps(pv, ensure_ascii=False)[:800])
            print(" LIVE:", json.dumps(lv, ensure_ascii=False)[:800])
    # Also list what fields existed pre vs live
    print("\npre keys:", sorted(pd.keys()))
    print("live keys:", sorted(live.keys()))
