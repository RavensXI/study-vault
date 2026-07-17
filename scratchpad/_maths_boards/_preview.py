import json,re
pd=json.load(open("lesson_geometry-L01.json",encoding="utf-8"))
svgs=[]
def grab(disp,tag):
    m=re.search(r'<svg.*?</svg>',disp,re.S)
    if m: svgs.append((tag,m.group(0)))
grab(pd["guided"]["opener"]["display"],"opener pizza (120,150,? -> 90)")
pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        grab(p["display"],f"{tier}[{i}]")
html="<html><body style='background:#faf8f5;color:#2d2a26;font-family:Inter,sans-serif'><div style='display:flex;flex-wrap:wrap;gap:20px'>"
for tag,s in svgs:
    html+=f"<figure style='width:260px;border:1px solid #ccc;padding:6px;margin:0'><figcaption style='font-size:12px'>{tag}</figcaption>{s}</figure>"
html+="</div></body></html>"
open("_preview.html","w",encoding="utf-8").write(html)
print("figures:",len(svgs))
