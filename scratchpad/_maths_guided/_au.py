import json
au=json.load(open("../_maths_audit/_audit_result.json",encoding="utf-8"))
for grp in ["issues","unconfirmed"]:
    for it in au.get(grp,[]):
        k=json.dumps(it)
        if "ratio-proportion-L01" in k:
            print("===",grp,it.get("tier"),it.get("index"),it.get("type"))
            print(it.get("detail"))
            print()
