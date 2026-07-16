import json
live=json.load(open("_live_graphs_l04.json",encoding="utf-8"))
s=json.dumps(live,ensure_ascii=False)
print("em dash (—) count:", s.count("—"))
print("en dash (–) count:", s.count("–"))
# find contexts of en dashes
import re
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o: print("EM",path,repr(o[:80]))
        if "–" in o: print("EN",path,repr(o[:90]))
walk(live)
