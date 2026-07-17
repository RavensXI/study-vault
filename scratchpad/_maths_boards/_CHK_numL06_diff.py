import json
ID = "d15fddc3-0766-4882-bfc8-15a0b7208d89"
live = json.load(open("_CHK_numL06_live.json", encoding="utf-8"))["practice_data"]
pre = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))
entry = next(v for v in pre if v.get("id")==ID)
old = entry["practice_data"]["problem_bank"]
new = live["problem_bank"]
for t in ["bronze","silver","gold"]:
    print(f"\n=== {t} ===  old={len(old[t])} new={len(new[t])}")
    for i in range(max(len(old[t]),len(new[t]))):
        od = old[t][i] if i<len(old[t]) else {}
        nd = new[t][i] if i<len(new[t]) else {}
        odisp, ndisp = od.get("display"), nd.get("display")
        osol, nsol = od.get("solutions"), nd.get("solutions")
        flag=""
        if odisp!=ndisp: flag+=" DISPLAY-CHANGED"
        if osol!=nsol: flag+=" SOL-CHANGED"
        print(f"[{i}] sol {osol} -> {nsol}{flag}")
        if odisp!=ndisp:
            print("     OLD:", odisp)
            print("     NEW:", ndisp)
