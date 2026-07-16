import json

ID = "4d1ac99e-f293-4cce-a4d3-c276c5f8f24b"
live = json.load(open("_CHK_algL08_live.json", encoding="utf-8"))
pre = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
entry = None
if isinstance(pre, dict):
    entry = pre.get(ID)
    if entry is None:
        for k, v in pre.items():
            if isinstance(v, dict) and v.get("id") == ID:
                entry = v; break
elif isinstance(pre, list):
    for v in pre:
        if isinstance(v, dict) and v.get("id") == ID:
            entry = v; break
pd = entry.get("practice_data", entry)
out = []
out.append("PRE worked_examples:")
out.append(json.dumps(pd.get("worked_examples"), ensure_ascii=False, indent=2))
out.append("\n\nLIVE worked_examples:")
out.append(json.dumps(live.get("worked_examples"), ensure_ascii=False, indent=2))
open("_CHK_algL08_we_diff.txt","w",encoding="utf-8").write("\n".join(out))
print("PRE we count:", len(pd.get("worked_examples") or []))
print("LIVE we count:", len(live.get("worked_examples") or []))
print("PRE keys:", list(pd.keys()))
