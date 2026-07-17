import json,re,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_LIVE_eduqas_probstat_L02.json",encoding="utf-8"))

def regions(svg):
    # map x-position -> text content
    d={}
    for m in re.finditer(r'<text x="(\d+)"[^>]*>([^<]*)</text>',svg):
        x=int(m.group(1)); t=m.group(2).strip()
        d.setdefault(x,[]).append(t)
    tot=None
    mt=re.search(r'Total:\s*([0-9?]+)',svg)
    if mt: tot=mt.group(1)
    return d,tot

def num(s):
    try: return float(s)
    except: return None

problems=[]
for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        problems.append((f"{tier}[{i}]",p.get("display","")))
# teach + opener
for t in ["gold","bronze","silver"]:
    problems.append((f"teach.{t}", live["guided"]["teach"][t].get("display","")))
for i,s in enumerate(live["guided"]["opener"]["steps"]):
    if s.get("display"): problems.append((f"opener[{i}]", s["display"]))

for name,disp in problems:
    if "<svg" not in disp: 
        continue
    d,tot=regions(disp)
    # region labels at x=76 (left-only),130(both),184(right-only),236(neither)
    left=d.get(76,[""])[0]; both=d.get(130,[""])[0]; right=d.get(184,[""])[0]; neither=d.get(236,[""])[0]
    print(f"{name}: left={left!r} both={both!r} right={right!r} neither={neither!r} total={tot!r}")
