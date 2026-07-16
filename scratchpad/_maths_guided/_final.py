import json,io,sys,math
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_L06_fresh.json",encoding="utf-8"))
# independent solver for each problem by description
def sols_in_range(f,target,lo=0,hi=360,tol=1e-6):
    out=[]
    for d in range(lo,hi+1):
        if abs(f(math.radians(d))-target)<1e-9: out.append(d)
    return out
checks={
 ("gold",0):("cos=0.5 larger", max(sols_in_range(math.cos,0.5))),
 ("gold",1):("sin=-√2/2 smaller", min(sols_in_range(math.sin,-math.sqrt(2)/2))),
 ("gold",3):("tan=1 sum", sum([45,225])),
 ("gold",4):("2sinx-1=0 count", len(sols_in_range(math.sin,0.5))),
 ("bronze",0):("cos0", round(math.cos(0))),
 ("bronze",1):("tan period",180),
 ("bronze",2):("sin270", round(math.sin(math.radians(270)))),
 ("bronze",4):("sin min angle",270),
 ("bronze",5):("tan0",0),
 ("bronze",6):("tan asymptote",90),
 ("bronze",7):("tan=1 first",45),
 ("silver",0):("sin=1 smallest", min(sols_in_range(math.sin,1))),
 ("silver",1):("cos=0 larger", max(sols_in_range(math.cos,0))),
 ("silver",2):("sin=0.5 other",150),
 ("silver",3):("sin=0 count", len(sols_in_range(math.sin,0))),
 ("silver",4):("max 4sinx",4),
 ("silver",5):("tan cycles",360//180),
 ("silver",6):("cos=-1", sols_in_range(math.cos,-1)[0]),
}
bad=0
for (t,i),(desc,val) in checks.items():
    stored=pd["problem_bank"][t][i]["solutions"][0]
    ok = (val==stored)
    if not ok: bad+=1
    print(("OK " if ok else "XX ")+f"{t}[{i}] {desc}: computed={val} stored={stored}")
# MC
print("gold[2] MC sol idx",pd["problem_bank"]["gold"][2]["solutions"],"opt1=",pd["problem_bank"]["gold"][2]["options"][1])
print("bronze[3] MC sol idx",pd["problem_bank"]["bronze"][3]["solutions"],"opt3=",pd["problem_bank"]["bronze"][3]["options"][3])
print("TOTAL MATHS ERRORS:",bad)
