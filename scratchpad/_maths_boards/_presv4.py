import json,difflib
ID="e40e80e4-666f-4cce-a8b3-5f7bb6b5c490"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
ppd=[e for e in pre if e["id"]==ID][0]["practice_data"]
live=json.load(open("_live_gl02.json",encoding="utf-8"))
out=[]
a=json.dumps(ppd.get("method_card"),indent=1,ensure_ascii=False).splitlines()
b=json.dumps(live.get("method_card"),indent=1,ensure_ascii=False).splitlines()
for l in difflib.unified_diff(a,b,lineterm="",n=0):
    if l.startswith(("+","-")) and not l.startswith(("+++","---")):
        out.append(l)
open("_mc_diff.txt","w",encoding="utf-8").write("\n".join(out) or "IDENTICAL")
print("lines:",len(out))
