import json
ID="65e7a745-9820-431a-8b99-d96cd7514bf3"
pre=[e for e in json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8")) if e.get("id")==ID][0]["practice_data"]
for t,i in [("silver",6),("gold",2)]:
    p=pre["problem_bank"][t][i]
    print(f"\n=== ORIG {t}[{i}] ===")
    print("DISPLAY:",p.get("display"))
    print("SOL:",p.get("solutions"),"options:",p.get("options"))
