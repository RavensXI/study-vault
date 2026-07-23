# -*- coding: utf-8 -*-
"""Turn an apply-workflow journal into an _apply_edits file.
    python _parse_apply_journal.py <journal.jsonl> <out.json>
"""
import json,io,os,re,sys,collections
os.environ["PYTHONUTF8"]="1"
try: sys.stdout.reconfigure(encoding="utf-8",errors="replace")
except: pass
jp,out=sys.argv[1],sys.argv[2]
edits=[]
for line in io.open(jp,encoding="utf-8"):
    line=line.strip()
    if not line: continue
    try: rec=json.loads(line)
    except: continue
    if rec.get("type")!="result": continue
    r=rec.get("result")
    if isinstance(r,str):
        try: r=json.loads(r)
        except: continue
    if not isinstance(r,dict): continue
    pack=r.get("pack","") or ""
    m=re.match(r"([a-z\-]+)__L(\d+)",pack)
    if not m: continue
    unit,ln=m.group(1),int(m.group(2))
    for e in (r.get("edits") or []):
        mp=re.match(r"(bronze|silver|gold)\s*\[?(\d+)\]?",e.get("problem",""))
        if not mp: continue
        edits.append({"board":e["board"],"unit":unit,"lesson":ln,"tier":mp.group(1),
                      "index":int(mp.group(2)),"step":e["step"],"field":e["field"],"new_text":e["new_text"]})
io.open(out,"w",encoding="utf-8").write(json.dumps(edits,indent=1,ensure_ascii=False))
print("parsed %d edits -> %s"%(len(edits),out))
print("by board:",dict(collections.Counter(e["board"] for e in edits)))
