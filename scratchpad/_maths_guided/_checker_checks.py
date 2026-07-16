import json, io
pd=json.load(io.open("_checker_live.json",encoding="utf-8"))

# 1. em dash scan in student-facing strings (exclude internal 'note' keys)
emdash="—"
hits=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if emdash in o:
            hits.append((path,o))
walk(pd,"")
print("EM DASH HITS:",len(hits))
for h in hits: print("  ",h)

# 2. numeric-only boxes: every guided_steps/teach/opener box 'answer' is int/float
badnum=[]
def check_answer(o,path):
    if isinstance(o,dict):
        if "answer" in o and not isinstance(o["answer"],(int,float)):
            badnum.append((path,o["answer"]))
        for k,v in o.items(): check_answer(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): check_answer(v,f"{path}[{i}]")
check_answer(pd,"")
print("NON-NUMERIC answers:",badnum)

# 3. hint plain text (no LaTeX backslash-paren) in problem hints and box hints
latexhint=[]
def check_hint(o,path):
    if isinstance(o,dict):
        if "hint" in o and isinstance(o["hint"],str) and ("\(" in o["hint"] or "<" in o["hint"]):
            latexhint.append((path,o["hint"]))
        for k,v in o.items(): check_hint(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): check_hint(v,f"{path}[{i}]")
check_hint(pd,"")
print("HINT with latex/html:",latexhint)
