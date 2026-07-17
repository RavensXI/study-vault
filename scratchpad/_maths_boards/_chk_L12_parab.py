import json, re

pd = json.load(open("_chk_L12_live.json", encoding="utf-8"))
teach = pd["guided"]["teach"]

# For each teach parabola: roots (circles on axis) should sit at midpoint symmetric,
# and shaded polygon should be between roots (bronze/gold, <0) or outside (silver, >=0).
for tier, (r1,r2,mode) in {
    "bronze": (3,4,"between"),
    "silver": (-3,5,"outside"),
    "gold": (-3,0.5,"between"),
}.items():
    svg = teach[tier]["display"]
    axis_y = re.search(r'<line x1="20" y1="([\d.]+)" x2="226"', svg).group(1)
    circs = re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="2.6"', svg)
    rootpx = sorted(float(cx) for cx,cy in circs)
    # all circles on axis?
    onaxis = all(abs(float(cy)-float(axis_y))<0.5 for cx,cy in circs)
    # vertex (lowest polyline point) x
    poly = re.search(r'<polyline points="([^"]+)"', svg).group(1)
    pts = [tuple(map(float,p.split(","))) for p in poly.split()]
    vy = max(p[1] for p in pts)
    vx = [p[0] for p in pts if p[1]==vy][0]
    mid = sum(rootpx)/2
    print(f"{tier}: roots@{rootpx} axis_y={axis_y} onaxis={onaxis} vertex_x={vx} midpoint={mid:.1f} sym={abs(vx-mid)<1.0}")
