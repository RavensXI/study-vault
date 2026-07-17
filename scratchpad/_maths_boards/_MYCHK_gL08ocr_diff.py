# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_MYCHK_gL08ocr_live.json", encoding="utf-8"))
pre = json.load(io.open("_MYCHK_gL08ocr_pre.json", encoding="utf-8"))

print("=== WORKED_EXAMPLES pre ===")
print(json.dumps(pre.get("worked_examples"), indent=1, ensure_ascii=False))
print("=== WORKED_EXAMPLES live ===")
print(json.dumps(pd.get("worked_examples"), indent=1, ensure_ascii=False))

print("\n=== DISPLAY diffs for solution-changed problems ===")
for tier,i in [("gold",0),("gold",4),("bronze",2),("bronze",5),("bronze",6),("silver",0),("silver",3),("silver",5)]:
    a = pre["problem_bank"][tier][i]
    b = pd["problem_bank"][tier][i]
    da = a.get("display","")
    db = b.get("display","")
    same = "SAME" if da==db else "DIFFERENT"
    print(f"\n--- {tier}[{i}] display {same}  sol {a.get('solutions')} -> {b.get('solutions')}")
    if da!=db:
        print("  PRE :", da[:200])
        print("  LIVE:", db[:200])
    else:
        print("  disp:", db[:160])
