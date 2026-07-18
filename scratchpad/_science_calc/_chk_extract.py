import json, re, io
d=json.load(open("_live_canon.json",encoding="utf-8"))
def strip(s):
    if not isinstance(s,str): return s
    s=re.sub(r'<svg.*?</svg>','[SVG]',s,flags=re.S)
    s=re.sub(r'<[^>]+>','',s)
    return s.strip()
out=[]
pb=d["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        out.append(f"=== {tier}[{i}] ===")
        out.append("DISPLAY: "+strip(p.get("display","")))
        out.append(f"input_type={p.get('input_type')} solutions={p.get('solutions')} unit={p.get('unit')!r} accept={p.get('accept')} higher_only={p.get('higher_only')} calc={p.get('calculator')}")
        if p.get("options"): out.append("OPTIONS: "+str([strip(o) for o in p["options"]]))
        for m in p.get("misconceptions",[]):
            out.append(f"  MISC pattern={m.get('pattern')} expect={m.get('expect')} :: {strip(m.get('message',''))}")
        gs=p.get("guided_steps")
        if gs:
            for j,st in enumerate(gs):
                if "say" in st and "answer" not in st:
                    out.append(f"  gs[{j}] SAY: {strip(st['say'])}")
                else:
                    ph=st.get("phase","")
                    out.append(f"  gs[{j}] pre='{strip(st.get('pre',''))}' post='{strip(st.get('post',''))}' answer={st.get('answer')} phase={ph} done='{strip(st.get('done','')) }'")
        else:
            out.append("  NO guided_steps")
        out.append("")
io.open("_chk_report.txt","w",encoding="utf-8").write("\n".join(out))
print("\n".join(out))
