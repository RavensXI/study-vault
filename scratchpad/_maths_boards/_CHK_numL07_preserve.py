import json
ID="8696e75e-f9fd-40ef-b3a4-df27f5811c73"
pre=json.load(open("_pre_dump_maths-aqa.json",encoding="utf-8"))
# pre may be list of rows
rows = pre if isinstance(pre, list) else pre.get("data", pre)
entry=None
for r in rows:
    if isinstance(r,dict) and r.get("id")==ID:
        entry=r; break
print("found pre entry:", entry is not None)
live=json.load(open("_CHK_numL07_live.json",encoding="utf-8"))["practice_data"]
pd=entry["practice_data"] if entry else {}
for f in ["related_videos","topic_links","worked_examples"]:
    same = json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f, "PRESERVED" if same else "CHANGED")
    if not same:
        print("  PRE :", json.dumps(pd.get(f),ensure_ascii=False)[:500])
        print("  LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:500])
print("pre top keys:", list(pd.keys()))
