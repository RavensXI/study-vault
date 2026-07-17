import json,re
live=json.load(open("_CHKR_ps03_live.json",encoding="utf-8"))["practice_data"]
svgs=[]
def collect(o):
    if isinstance(o,dict):
        for v in o.values(): collect(v)
    elif isinstance(o,list):
        for v in o: collect(v)
    elif isinstance(o,str) and "<svg" in o:
        svgs.append(o)
collect(live)
print("svg count:",len(svgs))
tf=set()
for s in svgs:
    tf|=set(re.findall(r'<text[^>]*\bfill="([^"]+)"',s))
print("text fills used:",tf)
allpaths=[]
for s in svgs:
    allpaths+=re.findall(r'<path[^>]*\bfill="(#[0-9a-fA-F]+)"[^>]*>',s)
print("path color fills:",set(allpaths))
missing=[]
for s in svgs:
    for m in re.finditer(r'<path[^>]*\bfill="#[0-9a-fA-F]+"[^>]*>',s):
        if "fill-opacity" not in m.group(0): missing.append(m.group(0)[:60])
print("paths w/o opacity:",missing)
