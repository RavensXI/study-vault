import json,re
live=json.load(open("_ADVCHK_L13_live.json",encoding="utf-8"))
# --- verify fix 1: gold sum=175 -> integer n
# n(3n+5)=2*175=350 ; 3n^2+5n-350=0
import math
disc=25+4*3*350
print("gold sum=175 disc sqrt:",math.isqrt(disc)**2==disc, "n=",(-5+math.isqrt(disc))/6)
# old 115:
disc0=25+4*3*230
print("old sum=115 integer?:",math.isqrt(disc0)**2==disc0)
# --- verify fix 2: silver 20,17,14,11 options no duplicate, index2=17-3n
opts=live["problem_bank"]["silver"][2]["options"]
print("silver[2] opts:",opts)
# evaluate each as function of n=1 to see distinctness at n=1
def ev(o,n):
    o=o.replace("\(","").replace("\)","").replace(" ","")
    o=o.replace("−","-")
    # forms: a-3n , 3n+a, etc
    m=re.match(r"^(-?\d+)-3n$",o)
    if m: return int(m.group(1))-3*n
    m=re.match(r"^3n\+(-?\d+)$",o)
    if m: return 3*n+int(m.group(1))
    return None
vals=[ev(o,1) for o in opts]
print("values at n=1:",vals,"target 20; distinct:",len(set(vals))==len(vals))
# --- SVG figure audits
def count_svg(html,tag):
    return len(re.findall("<"+tag,html))
op=live["guided"]["opener"]["display"]
bt=live["guided"]["teach"]["bronze"]["display"]
print("opener rects:",count_svg(op,"rect"),"(1 screen + 5+7+9=21 seats =22)")
print("bronze teach circles:",count_svg(bt,"circle"),"(3+5+7=15)")
# theme safety: any hardcoded near-black fill in <text>?
for name,html in [("opener",op),("bronze",bt)]:
    texts=re.findall(r"<text[^>]*>",html)
    bad=[t for t in texts if "currentColor" not in t]
    print(name,"text elems:",len(texts),"non-currentColor:",len(bad))
    print(name,"external refs (http/xlink):", ("http" in html or "xlink" in html))
