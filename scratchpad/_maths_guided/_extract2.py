import json, io
ID="6623fba3-fb9e-4353-80c4-35ed1d88f47e"
d=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
print("top type:", type(d).__name__)
matches=[]
def walk(o,path):
    if isinstance(o,dict):
        if o.get("id")==ID:
            matches.append((path,o))
        for k,v in o.items():
            walk(v,path+"/"+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v,f"{path}[{i}]")
walk(d,"")
print("num matches:", len(matches))
for p,o in matches:
    pd=o.get("practice_data",{})
    goldsol = pd.get("problem_bank",{}).get("gold",[{}])
    print("path:",p,"| pd keys:", list(pd.keys()) if isinstance(pd,dict) else None)
    print("   title:", o.get("title"), "lesson_number:", o.get("lesson_number"))
