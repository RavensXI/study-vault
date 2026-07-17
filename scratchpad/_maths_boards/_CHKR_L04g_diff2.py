import json,difflib
ID="fb13c12c-f5c1-4832-871b-40440d729361"
live=json.load(open("_CHKR_L04g_live.json",encoding="utf-8"))["practice_data"]
dump=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
row=[r for r in dump if r.get("id")==ID][0]
pre=row["practice_data"]
for f in ["method_card","worked_examples"]:
    a=json.dumps(pre.get(f),ensure_ascii=False,indent=0).split("\n")
    b=json.dumps(live.get(f),ensure_ascii=False,indent=0).split("\n")
    print("="*20,f)
    for line in difflib.unified_diff(a,b,lineterm=""):
        if line.startswith(("+","-")) and not line.startswith(("+++","---")):
            print(repr(line))
