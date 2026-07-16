import json

ID = "2603a7c5-7660-4a4c-943d-78f2a112009e"
dump = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
entry = None
for row in dump:
    if row.get("id") == ID:
        entry = row; break
pre = entry["practice_data"]
live = json.load(open("_chk_L01_live.json", encoding="utf-8"))

out = []
out.append("PRE worked_examples:")
out.append(json.dumps(pre.get("worked_examples"), ensure_ascii=False, indent=1))
out.append("\n\nLIVE worked_examples:")
out.append(json.dumps(live.get("worked_examples"), ensure_ascii=False, indent=1))
open("_chk_we_out.txt","w",encoding="utf-8").write("\n".join(out))
print("written")
