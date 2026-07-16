import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pre = json.load(open("_pre_L12.json",encoding="utf-8"))
live = json.load(open("_live_L12.json",encoding="utf-8"))
pw=pre["worked_examples"]; lw=live["worked_examples"]
print("pre count",len(pw),"live count",len(lw))
for i in range(max(len(pw),len(lw))):
    a=pw[i] if i<len(pw) else None
    b=lw[i] if i<len(lw) else None
    same=json.dumps(a,sort_keys=True,ensure_ascii=False)==json.dumps(b,sort_keys=True,ensure_ascii=False)
    print(i, "SAME" if same else "DIFF", "| pre q:",a and a.get("question"),"| live q:",b and b.get("question"))
