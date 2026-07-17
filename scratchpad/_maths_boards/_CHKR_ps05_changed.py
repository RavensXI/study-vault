import json, re
ID = "b063ea7d-cb1c-40ca-a28b-ea79c429361f"
live = json.load(open("_CHKR_ps05_live.json", encoding="utf-8"))
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
pdold = [r for r in pre if r["id"]==ID][0]["practice_data"]

def strip(s):
    return re.sub("<[^>]+>","",s)

changed = [("bronze",0),("bronze",7),("silver",5),("gold",3)]
for tier,i in changed:
    o = pdold["problem_bank"][tier][i]
    n = live["problem_bank"][tier][i]
    print("="*70)
    print(f"{tier}[{i}]")
    print("OLD display:", strip(o.get("display","")))
    print("OLD sol:", o.get("solutions"))
    print("NEW display:", strip(n.get("display","")))
    print("NEW sol:", n.get("solutions"))
    if "chart" in o:
        print("OLD chart data:", o["chart"]["data"]["datasets"][0]["data"], "labels", o["chart"]["data"]["labels"])
    if "chart" in n:
        print("NEW chart data:", n["chart"]["data"]["datasets"][0]["data"], "labels", n["chart"]["data"]["labels"])
