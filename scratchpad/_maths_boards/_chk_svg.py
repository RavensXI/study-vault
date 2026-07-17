import json,re,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_CHK_LIVE_fresh.json",encoding="utf-8"))["practice_data"]

def get_axes(svg):
    # x tick labels: <text ...>N</text> preceded by tick line at x=..; parse tick lines with y at axis
    # Instead parse from labelled ticks: find all <line x1=A y1=B x2=A y2=B+3> then text at x=A
    return svg

def parse_ticks(svg):
    # x ticks: small vertical lines length 3 below axis, with a number text at same x
    texts=re.findall(r'<text x="([\-\d.]+)" y="[\-\d.]+" font-size="9"[^>]*text-anchor="middle">([\-\d]+)</text>',svg)
    xmap={} # px->val
    for px,val in texts:
        xmap[float(px)]=int(val)
    ytexts=re.findall(r'<text x="([\-\d.]+)" y="([\-\d.]+)" font-size="9"[^>]*text-anchor="end">([\-\d]+)</text>',svg)
    ymap={}
    for px,py,val in ytexts:
        ymap[float(py)]=int(val)
    return xmap,ymap

def linfit(m):
    items=sorted(m.items())
    (p1,v1),(p2,v2)=items[0],items[-1]
    scale=(v2-v1)/(p2-p1)
    return lambda p:(p-p1)*scale+v1

def check(name,svg,f):
    xmap,ymap=parse_ticks(svg)
    fx=linfit(xmap); fy=linfit(ymap)
    poly=re.search(r'<polyline points="([^"]+)"',svg).group(1)
    pts=[tuple(map(float,p.split(','))) for p in poly.split()]
    errs=0
    for px,py in pts[::12]:
        x=fx(px); y=fy(py); yt=f(x)
        if abs(y-yt)>0.25:
            print(f"  {name} MISMATCH px={px} x={x:.2f} plotted_y={y:.2f} eqn_y={yt:.2f}"); errs+=1
    # check markers (circles)
    print(f"{name}: {len(pts)} pts, {errs} mismatches; xmap={xmap}; ymap={ymap}")
    return errs

tot=0
tot+=check("teach.gold", pd["guided"]["teach"]["gold"]["display"], lambda x:-x**2+4*x-1)
tot+=check("teach.bronze", pd["guided"]["teach"]["bronze"]["display"], lambda x:x**2-2*x-3)
tot+=check("teach.silver", pd["guided"]["teach"]["silver"]["display"], lambda x:x**2-6*x+8)
# opener: arch through (0,0),(8,0),(4,?) height; symmetric; parametric not an eqn but check symmetry & 3m@2 ->? 
op=pd["guided"]["opener"]["display"]
xmap,ymap=parse_ticks(op)
print("opener xmap:",xmap)
print("TOTAL svg mismatches:",tot)
