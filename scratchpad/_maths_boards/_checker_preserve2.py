import json
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
live = json.load(open("_live_L01.json", encoding="utf-8"))
SID = "32c2c2c1-056b-4d78-b025-7e1e6f7ab3f3"
entry=None
for e in pre:
    if isinstance(e,dict) and (e.get("id")==SID or e.get("lesson_id")==SID):
        entry=e; break
print("entry keys:", list(entry.keys()))
pd = entry.get("practice_data") or entry
if "practice_data" in entry:
    pd = entry["practice_data"]
print("pre practice_data keys:", list(pd.keys()) if isinstance(pd,dict) else type(pd))
for f in ["related_videos","topic_links","worked_examples"]:
    pv = pd.get(f) if isinstance(pd,dict) else None
    lv = live.get(f)
    print(f, "==" if pv==lv else "DIFF", "| pre:", json.dumps(pv)[:120] if pv is not None else None)
