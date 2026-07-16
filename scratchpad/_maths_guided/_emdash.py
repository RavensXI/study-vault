import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_live_geometry-L08.json",encoding="utf-8"))
found=[]
def walk(node,path):
    if isinstance(node,dict):
        for k,v in node.items():
            # skip internal note fields (exempt)
            if k=="note":
                continue
            walk(v,f"{path}.{k}")
    elif isinstance(node,list):
        for i,v in enumerate(node):
            walk(v,f"{path}[{i}]")
    elif isinstance(node,str):
        if "—" in node or "–" in node:
            found.append((path,node))
walk(live,"")
print("EM/EN DASHES in student-facing:",len(found))
for p,s in found: print(p,"::",s[:120])
