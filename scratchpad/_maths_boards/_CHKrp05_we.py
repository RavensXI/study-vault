import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

live = json.load(open("_CHKrp05_live.json", encoding="utf-8"))[0]["practice_data"]
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
ID = "ddbb6863-36ab-4898-8090-16df440a9d85"
entry = None
for v in pre:
    if v.get("id") == ID or v.get("slug") == "proportion-equations-and-powers":
        entry = v; break
print("matched by:", "id" if entry.get("id")==ID else "slug", "| slug=", entry.get("slug"))
ppd = entry.get("practice_data", entry)

print("=== PRE worked_examples ===")
print(json.dumps(ppd["worked_examples"], indent=1, ensure_ascii=False))
print("\n=== LIVE worked_examples ===")
print(json.dumps(live["worked_examples"], indent=1, ensure_ascii=False))
