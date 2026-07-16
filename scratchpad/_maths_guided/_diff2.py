import json
live=json.load(open("_live_ratio_L01.json",encoding="utf-8"))
ship=json.load(open("lesson_ratio-proportion-L01.json",encoding="utf-8"))
print("live==shipped file:", json.dumps(live,sort_keys=True,ensure_ascii=False)==json.dumps(ship,sort_keys=True,ensure_ascii=False))
# audit issues
try:
    au=json.load(open("../_maths_audit/_audit_result.json",encoding="utf-8"))
    for grp in ["issues","unconfirmed"]:
        for it in au.get(grp,[]):
            k=json.dumps(it)
            if "ratio-proportion-L01" in k or "bc1ac13e" in k:
                print(grp,":",json.dumps(it,ensure_ascii=False)[:300])
except Exception as e:
    print("audit read err",e)
