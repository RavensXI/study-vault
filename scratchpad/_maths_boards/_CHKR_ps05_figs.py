import json, re
live = json.load(open("_CHKR_ps05_live.json", encoding="utf-8"))
issues = []

def axis_from_ticks(svg):
    # find tick text labels with numeric content and their x from preceding line or the text x
    # texts of form <text x="X" ...>NUM</text> where NUM is an axis number on baseline
    ticks = []
    for m in re.finditer(r'<text x="([\d.]+)" y="(\d+)"[^>]*>(\d+(?:\.\d+)?)</text>', svg):
        x=float(m.group(1)); y=int(m.group(2)); val=float(m.group(3))
        ticks.append((x,y,val))
    return ticks

def linmap(ticks):
    # use two extreme axis ticks (largest y = baseline labels). pick ticks sharing the max y
    if not ticks: return None
    maxy = max(t[1] for t in ticks)
    base = [t for t in ticks if t[1]==maxy]
    base.sort(key=lambda t:t[2])
    if len(base)<2: return None
    (x0,_,v0),(x1,_,v1)=base[0],base[-1]
    scale=(x1-x0)/(v1-v0)
    return lambda x:(x-x0)/scale+v0, base

def check_boxplot(svg, label, claims):
    res=linmap(axis_from_ticks(svg))
    if not res:
        issues.append(f"{label}: no axis"); return
    inv,base=res
    # rects (box)
    for m in re.finditer(r'<rect x="([\d.]+)" y="\d+" width="([\d.]+)"', svg):
        x=float(m.group(1)); w=float(m.group(2))
        left=inv(x); right=inv(x+w)
        print(f"  {label} box left={left:.2f} right={right:.2f}")
    # vertical median/whisker lines x1==x2
    for m in re.finditer(r'<line x1="([\d.]+)" y1="\d+" x2="([\d.]+)" y2="\d+"', svg):
        x1=float(m.group(1)); x2=float(m.group(2))
        if abs(x1-x2)<0.01:
            print(f"  {label} vline at value {inv(x1):.2f}")

pb=live["problem_bank"]
# box plot problems
for tier,i,claims in [("gold",1,"A Q115 med22 Q3 30; B Q1 18 med25 Q3 32"),
                      ("bronze",3,"min10 Q1 15 med20 Q3 28 max35"),
                      ("silver",3,"A Q1 20 Q3 45; B Q1 25 Q3 55")]:
    d=pb[tier][i]["display"]
    print(f"--- {tier}[{i}] {claims}")
    check_boxplot(d,f"{tier}[{i}]",claims)

# histograms: check bar heights proportional to FD, widths proportional to class span
def check_hist(svg,label,classes):
    # classes: list of (lo,hi,fd). find rects and the axis text tick x for boundaries
    inv_res=linmap([t for t in axis_from_ticks(svg)])
    # x-axis boundary ticks are the small-value labels near y=112
    ticks=[t for t in axis_from_ticks(svg) if t[1]>=110]
    ticks.sort(key=lambda t:t[2])
    print(f"  {label} x-ticks:", [(t[2],t[0]) for t in ticks])
    rects=[(float(m.group(1)),float(m.group(2)),float(m.group(3))) for m in
           re.finditer(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"',svg)]
    rects=[(float(m.group(1)),float(m.group(4)),float(m.group(3))) for m in
           re.finditer(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"',svg)]
    # height/fd ratio should be constant
    ratios=[]
    for (x,h,w),(lo,hi,fd) in zip(rects,classes):
        ratios.append(h/fd)
        print(f"    class {lo}-{hi} fd={fd}: rect h={h} w={w} h/fd={h/fd:.3f}")
    if ratios and (max(ratios)-min(ratios))>0.5:
        issues.append(f"{label}: bar height/FD not constant {ratios}")

print("--- gold[0] hist 0-10 fd1.2,10-20 fd2.5,20-40 fd1.8")
check_hist(pb["gold"][0]["display"],"gold[0]",[(0,10,1.2),(10,20,2.5),(20,40,1.8)])
print("--- gold[3] hist 0-5 fd4,5-15 fd2,15-20 fd6")
check_hist(pb["gold"][3]["display"],"gold[3]",[(0,5,4),(5,15,2),(15,20,6)])
print("--- teach.gold hist 0-10 fd1.5,10-30 fd2,30-60 fd1")
check_hist(live["guided"]["teach"]["gold"]["display"],"teach.gold",[(0,10,1.5),(10,30,2),(30,60,1)])

print("\nISSUES:", issues if issues else "none")
