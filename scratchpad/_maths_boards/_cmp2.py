import json,re
ID="5c10e089-e2cc-4a61-b6b3-951a8994a1a0"
pre=[r for r in json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8")) if r.get("id")==ID][0]
prepd=pre["practice_data"] if "practice_data" in pre else pre
live=json.load(open("_live_geoL02.json",encoding="utf-8"))
out=[]
def strip_svg(s):
    return re.sub(r"<svg.*?</svg>","",s or "",flags=re.S).replace('<span class="figure-caption">Diagram not drawn accurately</span>','').strip()
for t in ("bronze","silver","gold"):
    pa=prepd["problem_bank"][t]; la=live["problem_bank"][t]
    for i,(p,l) in enumerate(zip(pa,la)):
        pt=strip_svg(p.get("display")); lt=strip_svg(l.get("display"))
        # normalize latex cm^2 vs unicode
        norm=lambda x:x.replace("\(^2\)","²").replace("cm\(^2\)","cm²")
        if norm(pt)!=norm(lt):
            out.append(f"TEXTDIFF {t}[{i}] PRE=[{pt}] LIVE=[{lt}]")
out.append("worked_examples identical: %s"%(json.dumps(prepd.get("worked_examples"),sort_keys=True)==json.dumps(live.get("worked_examples"),sort_keys=True)))
out.append("method_card identical: %s"%(json.dumps(prepd.get("method_card"),sort_keys=True)==json.dumps(live.get("method_card"),sort_keys=True)))
open("_cmp_out.txt","w",encoding="utf-8").write("\n".join(out))
print("done",len(out))
