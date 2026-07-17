import json,sys
sys.stdout.reconfigure(encoding="utf-8")
pd=json.load(open("_ps03e_live.json",encoding="utf-8"))["practice_data"]
pb=pd["problem_bank"]
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        if "chart" in p or "options" in p:
            print("="*60)
            print(f"[{t}][{i}] {p.get('input_type')}: {p.get('display')[:70]}")
            if "options" in p: print("  OPTIONS:",p["options"], " sol idx:",p.get("solutions"))
            if "chart" in p:
                print("  CHART:",json.dumps(p["chart"],ensure_ascii=False))
print("\n\n###### METHOD CARD ######")
print(json.dumps(pd.get("method_card"),ensure_ascii=False,indent=1))
print("\n###### WORKED EXAMPLES ######")
print(json.dumps(pd.get("worked_examples"),ensure_ascii=False,indent=1))
print("\n###### TOPIC LINKS ######")
print(json.dumps(pd.get("topic_links"),ensure_ascii=False))
print("\n###### RELATED VIDEOS ######")
print(json.dumps(pd.get("related_videos"),ensure_ascii=False))
