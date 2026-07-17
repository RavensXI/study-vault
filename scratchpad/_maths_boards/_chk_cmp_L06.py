import json
pre=json.load(open("_pre_worked_examples.json", encoding="utf-8"))
live=json.load(open("_live_number-L06.json", encoding="utf-8"))["worked_examples"]
print("pre n=",len(pre),"live n=",len(live))
for i,(p,l) in enumerate(zip(pre,live)):
    print("=== WE",i,"===")
    print(" q pre :", repr(p.get("question")))
    print(" q live:", repr(l.get("question")))
    print(" diff labels:")
    for ps,ls in zip(p["steps"],l["steps"]):
        if ps.get("label")!=ls.get("label") or ps.get("content")!=ls.get("content"):
            print("   PRE :", repr(ps.get("label")), repr(ps.get("content")))
            print("   LIVE:", repr(ls.get("label")), repr(ls.get("content")))
