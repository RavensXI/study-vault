import json
live=json.load(open("_live_L06.json",encoding="utf-8"))
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
ID="622f7959-f9e9-45aa-b2bd-8a5b6698e357"
ppd=[v for v in pre if v.get("id")==ID][0]["practice_data"]
pw=ppd["worked_examples"]; lw=live["worked_examples"]
out=[]
for i,(a,b) in enumerate(zip(pw,lw)):
    # normalise em dash to colon-ish and compare
    sa=json.dumps(a,ensure_ascii=True)
    sb=json.dumps(b,ensure_ascii=True)
    # replace em dash unicode escape in pre with ": " equivalent? just report char-level
    na=sa.replace("\u2014 ",": ").replace("\u2014",":")
    if na==sb:
        out.append(f"we[{i}]: ONLY em-dash->colon in labels (maths identical)")
    else:
        out.append(f"we[{i}]: OTHER DIFF")
        out.append("  PRE="+sa)
        out.append("  LIVE="+sb)
# em dash scan in ALL live student-facing strings
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            walk(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o: out.append(f"EM DASH at {path}: {o}")
walk(live)
open("_wediff_out.txt","w",encoding="utf-8").write("\n".join(out))
print("\n".join(out))
