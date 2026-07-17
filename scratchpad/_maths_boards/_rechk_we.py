import json
ID="7f378aaa-68dc-4420-b952-f56d8349b1ed"
dump=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
entry=[r for r in dump if r.get("id")==ID][0]
old=entry["practice_data"]["worked_examples"]
new=json.load(open("_rechk_live.json",encoding="utf-8"))["worked_examples"]
print("counts old/new:",len(old),len(new))
import difflib
os=json.dumps(old,ensure_ascii=False,indent=1).splitlines()
ns=json.dumps(new,ensure_ascii=False,indent=1).splitlines()
for line in difflib.unified_diff(os,ns,lineterm="",n=0):
    print(line)
