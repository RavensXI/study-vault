import json
live=json.load(open("_live_ratio-proportion-L01.json",encoding="utf-8"))
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
ID="9a6f1e85-41b4-4b82-87c6-e919e48362a9"
entry=[r for r in pre if r.get("id")==ID][0]
ppd=entry["practice_data"]
print("=== PRE worked_examples ===")
print(json.dumps(ppd["worked_examples"],indent=1,ensure_ascii=False))
print("=== LIVE worked_examples ===")
print(json.dumps(live["worked_examples"],indent=1,ensure_ascii=False))
# Also check problem_bank displays/solutions preserved vs pre (numbers shouldn't drift unless fixed)
print("\n=== problem_bank solutions PRE vs LIVE ===")
for tier in ["bronze","silver","gold"]:
    pb_pre=ppd["problem_bank"][tier]; pb_live=live["problem_bank"][tier]
    print(tier, "counts", len(pb_pre), len(pb_live))
    for i,(a,b) in enumerate(zip(pb_pre,pb_live)):
        if a.get("display")!=b.get("display") or a.get("solutions")!=b.get("solutions"):
            print(f"  [{i}] DISPLAY/SOL CHANGED")
            print("    PRE :", a.get("display"), a.get("solutions"))
            print("    LIVE:", b.get("display"), b.get("solutions"))
