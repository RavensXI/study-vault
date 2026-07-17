import json,io,re
pd=json.load(open("_CHK_rpL06_live.json",encoding="utf-8"))["practice_data"]
out=io.open("_CHK_rpL06_guided.txt","w",encoding="utf-8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n")
def sv(s): return re.sub(r'<svg.*?</svg>','[SVG]',s,flags=re.S) if isinstance(s,str) else s
g=pd["guided"]
w("=== OPENER ===")
op=g.get("opener",{})
w(json.dumps(op,ensure_ascii=False,indent=1))
w("\n=== TEACH ===")
for tier in ["bronze","silver","gold"]:
    t=g.get("teach",{}).get(tier,{})
    w(f"\n--- teach.{tier} ---")
    w(json.dumps(t,ensure_ascii=False,indent=1))
out.close()
print("written", out)
