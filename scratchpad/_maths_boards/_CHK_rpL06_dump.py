import json,io,re
pd=json.load(open("_CHK_rpL06_live.json",encoding="utf-8"))["practice_data"]
out=io.open("_CHK_rpL06_bank.txt","w",encoding="utf-8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n")
pb=pd["problem_bank"]
def strip_svg(s):
    if s is None: return s
    return re.sub(r'<svg.*?</svg>','[SVG]',s,flags=re.S)
for tier in ["bronze","silver","gold"]:
    probs=pb[tier]
    w(f"\n===== {tier.upper()} ({len(probs)} problems) desc: {pb.get(tier+'_description')}")
    for i,p in enumerate(probs):
        w(f"\n--- {tier}[{i}] input_type={p.get('input_type')} calculator={p.get('calculator')} chart={'chart' in p}")
        w("DISPLAY:",strip_svg(p.get("display")))
        w("SOLUTIONS:",p.get("solutions"))
        w("HINT:",p.get("hint"))
        mc=p.get("misconceptions",[])
        for j,m in enumerate(mc):
            w(f"  MISC[{j}] expect={m.get('expect')} pattern={m.get('pattern')} msg={m.get('message')}")
out.close()
print("done")
