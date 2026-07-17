import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
pd = json.load(open("_L07ocr_live.json", encoding="utf-8"))
pb = pd["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    print("==============", tier)
    print("  desc:", pb.get(f"{tier}_description"))
    for i, p in enumerate(pb[tier]):
        print(f"--- [{i}] input={p.get('input_type')} calc={p.get('calculator')}")
        print("  display:", p.get("display"))
        if "options" in p:
            print("  options:", p.get("options"))
        print("  solutions:", p.get("solutions"))
        print("  hint:", p.get("hint"))
        for m in p.get("misconceptions", []):
            print("   misc:", {kk: m.get(kk) for kk in ("pattern", "expect", "message")})
        extra = [k for k in p if k not in ("input_type","calculator","display","options","solutions","hint","misconceptions")]
        if extra:
            print("  extrakeys:", extra)
print("\n\n###### method_card ######")
print(json.dumps(pd.get("method_card"), indent=1, ensure_ascii=False))
print("\n###### worked_examples ######")
print(json.dumps(pd.get("worked_examples"), indent=1, ensure_ascii=False))
print("\n###### topic_links ######")
print(json.dumps(pd.get("topic_links"), indent=1, ensure_ascii=False))
print("\n###### related_videos ######")
print(json.dumps(pd.get("related_videos"), indent=1, ensure_ascii=False))
print("\n###### top-level keys ######", list(pd.keys()))
