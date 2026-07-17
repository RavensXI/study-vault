import json
ID="fe589e29-485c-4272-94df-41687f398c1b"
live=json.load(open("_CHK_L02_livefresh.json",encoding="utf-8"))["practice_data"]
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
entry=[x for x in pre if x.get("id")==ID][0]
pp=entry.get("practice_data",entry)
out=[]
out.append("PRE worked_examples:")
out.append(json.dumps(pp.get("worked_examples"),ensure_ascii=False,indent=1))
out.append("\nLIVE worked_examples:")
out.append(json.dumps(live.get("worked_examples"),ensure_ascii=False,indent=1))
open("_we_diff_L02.txt","w",encoding="utf-8").write("\n".join(out))
# also list all top-level keys pre vs live and which changed
prekeys=set(pp.keys()); livekeys=set(live.keys())
print("keys only in PRE:",prekeys-livekeys)
print("keys only in LIVE:",livekeys-prekeys)
for k in sorted(prekeys&livekeys):
    same=json.dumps(pp[k],sort_keys=True,ensure_ascii=False)==json.dumps(live[k],sort_keys=True,ensure_ascii=False)
    print(f"  {k}: {'same' if same else 'CHANGED'}")
