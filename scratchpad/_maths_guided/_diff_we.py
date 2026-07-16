import json
live = json.load(open("_checker_live_L06.json",encoding="utf-8"))
dump = json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
entry=[e for e in dump if e.get("id")=="f6f5708d-edf9-42e6-81d8-49c3cf282310"][0]
old = entry.get("practice_data", entry).get("worked_examples")
new = live.get("worked_examples")
for i,(o,n) in enumerate(zip(old,new)):
    so=json.dumps(o,sort_keys=True,ensure_ascii=False)
    sn=json.dumps(n,sort_keys=True,ensure_ascii=False)
    if so!=sn:
        out=open(f"_we_diff_{i}.txt","w",encoding="utf-8")
        out.write("OLD:\n"+json.dumps(o,indent=1,ensure_ascii=False)+"\n\nNEW:\n"+json.dumps(n,indent=1,ensure_ascii=False))
        out.close()
        print(f"WE[{i}] DIFFERS -> _we_diff_{i}.txt")
    else:
        print(f"WE[{i}] same")
