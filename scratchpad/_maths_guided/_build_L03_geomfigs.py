# -*- coding: utf-8 -*-
"""Generate exam-realism SVG figures for geometry-L03 (Volume & Surface Area)
programmatically from each problem's own numbers, inject into displays."""
import json, io

SRC = "_L03_fresh_live.json"
OUT = "lesson_geometry-L03_diagrams.json"

def R(v):
    return int(round(v))

def T(x, y, s, anchor="middle", size=11):
    return ('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="%d" '
            'fill="currentColor" text-anchor="%s">%s</text>' % (R(x), R(y), size, anchor, s))

def LN(x1, y1, x2, y2, dash=False, w=1.4):
    d = ' stroke-dasharray="4 3"' if dash else ''
    return ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" '
            'stroke-width="%.1f"%s/>' % (R(x1), R(y1), R(x2), R(y2), w, d))

def POLY(pts, fill="#60a5fa", op=0.30):
    p = " ".join("%d,%d" % (R(a), R(b)) for a, b in pts)
    return ('<polygon points="%s" fill="%s" fill-opacity="%.2f" stroke="currentColor" '
            'stroke-width="1.4" stroke-linejoin="round"/>' % (p, fill, op))

def PATH(d, fill="#60a5fa", op=0.30, dash=False, w=1.4):
    da = ' stroke-dasharray="4 3"' if dash else ''
    f = ('fill="%s" fill-opacity="%.2f"' % (fill, op)) if fill != "none" else 'fill="none"'
    return '<path d="%s" %s stroke="currentColor" stroke-width="%.1f"%s/>' % (d, f, w, da)

def ELL(cx, cy, rx, ry, fill="none", op=0.30):
    f = ('fill="%s" fill-opacity="%.2f"' % (fill, op)) if fill != "none" else 'fill="none"'
    return ('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" %s stroke="currentColor" '
            'stroke-width="1.4"/>' % (R(cx), R(cy), R(rx), R(ry), f))

def SVG(vb, aria, body):
    return ('<svg viewBox="%s" style="display:block;margin:0 auto 0.4rem;max-width:250px;'
            'width:100%%" role="img" aria-label="%s">%s</svg>' % (vb, aria, body))

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

# ---- shape builders -------------------------------------------------------

def cuboid(la, lb, lc, aria, grid=None):
    x, y, w, h = 55, 55, 100, 66
    ox, oy = 46, -34
    A=(x,y); B=(x+w,y); C=(x+w,y+h); D=(x,y+h)
    A2=(x+ox,y+oy); B2=(x+w+ox,y+oy); C2=(x+w+ox,y+h+oy); D2=(x+ox,y+h+oy)
    b = []
    b.append(POLY([A,B,B2,A2]))
    b.append(POLY([B,C,C2,B2]))
    b.append(POLY([A,B,C,D]))
    b.append(LN(*A2, *D2, dash=True)); b.append(LN(*D2, *C2, dash=True)); b.append(LN(*D2, *D, dash=True))
    if grid:
        gw, gd, gh = grid
        for i in range(1, gw):
            fx = x + w*i/gw
            b.append(LN(fx, y, fx, y+h)); b.append(LN(fx, y, fx+ox, y+oy))
        for i in range(1, gh):
            fy = y + h*i/gh
            b.append(LN(x, fy, x+w, fy)); b.append(LN(x+w, fy, x+w+ox, fy+oy))
        for i in range(1, gd):
            b.append(LN(x+ox*i/gd, y+oy*i/gd, x+w+ox*i/gd, y+oy*i/gd))
            b.append(LN(x+w+ox*i/gd, y+oy*i/gd, x+w+ox*i/gd, y+h+oy*i/gd))
    b.append(T(x+w/2, y+h+17, la))
    b.append(T(x-6, y+h/2+4, lc, anchor="end"))
    b.append(T(x+w+ox/2+8, y+oy/2+3, lb, anchor="start"))
    return SVG("0 0 235 150", aria, "".join(b))

def cylinder(rlab, hlab, aria, vlab=None):
    cx, ty, by, rx, ry = 105, 42, 128, 40, 13
    b = []
    b.append(PATH("M %d,%d L %d,%d A %d,%d 0 0 0 %d,%d L %d,%d A %d,%d 0 0 1 %d,%d Z"
                  % (cx-rx,ty, cx-rx,by, rx,ry, cx+rx,by, cx+rx,ty, rx,ry, cx-rx,ty)))
    b.append(ELL(cx, ty, rx, ry))
    b.append(PATH("M %d,%d A %d,%d 0 0 0 %d,%d" % (cx-rx,by,rx,ry,cx+rx,by), fill="none"))
    b.append(PATH("M %d,%d A %d,%d 0 0 1 %d,%d" % (cx-rx,by,rx,ry,cx+rx,by), fill="none", dash=True))
    b.append(LN(cx, ty, cx+rx, ty)); b.append(T(cx+rx/2, ty-4, rlab))
    b.append(LN(cx+rx+14, ty, cx+rx+14, by, dash=True))
    b.append(LN(cx+rx+11, ty, cx+rx+17, ty)); b.append(LN(cx+rx+11, by, cx+rx+17, by))
    b.append(T(cx+rx+21, (ty+by)/2+4, hlab, anchor="start"))
    if vlab:
        b.append(T(cx, by+22, vlab))
    return SVG("0 0 215 %d" % (by + (30 if vlab else 16)), aria, "".join(b))

def cone(rlab, aria, hlab=None, slab=None):
    cx, ay, by, rx, ry = 100, 30, 128, 42, 13
    b = []
    b.append(PATH("M %d,%d L %d,%d A %d,%d 0 0 0 %d,%d Z" % (cx,ay, cx-rx,by, rx,ry, cx+rx,by)))
    b.append(PATH("M %d,%d A %d,%d 0 0 0 %d,%d" % (cx-rx,by,rx,ry,cx+rx,by), fill="none"))
    b.append(PATH("M %d,%d A %d,%d 0 0 1 %d,%d" % (cx-rx,by,rx,ry,cx+rx,by), fill="none", dash=True))
    b.append(LN(cx, by, cx+rx, by)); b.append(T(cx+rx/2, by+16, rlab))
    if hlab:
        b.append(LN(cx, ay, cx, by, dash=True)); b.append(T(cx-6, (ay+by)/2, hlab, anchor="end"))
    if slab:
        b.append(T(cx+rx/2+18, (ay+by)/2, slab, anchor="start"))
    return SVG("0 0 205 %d" % (by+24), aria, "".join(b))

def sphere(aria, rlab="r", vlab=None):
    cx, cy, Rr, ry = 90, 78, 52, 17
    b = []
    b.append('<circle cx="%d" cy="%d" r="%d" fill="#60a5fa" fill-opacity="0.30" stroke="currentColor" stroke-width="1.4"/>' % (cx, cy, Rr))
    b.append(PATH("M %d,%d A %d,%d 0 0 0 %d,%d" % (cx-Rr,cy,Rr,ry,cx+Rr,cy), fill="none"))
    b.append(PATH("M %d,%d A %d,%d 0 0 1 %d,%d" % (cx-Rr,cy,Rr,ry,cx+Rr,cy), fill="none", dash=True))
    ex, ey = cx+Rr*0.62, cy-Rr*0.62
    b.append(LN(cx, cy, ex, ey)); b.append(T((cx+ex)/2+8, (cy+ey)/2, rlab, anchor="start"))
    if vlab:
        b.append(T(cx, 13, vlab))
    return SVG("0 0 190 %d" % (cy+Rr+10), aria, "".join(b))

def hemisphere(rlab, aria):
    cx, cy, Rr, ry = 90, 92, 55, 18
    b = []
    b.append(PATH("M %d,%d A %d,%d 0 0 1 %d,%d Z" % (cx-Rr,cy,Rr,Rr,cx+Rr,cy)))
    b.append(PATH("M %d,%d A %d,%d 0 0 0 %d,%d" % (cx-Rr,cy,Rr,ry,cx+Rr,cy), fill="none"))
    b.append(PATH("M %d,%d A %d,%d 0 0 1 %d,%d" % (cx-Rr,cy,Rr,ry,cx+Rr,cy), fill="none", dash=True))
    b.append(LN(cx, cy, cx+Rr, cy)); b.append(T(cx+Rr/2, cy+16, rlab))
    return SVG("0 0 190 %d" % (cy+22), aria, "".join(b))

def pyramid(base_lab, h_lab, aria):
    cx = 100; bw, bh = 58, 24; yb, ytop = 118, 30
    front=(cx, yb+bh); right=(cx+bw, yb); back=(cx, yb-bh); left=(cx-bw, yb); apex=(cx, ytop)
    b = []
    b.append(POLY([left, front, right, back]))
    b.append(POLY([apex, left, front]))
    b.append(POLY([apex, front, right]))
    b.append(LN(*apex, *back, dash=True))
    b.append(LN(cx, ytop, cx, yb, dash=True))
    b.append(T(cx-6, (ytop+yb)/2, h_lab, anchor="end"))
    b.append(T((cx+cx+bw)/2+4, (yb+bh+yb)/2+12, base_lab, anchor="start"))
    return SVG("0 0 205 150", aria, "".join(b))

def prism(area_lab, len_lab, aria):
    ox, oy = 66, -30
    A=(45,120); B=(105,120); C=(70,55)
    A2=(A[0]+ox,A[1]+oy); B2=(B[0]+ox,B[1]+oy); C2=(C[0]+ox,C[1]+oy)
    b = []
    b.append(POLY([A2,B2,C2], fill="#f59e0b", op=0.22))
    b.append(POLY([B,B2,C2,C]))
    b.append(POLY([A,B,C], fill="#f59e0b", op=0.30))
    b.append(LN(*A,*A2, dash=True)); b.append(LN(*A2,*B2)); b.append(LN(*A2,*C2))
    b.append(LN(*B,*B2)); b.append(LN(*C,*C2))
    b.append(T((A[0]+B[0]+C[0])/3, (A[1]+B[1]+C[1])/3+4, area_lab))
    b.append(T((B[0]+B2[0])/2+8, (B[1]+B2[1])/2+2, len_lab, anchor="start"))
    return SVG("0 0 195 150", aria, "".join(b))

def frustum(aria):
    cx = 100; Rb, rt = 52, 20; ryb, ryt = 15, 9
    yb, yt, yapex = 130, 66, 34
    b = []
    b.append(PATH("M %d,%d L %d,%d A %d,%d 0 0 0 %d,%d L %d,%d A %d,%d 0 0 1 %d,%d Z"
                  % (cx-Rb,yb, cx-rt,yt, rt,ryt, cx+rt,yt, cx+Rb,yb, Rb,ryb, cx-Rb,yb)))
    b.append(PATH("M %d,%d A %d,%d 0 0 0 %d,%d" % (cx-Rb,yb,Rb,ryb,cx+Rb,yb), fill="none"))
    b.append(PATH("M %d,%d A %d,%d 0 0 1 %d,%d" % (cx-Rb,yb,Rb,ryb,cx+Rb,yb), fill="none", dash=True))
    b.append(ELL(cx, yt, rt, ryt))
    b.append(LN(cx-rt, yt, cx, yapex, dash=True)); b.append(LN(cx+rt, yt, cx, yapex, dash=True))
    b.append(LN(cx, yt, cx, yapex, dash=True))
    b.append(LN(cx, yb, cx+Rb, yb)); b.append(T(cx+Rb/2, yb+16, "6 cm"))
    b.append(LN(cx, yt, cx+rt, yt)); b.append(T(cx+rt+4, yt-3, "2 cm", anchor="start"))
    b.append(LN(cx-Rb-12, yb, cx-Rb-12, yapex, dash=True))
    b.append(LN(cx-Rb-15, yb, cx-Rb-9, yb)); b.append(LN(cx-Rb-15, yapex, cx-Rb-9, yapex))
    b.append(T(cx-Rb-16, (yapex+yb)/2, "12 cm", anchor="end"))
    b.append(T(cx+rt+22, (yt+yapex)/2+2, "tip 4 cm", anchor="start"))
    return SVG("0 0 210 150", aria, "".join(b))

def cone_and_cylinder(aria):
    b = []
    cx, ay, by, rx, ry = 52, 34, 120, 28, 9
    b.append(PATH("M %d,%d L %d,%d A %d,%d 0 0 0 %d,%d Z" % (cx,ay, cx-rx,by, rx,ry, cx+rx,by)))
    b.append(PATH("M %d,%d A %d,%d 0 0 0 %d,%d" % (cx-rx,by,rx,ry,cx+rx,by), fill="none"))
    b.append(PATH("M %d,%d A %d,%d 0 0 1 %d,%d" % (cx-rx,by,rx,ry,cx+rx,by), fill="none", dash=True))
    b.append(LN(cx, ay, cx, by, dash=True)); b.append(T(cx-5, (ay+by)/2, "12 cm", anchor="end"))
    b.append(LN(cx, by, cx+rx, by)); b.append(T(cx+rx/2, by+15, "5 cm"))
    dx, ty2, by2, rx2, ry2 = 165, 42, 120, 28, 9
    b.append(PATH("M %d,%d L %d,%d A %d,%d 0 0 0 %d,%d L %d,%d A %d,%d 0 0 1 %d,%d Z"
                  % (dx-rx2,ty2, dx-rx2,by2, rx2,ry2, dx+rx2,by2, dx+rx2,ty2, rx2,ry2, dx-rx2,ty2)))
    b.append(ELL(dx, ty2, rx2, ry2))
    b.append(PATH("M %d,%d A %d,%d 0 0 0 %d,%d" % (dx-rx2,by2,rx2,ry2,dx+rx2,by2), fill="none"))
    b.append(PATH("M %d,%d A %d,%d 0 0 1 %d,%d" % (dx-rx2,by2,rx2,ry2,dx+rx2,by2), fill="none", dash=True))
    b.append(LN(dx+rx2+12, ty2, dx+rx2+12, by2, dash=True)); b.append(T(dx+rx2+16, (ty2+by2)/2, "12 cm", anchor="start"))
    b.append(LN(dx, by2, dx+rx2, by2)); b.append(T(dx+rx2/2, by2+15, "5 cm"))
    return SVG("0 0 225 145", aria, "".join(b))

def hemisphere_on_cylinder(aria):
    cx, ty, by, rx, ry = 95, 82, 152, 44, 14
    Rr = rx
    b = []
    b.append(PATH("M %d,%d L %d,%d A %d,%d 0 0 0 %d,%d L %d,%d A %d,%d 0 0 1 %d,%d Z"
                  % (cx-rx,ty, cx-rx,by, rx,ry, cx+rx,by, cx+rx,ty, rx,ry, cx-rx,ty)))
    b.append(PATH("M %d,%d A %d,%d 0 0 0 %d,%d" % (cx-rx,by,rx,ry,cx+rx,by), fill="none"))
    b.append(PATH("M %d,%d A %d,%d 0 0 1 %d,%d" % (cx-rx,by,rx,ry,cx+rx,by), fill="none", dash=True))
    b.append(PATH("M %d,%d A %d,%d 0 0 1 %d,%d Z" % (cx-Rr,ty,Rr,Rr,cx+Rr,ty)))
    b.append(PATH("M %d,%d A %d,%d 0 0 0 %d,%d" % (cx-rx,ty,rx,ry,cx+rx,ty), fill="none"))
    b.append(PATH("M %d,%d A %d,%d 0 0 1 %d,%d" % (cx-rx,ty,rx,ry,cx+rx,ty), fill="none", dash=True))
    b.append(LN(cx, ty, cx+rx, ty)); b.append(T(cx+rx-6, ty-4, "4 cm", anchor="end"))
    b.append(LN(cx+rx+14, ty, cx+rx+14, by, dash=True))
    b.append(LN(cx+rx+11, ty, cx+rx+17, ty)); b.append(LN(cx+rx+11, by, cx+rx+17, by))
    b.append(T(cx+rx+21, (ty+by)/2, "10 cm", anchor="start"))
    b.append(T(cx, ty-Rr-4, "hemisphere r = 4 cm"))
    return SVG("0 0 205 168", aria, "".join(b))

# ---- assemble -------------------------------------------------------------

pd = json.load(io.open(SRC, encoding="utf-8"))
pb = pd["problem_bank"]
figs = []

def setfig(node, svg, label, cap=True):
    node["display"] = svg + (CAP if cap else "") + node["display"]
    figs.append(label)

# BRONZE
setfig(pb["bronze"][0], cuboid("6 cm","6 cm","6 cm","Cube of side 6 cm"), ("svg","bronze[0]","cube side 6"))
setfig(pb["bronze"][1], cuboid("10 cm","4 cm","3 cm","Cuboid 10 cm by 4 cm by 3 cm"), ("svg","bronze[1]","cuboid 10x4x3"))
setfig(pb["bronze"][2], prism("Area = 15 cm²","9 cm","Triangular prism, cross-section area 15 square cm, length 9 cm"), ("svg","bronze[2]","triangular prism"))
setfig(pb["bronze"][3], cylinder("3 cm","10 cm","Cylinder radius 3 cm, height 10 cm"), ("svg","bronze[3]","cylinder r3 h10"))
setfig(pb["bronze"][4], cuboid("5 cm","5 cm","5 cm","Cube of side 5 cm"), ("svg","bronze[4]","cube side 5"))
setfig(pb["bronze"][5], cuboid("8 cm","3 cm","2 cm","Cuboid 8 cm by 3 cm by 2 cm"), ("svg","bronze[5]","cuboid 8x3x2"))
setfig(pb["bronze"][6], cylinder("4 cm","7 cm","Cylinder radius 4 cm, height 7 cm"), ("svg","bronze[6]","cylinder r4 h7"))
setfig(pb["bronze"][7], cuboid("40 cm","25 cm","30 cm","Fish tank, a cuboid 40 cm by 25 cm by 30 cm"), ("svg","bronze[7]","tank 40x25x30"))

# SILVER
setfig(pb["silver"][0], sphere("Sphere of radius 6 cm", rlab="6 cm"), ("svg","silver[0]","sphere r6"))
setfig(pb["silver"][1], cone("5 cm","Cone radius 5 cm, height 12 cm", hlab="12 cm"), ("svg","silver[1]","cone r5 h12"))
setfig(pb["silver"][2], cylinder("5 cm","h = ?","Cylinder radius 5 cm, volume 500 cubic cm, height unknown", vlab="V = 500 cm³"), ("svg","silver[2]","cylinder V500 find h"))
setfig(pb["silver"][3], cone("4 cm","Cone radius 4 cm, slant height 9 cm", slab="l = 9 cm"), ("svg","silver[3]","cone r4 slant9"))
setfig(pb["silver"][4], sphere("Sphere of radius 4 cm", rlab="4 cm"), ("svg","silver[4]","sphere r4"))
setfig(pb["silver"][5], pyramid("6 cm","10 cm","Square-based pyramid, base 6 cm, height 10 cm"), ("svg","silver[5]","pyramid base6 h10"))
setfig(pb["silver"][6], hemisphere("8 cm","Hemisphere of radius 8 cm"), ("svg","silver[6]","hemisphere r8"))

# GOLD
setfig(pb["gold"][0], sphere("Sphere of volume 288 pi cubic cm, radius unknown", rlab="r = ?", vlab="V = 288π cm³"), ("svg","gold[0]","sphere V288pi find r"))
setfig(pb["gold"][1], cone_and_cylinder("A cone and a cylinder, both radius 5 cm and height 12 cm"), ("svg","gold[1]","cone+cylinder pair"))
setfig(pb["gold"][2], hemisphere_on_cylinder("Solid hemisphere radius 4 cm on a cylinder radius 4 cm height 10 cm"), ("svg","gold[2]","hemisphere on cylinder"))
setfig(pb["gold"][3], sphere("Sphere of surface area 100 pi square cm, radius unknown", rlab="r = ?", vlab="SA = 100π cm²"), ("svg","gold[3]","sphere SA100pi find r"))
setfig(pb["gold"][4], frustum("Frustum: large cone radius 6 cm height 12 cm with a cone radius 2 cm height 4 cm removed from the top"), ("svg","gold[4]","frustum"))

# TEACH walks
tw = pd["guided"]["teach"]
tw["bronze"]["display"] = cuboid("5 cm","4 cm","2 cm","Cuboid 5 cm by 4 cm by 2 cm") + CAP + tw["bronze"]["display"]
figs.append(("svg","teach.bronze","cuboid 5x4x2"))
tw["silver"]["display"] = cone("3 cm","Cone radius 3 cm, height 8 cm", hlab="8 cm") + CAP + tw["silver"]["display"]
figs.append(("svg","teach.silver","cone r3 h8"))
tw["gold"]["display"] = sphere("Sphere of volume 36 pi cubic cm, radius unknown", rlab="r = ?", vlab="V = 36π cm³") + CAP + tw["gold"]["display"]
figs.append(("svg","teach.gold","sphere V36pi find r"))

# OPENER (literal counting grid, no not-to-scale caption)
op = pd["guided"]["opener"]
op["display"] = cuboid("3 cm","2 cm","2 cm","A box 3 cm by 2 cm by 2 cm shown as a grid of 1 cm cubes", grid=(3,2,2)) + op["display"]
figs.append(("svg","opener","box of unit cubes 3x2x2"))

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("figures added:", len(figs))
maxlen = 0
for t in ("bronze","silver","gold"):
    for i, p in enumerate(pb[t]):
        d = p.get("display","")
        assert d.count("<svg") == 1, (t, i)
        maxlen = max(maxlen, len(d))
print("max display len:", maxlen)
for f in figs:
    print("  ", f[1], f[2])
