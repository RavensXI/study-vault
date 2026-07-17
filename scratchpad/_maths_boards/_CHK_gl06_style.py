import json,re
live=json.load(open("_CHK_graphsL06_LIVE.json",encoding="utf-8"))
emdash=[]
hintlatex=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o: emdash.append(path+" :: "+o[:80])
walk(live,"root")
# hints latex
def hints(o,path):
    if isinstance(o,dict):
        if "hint" in o and isinstance(o["hint"],str) and ("\(" in o["hint"] or "\)" in o["hint"] or "<" in o["hint"]):
            hintlatex.append(path+".hint :: "+o["hint"])
        for k,v in o.items(): hints(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): hints(v,f"{path}[{i}]")
hints(live,"root")
print("em dashes:", len(emdash))
for e in emdash: print("  ",e)
print("hints w/ latex/html:", len(hintlatex))
for e in hintlatex: print("  ",e)

# check misconception expects reproduce for the two 'sine_symmetry' & tricky ones
bank=live["problem_bank"]
# gold[1] cos0.5: sine_symmetry expect 120 => 180-60
# gold[2] tan1: sine_symmetry expect 135 => 180-45
# verify quickly
print("gold1 mis:", [ (m['pattern'],m['expect']) for m in bank['gold'][1]['misconceptions']])
print("gold2 mis:", [ (m['pattern'],m['expect']) for m in bank['gold'][2]['misconceptions']])
