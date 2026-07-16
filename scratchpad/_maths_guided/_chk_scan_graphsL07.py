import json, io, re
pd=json.load(io.open("_CHK_graphsL07_live.json",encoding="utf-8"))

# 1. em dash scan (student-facing). Exclude internal 'note'
emdash=[]
def walk(o,path,innote=False):
    if isinstance(o,dict):
        for k,v in o.items():
            walk(v,path+"."+k, innote or k=="note")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v,path+f"[{i}]",innote)
    elif isinstance(o,str):
        if not innote and "—" in o:
            emdash.append(path)
walk(pd,"")
print("EM DASHES:", emdash)

# 2. check hints have no LaTeX
latexhints=[]
def walk2(o,path):
    if isinstance(o,dict):
        h=o.get("hint")
        if isinstance(h,str) and ("\(" in h or "$" in h):
            latexhints.append(path)
        for k,v in o.items(): walk2(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk2(v,path+f"[{i}]")
walk2(pd,"")
print("LATEX IN HINTS:", latexhints)

# 3. numeric answers only
nonnum=[]
def walk3(o,path):
    if isinstance(o,dict):
        if "answer" in o and not isinstance(o["answer"],(int,float)):
            nonnum.append((path,o["answer"]))
        for k,v in o.items(): walk3(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk3(v,path+f"[{i}]")
walk3(pd,"")
print("NON-NUMERIC ANSWERS:", nonnum)

# tier guide word counts
for t in ["bronze","silver","gold"]:
    steps=pd["tier_guides"][t]["steps"]
    wc=sum(len(re.sub(r"<[^>]+>","",s).split()) for s in steps)
    print(f"tier_guide {t} steps wordcount:", wc)
