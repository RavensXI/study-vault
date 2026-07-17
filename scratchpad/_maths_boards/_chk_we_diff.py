import json

ID = "5f629e65-9b8c-4fcb-a334-93ee7e25d4ff"
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
entry = None
items = pre.items() if isinstance(pre, dict) else enumerate(pre)
for k, v in items:
    if isinstance(v, dict) and v.get("id") == ID:
        entry = v; break
pd = entry["practice_data"]
live = json.load(open("_chk_numL03_live.json", encoding="utf-8"))

out = []
out.append("=== PRE worked_examples ===")
out.append(json.dumps(pd.get("worked_examples"), indent=1, ensure_ascii=False))
out.append("=== LIVE worked_examples ===")
out.append(json.dumps(live.get("worked_examples"), indent=1, ensure_ascii=False))
open("_chk_we_diff.txt","w",encoding="utf-8").write("\n".join(out))
print("wrote")
# also list top-level keys pre vs live
print("PRE keys:", sorted(pd.keys()))
print("LIVE keys:", sorted(live.keys()))
