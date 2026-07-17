import json, re

live = json.load(open(r"_CHK_gL04ocr_pd.json", encoding="utf-8"))
pb = live["problem_bank"]

def analyze(label, disp):
    svg = re.search(r"<svg.*?</svg>", disp, re.S)
    if not svg:
        return
    s = svg.group(0)
    # bold axes: stroke-width 1.6 lines -> find x-axis (horizontal) y and y-axis (vertical) x
    axes = re.findall(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)" stroke="currentColor" stroke-width="1.6"', s)
    x_axis_y = None; y_axis_x = None
    for x1,y1,x2,y2 in axes:
        x1,y1,x2,y2=map(float,(x1,y1,x2,y2))
        if abs(y1-y2)<0.5:  # horizontal
            x_axis_y=y1; origin_x=min(x1,x2)
        if abs(x1-x2)<0.5:  # vertical
            y_axis_x=x1;
    # grid spacing: from faint vertical lines x positions
    vx = sorted(set(float(x) for x in re.findall(r'<line x1="([\d.]+)" y1="[\d.]+" x2="\1"', s)))
    # simpler: gather all vertical faint line x's
    vlines = sorted(set(float(m) for m in re.findall(r'<line x1="([\d.]+)" y1="[\d.]+" x2="[\d.]+" y2="[\d.]+" stroke="currentColor" stroke-opacity="0.12"', s) if True))
    # need pairs where x1==x2
    vpos=[]; hpos=[]
    for m in re.finditer(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)" stroke="currentColor" stroke-opacity="0.12"', s):
        x1,y1,x2,y2=map(float,m.groups())
        if abs(x1-x2)<0.5: vpos.append(x1)
        if abs(y1-y2)<0.5: hpos.append(y1)
    vpos=sorted(set(vpos)); hpos=sorted(set(hpos))
    stepx = vpos[1]-vpos[0]
    stepy = hpos[1]-hpos[0]
    ox = vpos[0]  # x=0 at leftmost vertical (=y-axis)
    oy = max(hpos)  # y=0 at bottom (x-axis)
    def to_grid(cx,cy):
        return round((cx-ox)/stepx,2), round((oy-cy)/stepy,2)
    print(f"\n{label}: origin=({ox},{oy}) stepx={stepx:.2f} stepy={stepy:.2f}")
    for m in re.finditer(r'<circle cx="([\d.]+)" cy="([\d.]+)"', s):
        cx,cy=map(float,m.groups())
        print("  circle ->", to_grid(cx,cy))
    # X marks (centre): pairs of crossing lines width 1.8; take midpoint
    xl=[]
    for m in re.finditer(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)" stroke="currentColor" stroke-width="1.8"', s):
        x1,y1,x2,y2=map(float,m.groups())
        xl.append(((x1+x2)/2,(y1+y2)/2))
    if xl:
        mx=sum(p[0] for p in xl)/len(xl); my=sum(p[1] for p in xl)/len(xl)
        print("  X-mark ->", to_grid(mx,my))
    # labels
    for m in re.finditer(r'>([^<]*\([^)]*\)[^<]*)</text>', s):
        print("  label:", m.group(1))

for tier in ["silver","gold"]:
    for i,p in enumerate(pb[tier]):
        analyze(f"{tier}[{i}]", p["display"])
