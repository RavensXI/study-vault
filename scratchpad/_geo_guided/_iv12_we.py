import json,os,difflib,io
d=os.path.dirname(os.path.abspath(__file__))
live=json.load(open(os.path.join(d,"_iv12_live.json"),encoding="utf-8"))
pre=json.load(open(os.path.join(d,"_iv12_pre.json"),encoding="utf-8"))["pd"]
buf=io.StringIO()
a=json.dumps(pre.get("worked_examples"),ensure_ascii=False,indent=1).splitlines()
b=json.dumps(live.get("worked_examples"),ensure_ascii=False,indent=1).splitlines()
for l in difflib.unified_diff(a,b,lineterm="",n=0): print(l,file=buf)
a=json.dumps(pre.get("method_card"),ensure_ascii=False,indent=1).splitlines()
b=json.dumps(live.get("method_card"),ensure_ascii=False,indent=1).splitlines()
print("=== METHOD CARD DIFF ===",file=buf)
for l in difflib.unified_diff(a,b,lineterm="",n=0): print(l,file=buf)
open(os.path.join(d,"_iv12_we.txt"),"w",encoding="utf-8").write(buf.getvalue())
