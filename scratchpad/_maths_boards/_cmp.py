import json
ID="5c10e089-e2cc-4a61-b6b3-951a8994a1a0"
pre=[r for r in json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8")) if r.get("id")==ID][0]
prepd=pre["practice_data"] if "practice_data" in pre else pre
live=json.load(open("_live_geoL02.json",encoding="utf-8"))
import re
def strip_svg(s):
    return re.sub(r"<svg.*?</svg>","",s or "",flags=re.S).replace('<span class="figure-caption">Diagram not drawn accurately</span>','').strip()
for t in ("bronze","silver","gold"):
    pa=prepd["problem_bank"][t]; la=live["problem_bank"][t]
    for i,(p,l) in enumerate(zip(pa,la)):
        ps=p.get("solutions"); ls=l.get("solutions")
        if ps!=ls:
            print(f"SOL DIFF {t}[{i}] pre={ps} live={ls}")
        pt=strip_svg(p.get("display")); lt=strip_svg(l.get("display"))
        if pt!=lt:
            print(f"TEXT DIFF {t}[{i}]:\n  PRE: {pt}\n  LIVE:{lt}")
        if p.get("calculator")!=l.get("calculator"):
            print(f"CALC DIFF {t}[{i}] pre={p.get('calculator')} live={l.get('calculator')}")
# worked examples compare
we_p=json.dumps(prepd.get("worked_examples"),sort_keys=True)
we_l=json.dumps(live.get("worked_examples"),sort_keys=True)
print("worked_examples identical:", we_p==we_l)
mc_p=json.dumps(prepd.get("method_card"),sort_keys=True)
mc_l=json.dumps(live.get("method_card"),sort_keys=True)
print("method_card identical:", mc_p==mc_l)
