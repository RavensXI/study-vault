import json, sys
sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open("_L09ocr_live.json", encoding="utf-8"))
print("== method_card =="); print(json.dumps(d.get("method_card"), indent=1, ensure_ascii=False))
print("== topic_links =="); print(json.dumps(d.get("topic_links"), indent=1, ensure_ascii=False))
print("== related_videos =="); print(json.dumps(d.get("related_videos"), indent=1, ensure_ascii=False))
we = d.get("worked_examples", [])
print("== worked_examples count:", len(we))
for e in we:
    print("  -", e.get("difficulty"), "|", e.get("question"))
print("== gold[4] full =="); print(json.dumps(d["problem_bank"]["gold"][4], indent=1, ensure_ascii=False))
