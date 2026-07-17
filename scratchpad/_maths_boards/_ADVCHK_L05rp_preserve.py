import json
ID="93469b0d-2704-499c-a20b-587a84c2e214"
live = json.load(open("_ADVCHK_L05rp_live.json", encoding="utf-8"))["practice_data"]

pre_raw = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))
# find entry
if isinstance(pre_raw, list):
    entry = next((r for r in pre_raw if r.get("id")==ID), None)
elif isinstance(pre_raw, dict):
    entry = pre_raw.get(ID) or next((v for k,v in pre_raw.items() if (isinstance(v,dict) and v.get("id")==ID)), None)
    if entry is None and "practice_data" in pre_raw:
        entry = pre_raw
print("pre entry found:", entry is not None, "| type pre_raw:", type(pre_raw).__name__)
if isinstance(pre_raw, dict):
    print("pre_raw top keys sample:", list(pre_raw.keys())[:5])
if entry is None:
    raise SystemExit("no pre entry")
pre = entry["practice_data"] if "practice_data" in entry else entry

for f in ["related_videos","topic_links","worked_examples","method_card"]:
    a=json.dumps(pre.get(f), sort_keys=True, ensure_ascii=False)
    b=json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
    print(f"\n=== {f}: {'UNCHANGED' if a==b else 'CHANGED'} (pre_present={f in pre})")
    if a!=b:
        print("PRE :", a[:600])
        print("LIVE:", b[:600])
print("\nPre practice_data keys:", list(pre.keys()))
print("Live practice_data keys:", list(live.keys()))
