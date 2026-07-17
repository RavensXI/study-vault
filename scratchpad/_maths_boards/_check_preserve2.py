import json
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
live=json.load(open("_live_ratio-L04.json",encoding="utf-8"))
lid="f4a69507-b194-4751-ae27-c657ddd23113"
def find(pre):
    for r in pre:
        if r.get("id")==lid: return r
row=find(pre)
pd=row.get("practice_data")
a=pd.get("worked_examples"); b=live.get("worked_examples")
out=[]
out.append("PRE worked_examples:\n"+json.dumps(a,ensure_ascii=False,indent=1))
out.append("\nLIVE worked_examples:\n"+json.dumps(b,ensure_ascii=False,indent=1))
open("_we_diff.txt","w",encoding="utf-8").write("\n".join(out))
print("written; pre count", len(a), "live count", len(b))
# also list which top-level keys existed pre vs live
print("PRE keys:", sorted(pd.keys()))
print("LIVE keys:", sorted(live.keys()))
