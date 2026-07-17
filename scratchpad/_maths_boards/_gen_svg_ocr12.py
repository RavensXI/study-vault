# -*- coding: utf-8 -*-
def parabola_svg(a,b,c,r1,r2,label,region,aria):
    # region: "between" (shade below-axis dip) or "outside" (shade above-axis arms)
    import math
    lo,hi=min(r1,r2),max(r1,r2)
    span=hi-lo
    xmin=lo-0.6*span-0.4
    xmax=hi+0.6*span+0.4
    def f(x): return a*x*x+b*x+c
    N=68
    xs=[xmin+(xmax-xmin)*i/N for i in range(N+1)]
    ys=[f(x) for x in xs]
    fmin=min(ys); fmax=max(ys)
    # px mapping
    def PX(x): return 20+(x-xmin)/(xmax-xmin)*206
    # py mapping: fmax->16 (top), fmin->150 (bottom)
    def PY(v): return 16+(fmax-v)/(fmax-fmin)*(150-16)
    py0=PY(0)
    pts=[(PX(x),PY(f(x))) for x in xs]
    poly=" ".join(f"{px:.2f},{py:.2f}" for px,py in pts)
    # roots pixel
    pr1=PX(lo); pr2=PX(hi)
    parts=[]
    parts.append(f'<svg viewBox="0 0 240 172" role="img" aria-label="{aria}" style="max-width:240px;font-family:Inter,sans-serif">')
    # axis of symmetry faint vertical
    axsym=PX((lo+hi)/2)
    parts.append(f'<line x1="20" y1="{py0:.2f}" x2="226" y2="{py0:.2f}" stroke="currentColor" stroke-width="1"/>')
    parts.append(f'<line x1="{axsym:.2f}" y1="16" x2="{axsym:.2f}" y2="150" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.5"/>')
    if region=="between":
        # dip between roots: curve points where lo<=x<=hi
        dip=[(px,py) for (px,py),x in zip(pts,xs) if lo-1e-9<=x<=hi+1e-9]
        dip=[(pr1,py0)]+dip+[(pr2,py0)]
        parts.append(f'<polygon points="{" ".join(f"{px:.2f},{py:.2f}" for px,py in dip)}" fill="#60a5fa" fill-opacity="0.3" stroke="none"/>')
    else:
        left=[(px,py) for (px,py),x in zip(pts,xs) if x<=lo+1e-9]
        left=[(20,py0)]+left+[(pr1,py0)]
        right=[(px,py) for (px,py),x in zip(pts,xs) if x>=hi-1e-9]
        right=[(pr2,py0)]+right+[(226,py0)]
        parts.append(f'<polygon points="{" ".join(f"{px:.2f},{py:.2f}" for px,py in left)}" fill="#60a5fa" fill-opacity="0.3" stroke="none"/>')
        parts.append(f'<polygon points="{" ".join(f"{px:.2f},{py:.2f}" for px,py in right)}" fill="#60a5fa" fill-opacity="0.3" stroke="none"/>')
    parts.append(f'<polyline points="{poly}" fill="none" stroke="#60a5fa" stroke-width="1.8"/>')
    parts.append(f'<circle cx="{pr1:.2f}" cy="{py0:.2f}" r="2.6" fill="currentColor"/>')
    parts.append(f'<circle cx="{pr2:.2f}" cy="{py0:.2f}" r="2.6" fill="currentColor"/>')
    parts.append(f'<text x="226" y="{py0-3:.2f}" font-size="9" fill="currentColor" text-anchor="end" opacity="0.7">x</text>')
    parts.append(f'<text x="120" y="12" font-size="11" fill="currentColor" text-anchor="middle">{label}</text>')
    parts.append('</svg>')
    return "".join(parts), (pr1,pr2,py0,PX(0) if xmin<0<xmax else None)

if __name__=="__main__":
    for (a,b,c,r1,r2,lab,reg) in [
        (1,-8,15,3,5,"y = x squared minus 8x plus 15","between"),
        (1,2,-8,-4,2,"y = x squared plus 2x minus 8","outside"),
        (2,1,-6,-2,1.5,"y = 2x squared plus x minus 6","outside"),
    ]:
        svg,info=parabola_svg(a,b,c,r1,r2,lab,reg,"test")
        print(lab,"roots px:",round(info[0],1),round(info[1],1),"axis y:",round(info[2],1),"len:",len(svg))
