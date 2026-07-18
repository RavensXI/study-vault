import json, re
pd = json.load(open("_live_canon_L08.json", encoding="utf-8"))
issues = []
board_terms = ["AQA","Edexcel","OCR","Eduqas","WJEC"]
emdash=[]; board=[]; sheet=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o: emdash.append((path,o))
        for b in board_terms:
            if re.search(r'\b'+b+r'\b',o): board.append((path,b))
        if re.search(r'equation sheet|memorise|must remember',o,re.I): sheet.append((path,o))
walk(pd,"root")
print("EM DASHES:",emdash)
print("BOARD NAMES:",board)
print("SHEET/MEMORISE CLAIMS:")
for p,s in sheet: print("  ",p,"::",s[:90])
print("\nEXPECT vs ACCEPT:")
for tier in ("bronze","silver","gold"):
    for idx,prob in enumerate(pd["problem_bank"][tier]):
        sols=prob.get("solutions"); acc=prob.get("accept"); it=prob.get("input_type")
        for mi,m in enumerate(prob.get("misconceptions",[])):
            exp=m.get("expect")
            if exp is None: 
                print(f"{tier}[{idx}].mc[{mi}] expect=null (never fires)"); continue
            if it=="standard_form":
                dead=(exp==sols); status="DEAD" if dead else "ok"
            else:
                if acc is None:
                    dead=abs(exp-sols[0])<1e-9; status="DEAD(no acc,==sol)" if dead else "ok(no acc)"
                else:
                    dead=abs(exp-sols[0])<=acc; status="DEAD(in window)" if dead else "ok"
            if "DEAD" in status: issues.append(f"{tier}[{idx}].mc[{mi}] {status}")
            print(f"{tier}[{idx}].mc[{mi}] expect={exp} sol={sols} acc={acc} -> {status}")
print("\nISSUES:", issues if issues else "none")
