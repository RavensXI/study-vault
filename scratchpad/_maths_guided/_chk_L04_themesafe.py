import json,sys,io,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_CHK_L04_live.json",encoding="utf-8"))["practice_data"]
def allsvgs(obj):
    out=[]
    if isinstance(obj,dict):
        for v in obj.values(): out+=allsvgs(v)
    elif isinstance(obj,list):
        for v in obj: out+=allsvgs(v)
    elif isinstance(obj,str):
        out+=re.findall(r'<svg.*?</svg>',obj,flags=re.S)
    return out
svgs=allsvgs(pd)
print("total svgs:",len(svgs))
for i,s in enumerate(svgs):
    bad=[]
    if "http" in s: bad.append("external-url")
    if "<script" in s: bad.append("script")
    if "href" in s: bad.append("href")
    if "xlink" in s: bad.append("xlink")
    # hardcoded dark text fill?
    for tm in re.finditer(r'<text[^>]*fill="([^"]+)"',s):
        if tm.group(1)!="currentColor": bad.append("textfill:"+tm.group(1))
    # group fill
    root_role = 'role="img"' in s
    aria = 'aria-label' in s
    vb = 'viewBox' in s
    print(f"svg[{i}] role={root_role} aria={aria} viewBox={vb} issues={bad or 'none'} len={len(s)}")
