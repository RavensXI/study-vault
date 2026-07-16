import json,sys,io,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_CHK_L04_live.json",encoding="utf-8"))["practice_data"]
g=pd.get("guided",{})
print("guided keys:",list(g.keys()))
op=g.get("opener",{})
print("\n=== OPENER ===")
print(json.dumps(op,ensure_ascii=False,indent=1))
# scan any figure-claim words in opener/teach
def scan(obj,path):
    hits=[]
    if isinstance(obj,dict):
        for k,v in obj.items(): hits+=scan(v,path+"."+k)
    elif isinstance(obj,list):
        for i,v in enumerate(obj): hits+=scan(v,f"{path}[{i}]")
    elif isinstance(obj,str):
        for w in ["diagram","triangle","chart","table","shown below","here is","look at","the graph","picture","this figure","below"]:
            if w in obj.lower():
                hits.append((path,w,obj[:120]))
    return hits
print("\n=== FIGURE-CLAIM SCAN (guided) ===")
for h in scan(g,"guided"):
    has_svg = "<svg" in str(h)
    print(h)
