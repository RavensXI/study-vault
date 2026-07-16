# -*- coding: utf-8 -*-
"""Add the missing opener/teach figures for probability-statistics-L03.
Draws every figure PROGRAMMATICALLY from the problem's own numbers,
matching the house style of the existing problem-bank pie/bar SVGs.
"""
import json, io, math

pd = json.load(io.open("_L03_live_fresh.json", encoding="utf-8"))

def sector(cx, cy, r, start_deg, sweep_deg):
    """Path for a pie sector swept CLOCKWISE from `start_deg` (0=top) by sweep."""
    def pt(a):
        rad = math.radians(a)
        return (cx + r * math.sin(rad), cy - r * math.cos(rad))
    x0, y0 = pt(start_deg)
    x1, y1 = pt(start_deg + sweep_deg)
    large = 1 if sweep_deg > 180 else 0
    return "M%g %g L%s %s A%g %g 0 %d 1 %s %s Z" % (
        cx, cy, fmt(x0), fmt(y0), r, r, large, fmt(x1), fmt(y1))

def polar(cx, cy, r, a):
    rad = math.radians(a)
    return (cx + r * math.sin(rad), cy - r * math.cos(rad))

def fmt(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")

# ---------------------------------------------------------------- OPENER pie
# 20 friends: Margherita half (180), Pepperoni quarter (90), Veggie quarter (90)
cx, cy, r = 110, 100, 68
seg = [("Margherita", "1/2", 0, 180, "#f59e0b"),
       ("Pepperoni", "1/4", 180, 90, "#60a5fa"),
       ("Veggie", "1/4", 270, 90, "#34d399")]
parts = ['<svg viewBox="0 0 220 210" role="img" aria-label="Pizza pie chart: '
         'Margherita is half the circle, Pepperoni a quarter, Veggie a quarter" '
         'style="max-width:220px;font-family:Inter,sans-serif">']
parts.append('<circle cx="110" cy="100" r="68" fill="none" stroke="currentColor" stroke-width="1.5"/>')
for name, frac, start, sweep, col in seg:
    parts.append('<path d="%s" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
                 % (sector(cx, cy, r, start, sweep), col))
    lx, ly = polar(cx, cy, r, start + sweep / 2)
    lx, ly = polar(cx, cy, 40, start + sweep / 2)  # label at radius 40
    parts.append('<text x="%s" y="%s" text-anchor="middle" font-size="11" fill="currentColor">%s</text>'
                 % (fmt(lx), fmt(ly - 3), name))
    parts.append('<text x="%s" y="%s" text-anchor="middle" font-size="12" fill="currentColor">%s</text>'
                 % (fmt(lx), fmt(ly + 11), frac))
parts.append('<text x="110" y="202" text-anchor="middle" font-size="11" fill="currentColor">20 friends share a pizza</text>')
parts.append('</svg>')
opener_svg = "".join(parts)
pd["guided"]["opener"]["display"] = opener_svg

# ---------------------------------------------------------------- SILVER teach: single pie 120, rugby 60
cx, cy, r = 110, 100, 68
ang = 60
ex, ey = polar(cx, cy, r, ang)
lx, ly = polar(cx, cy, 40, ang / 2)      # angle label
qx, qy = polar(cx, cy, 22, ang / 2)      # ? inside shaded sector, deeper
silver_svg = (
    '<svg viewBox="0 0 220 200" role="img" '
    'aria-label="Pie chart of 120 people, the rugby sector is 60 degrees" '
    'style="max-width:220px;font-family:Inter,sans-serif">'
    '<text x="110" y="16" text-anchor="middle" font-size="12" fill="currentColor">120 people</text>'
    '<circle cx="110" cy="100" r="68" fill="none" stroke="currentColor" stroke-width="1.5"/>'
    '<path d="%s" fill="#a78bfa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    '<text x="%s" y="%s" text-anchor="middle" font-size="12" fill="currentColor">60°</text>'
    '<text x="%s" y="%s" text-anchor="middle" font-size="13" fill="currentColor">?</text>'
    '<text x="110" y="192" text-anchor="middle" font-size="11" fill="currentColor">Shaded sector = rugby</text>'
    '</svg>'
) % (sector(cx, cy, r, 0, ang), fmt(lx), fmt(ly + 4), fmt(qx), fmt(qy + 4))
pd["guided"]["teach"]["silver"]["display"] = (
    silver_svg + "120 people were surveyed. On a pie chart the slice for rugby is 60°. How many people chose rugby?")

# ---------------------------------------------------------------- BRONZE teach: bar chart Walk 9 Bus 7 Car 5 Cycle 4
bars = [("Walk", 9), ("Bus", 7), ("Car", 5), ("Cycle", 4)]
base_y = 150
scale = 11.0            # px per unit
axis_x = 40
centers = [60, 105, 150, 195]
bw = 30
p = ['<svg viewBox="0 0 240 180" role="img" '
     'aria-label="Bar chart of travel to school: Walk 9, Bus 7, Car 5, Cycle 4" '
     'style="max-width:240px;font-family:Inter,sans-serif">']
# axes
p.append('<line x1="40" y1="40" x2="40" y2="150" stroke="currentColor" stroke-width="1.2"/>')
p.append('<line x1="40" y1="150" x2="236" y2="150" stroke="currentColor" stroke-width="1.2"/>')
# y ticks 0..10 step 2
for t in range(0, 11, 2):
    ty = base_y - t * scale
    p.append('<line x1="37" y1="%g" x2="40" y2="%g" stroke="currentColor" stroke-width="1"/>' % (ty, ty))
    p.append('<text x="32" y="%g" text-anchor="end" font-size="9" fill="currentColor">%d</text>' % (ty + 3, t))
# bars
for (name, val), c in zip(bars, centers):
    h = val * scale
    y = base_y - h
    p.append('<rect x="%g" y="%s" width="%d" height="%s" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.2"/>'
             % (c - bw / 2, fmt(y), bw, fmt(h)))
    p.append('<text x="%d" y="%s" text-anchor="middle" font-size="11" fill="currentColor">%d</text>' % (c, fmt(y - 4), val))
    p.append('<text x="%d" y="164" text-anchor="middle" font-size="10" fill="currentColor">%s</text>' % (c, name))
p.append('<text x="10" y="95" text-anchor="middle" font-size="9" fill="currentColor" transform="rotate(-90 10 95)">Students</text>')
p.append('</svg>')
bronze_svg = "".join(p)
pd["guided"]["teach"]["bronze"]["display"] = (
    bronze_svg + "A bar chart shows how a class travels to school: Walk 9, Bus 7, Car 5, Cycle 4. How many more walk than cycle?")

# ---------------------------------------------------------------- GOLD teach: two pies Club A 240 (90), Club B 300 (60)
def one_pie(cx, title, ang, col, qxy):
    ex, ey = polar(cx, 100, 46, ang)
    lx, ly = polar(cx, 100, 30, ang / 2)
    out = ['<text x="%d" y="16" text-anchor="middle" font-size="11" fill="currentColor">%s</text>' % (cx, title)]
    out.append('<circle cx="%d" cy="100" r="46" fill="none" stroke="currentColor" stroke-width="1.5"/>' % cx)
    out.append('<path d="%s" fill="%s" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
               % (sector(cx, 100, 46, 0, ang), col))
    out.append('<text x="%s" y="%s" text-anchor="middle" font-size="11" fill="currentColor">%d°</text>'
               % (fmt(lx), fmt(ly + 4), ang))
    out.append('<text x="%d" y="%d" text-anchor="middle" font-size="12" fill="currentColor">?</text>' % qxy)
    return "".join(out)

gold_svg = (
    '<svg viewBox="0 0 260 185" role="img" '
    'aria-label="Two pie charts. Club A: 240 members with juniors sector 90 degrees, '
    'Club B: 300 members with juniors sector 60 degrees" '
    'style="max-width:260px;font-family:Inter,sans-serif">'
    + one_pie(68, "Club A: 240", 90, "#60a5fa", (55, 122))
    + one_pie(192, "Club B: 300", 60, "#60a5fa", (178, 122))
    + '<text x="130" y="178" text-anchor="middle" font-size="11" fill="currentColor">Shaded sector = juniors</text>'
    + '</svg>')
pd["guided"]["teach"]["gold"]["display"] = (
    gold_svg + "Club A has 240 members; its juniors slice is 90°. Club B has 300 members; "
    "its juniors slice is 60°. Which club has more juniors, and how many more?")

with io.open("lesson_probability-statistics-L03_diagrams.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=2)

# quick geometry echo for self-check
print("OPENER sectors (start,sweep,endpoint):")
for name, frac, start, sweep, col in seg:
    print("  ", name, start, sweep, tuple(round(v, 1) for v in polar(110, 100, 68, start + sweep)))
print("SILVER rugby 60 endpoint:", tuple(round(v, 1) for v in polar(110, 100, 68, 60)))
print("GOLD A 90 endpoint:", tuple(round(v, 1) for v in polar(68, 100, 46, 90)),
      "B 60 endpoint:", tuple(round(v, 1) for v in polar(192, 100, 46, 60)))
print("BRONZE bar heights:", [(n, v * 11) for n, v in bars])
print("written lesson_probability-statistics-L03_diagrams.json")
