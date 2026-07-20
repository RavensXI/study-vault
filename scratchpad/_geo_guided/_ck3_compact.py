import json
d=json.load(open("_ck3_L03_live.json",encoding="utf-8"))
pb=d["problem_bank"]
o=[]
def p(*a): o.append(" ".join(str(x) for x in a))
for t in ("bronze","silver","gold"):
    p("### %s_description: %r"%(t,pb.get(t+"_description")))
    for i,pr in enumerate(pb[t]):
        p("\n===== %s[%d] ====="%(t,i))
        for k in ("display","input_type","solutions","options","hint","note","guided_skip_reason","unit","ruler","image"):
            if k in pr: p("  %s: %s"%(k,json.dumps(pr[k],ensure_ascii=False)))
        if "chart" in pr:
            c=pr["chart"]
            ds=c.get("data",{}).get("datasets",[])
            p("  CHART type=%s"%c.get("type"))
            for j,s in enumerate(ds):
                p("    ds%d label=%s data=%s"%(j,s.get("label"),json.dumps(s.get("data"),ensure_ascii=False)))
            p("    labels=%s"%json.dumps(c.get("data",{}).get("labels"),ensure_ascii=False))
            sc=c.get("options",{}).get("scales",{})
            p("    scales=%s"%json.dumps(sc,ensure_ascii=False))
        for m in pr.get("misconceptions",[]):
            p("  MISC: %s"%json.dumps(m,ensure_ascii=False))
        gs=pr.get("guided_steps")
        if gs is None: p("  !! NO guided_steps")
        else:
            for j,s in enumerate(gs):
                p("  gs[%d]: %s"%(j,json.dumps(s,ensure_ascii=False)))
        extra=[k for k in pr if k not in ("display","input_type","solutions","options","hint","note","chart","misconceptions","guided_steps","unit","image","ruler","guided_skip_reason")]
        if extra: p("  OTHER KEYS: %s -> %s"%(extra, json.dumps({k:pr[k] for k in extra},ensure_ascii=False)[:800]))
open("_ck3_bank.txt","w",encoding="utf-8").write("\n".join(o))
print("ok")
