import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_CHK_LIVE_fresh.json",encoding="utf-8"))["practice_data"]["worked_examples"]
pre=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
ID="39bdcd12-eb3d-45b1-b0c5-d8e2257610df"
entry=[e for e in pre if e.get("id")==ID][0]
pwe=entry["practice_data"]["worked_examples"]
for i,(a,b) in enumerate(zip(pwe,live)):
    for j,(sa,sb) in enumerate(zip(a["steps"],b["steps"])):
        if sa.get("content")!=sb.get("content"):
            print(f"we[{i}].steps[{j}].content DIFF:\n  PRE={sa.get('content')}\n  LIVE={sb.get('content')}")
    if a.get("question")!=b.get("question"):
        print(f"we[{i}].question: PRE={a.get('question')} LIVE={b.get('question')}")
# emdash scan
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            walk(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,path+f"[{i}]")
    elif isinstance(o,str):
        if "—" in o: print("EM DASH at",path,":",o[:80])
walk(json.load(open("_CHK_LIVE_fresh.json",encoding="utf-8"))["practice_data"])
print("scan done")
