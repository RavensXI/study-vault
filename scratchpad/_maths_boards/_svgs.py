# -*- coding: utf-8 -*-
# Gradient-from-two-points figure generator. Theme-safe (currentColor), soft triangle fill.
def fnum(v):
    s = ("%g" % v)
    return s

def grad_fig(p1, p2, xr, yr, aria):
    (x1,y1),(x2,y2) = p1,p2
    xmin,xmax = xr; ymin,ymax = yr
    L,R,T,B = 42.0,214.0,22.0,168.0  # plot box in svg px
    def sx(x): return L + (x-xmin)/(xmax-xmin)*(R-L)
    def sy(y): return B - (y-ymin)/(ymax-ymin)*(B-T)
    def f(v): return round(v,1)
    # axis positions (data 0 lines if in range else clamp)
    ax0 = sx(0) if xmin<=0<=xmax else L
    ay0 = sy(0) if ymin<=0<=ymax else B
    P1=(sx(x1),sy(y1)); P2=(sx(x2),sy(y2))
    # extend line slightly beyond points
    dx=x2-x1; dy=y2-y1
    ex1=x1-0.4*dx; ey1=y1-0.4*dy; ex2=x2+0.4*dx; ey2=y2+0.4*dy
    # clamp extension to plot ranges roughly
    A=(sx(ex1),sy(ey1)); Bp=(sx(ex2),sy(ey2))
    run=x2-x1; rise=y2-y1
    # rise/run triangle: horizontal from P1 to (x2,y1), vertical up to P2
    Cx,Cy = sx(x2),sy(y1)
    parts=[]
    parts.append('<svg viewBox="0 0 240 190" role="img" aria-label="%s" style="max-width:260px">'%aria)
    parts.append('<style>text{font-family:Inter,system-ui,sans-serif;font-size:11px;fill:currentColor}</style>')
    # axes
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1" opacity="0.55"/>'%(ax0,T-4,ax0,B+4))
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1" opacity="0.55"/>'%(L-4,ay0,R+4,ay0))
    parts.append('<text x="%.1f" y="%.1f">x</text>'%(R+2,ay0+13))
    parts.append('<text x="%.1f" y="%.1f">y</text>'%(ax0-12,T-2))
    # rise/run triangle
    parts.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#60a5fa" fill-opacity="0.3" stroke="none"/>'%(P1[0],P1[1],Cx,Cy,P2[0],P2[1]))
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.8"/>'%(P1[0],P1[1],Cx,Cy))
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.8"/>'%(Cx,Cy,P2[0],P2[1]))
    # the tangent line
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#2563eb" stroke-width="2"/>'%(A[0],A[1],Bp[0],Bp[1]))
    # points
    for (px,py,lx,ly) in [(P1[0],P1[1],x1,y1),(P2[0],P2[1],x2,y2)]:
        parts.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#2563eb"/>'%(px,py))
    parts.append('<text x="%.1f" y="%.1f">(%s, %s)</text>'%(P1[0]-4,P1[1]+16,fnum(x1),fnum(y1)))
    parts.append('<text x="%.1f" y="%.1f">(%s, %s)</text>'%(P2[0]-30,P2[1]-6,fnum(x2),fnum(y2)))
    # run/rise labels
    parts.append('<text x="%.1f" y="%.1f">run %s</text>'%((P1[0]+Cx)/2-14,Cy+15,fnum(run)))
    parts.append('<text x="%.1f" y="%.1f">rise %s</text>'%(Cx+4,(Cy+P2[1])/2+3,fnum(rise)))
    parts.append('</svg>')
    return "".join(parts)

figs = {
 "b0": grad_fig((1,3),(5,11),(0,6),(0,12),"A line through the points (1, 3) and (5, 11) on x-y axes, with a rise and run triangle marked"),
 "b1": grad_fig((0,4),(2,10),(0,3),(0,12),"A line through the points (0, 4) and (2, 10) on x-y axes, with a rise and run triangle marked"),
 "b4": grad_fig((1,-2),(5,14),(0,6),(-4,16),"A line through the points (1, -2) and (5, 14) on x-y axes, with a rise and run triangle marked"),
}
for k,v in figs.items():
    print(k, "len", len(v))
    print(v)
    print()
