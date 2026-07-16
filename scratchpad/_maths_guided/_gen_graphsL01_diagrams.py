# -*- coding: utf-8 -*-
"""Diagram pass for graphs-L01 (Plotting & Reading Linear Graphs).
Adds a distance-time graph SVG to the opener display (the opener text
claims a cyclist's journey but showed no figure). Keeps the three existing
silver Chart.js grids untouched (verified correct). Programmatic, from the
opener's own numbers: 12 km per hour, straight line 0 -> 48 km over 4 hours.
"""
import json, io

LIVE = "_graphsL01_live.json"
OUT = "lesson_graphsL01_diagrams.json"

# --- geometry of the plot (viewBox 262 x 192) ---
X0, Y0 = 42, 158          # pixel origin (0 h, 0 km)
DX = 50                    # pixels per hour
KM_PER_PX = 146.0 / 48.0   # 48 km spans 146 px upward

def px(h):
    return X0 + h * DX

def py(v):
    return Y0 - v * KM_PER_PX

# journey vertices: (hour, km)
pts = [(0, 0), (1, 12), (2, 24), (3, 36), (4, 48)]

def r1(n):
    return round(n, 1)

# polyline (straight line through the vertices)
line = " ".join("%s,%s" % (r1(px(h)), r1(py(v))) for h, v in pts)

parts = []
parts.append(
    '<svg viewBox="0 0 262 192" role="img" '
    'aria-label="Distance-time graph of a cyclist riding 12 km each hour: '
    'a straight line from the origin reaching 48 km after 4 hours" '
    'style="max-width:280px;width:100%;height:auto;font-family:Inter,sans-serif">'
)
# faint horizontal gridlines at 12, 24, 36, 48 km
for v in (12, 24, 36, 48):
    parts.append(
        '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" '
        'stroke-opacity="0.12" stroke-width="1"/>' % (X0, r1(py(v)), px(4), r1(py(v)))
    )
# axes
parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1.5"/>'
             % (X0, r1(py(48)), X0, Y0))           # y-axis
parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1.5"/>'
             % (X0, Y0, px(4) + 6, Y0))             # x-axis
# the journey line
parts.append('<polyline points="%s" fill="none" stroke="#3b82f6" stroke-width="2.5"/>' % line)
# point markers
for h, v in pts:
    parts.append('<circle cx="%s" cy="%s" r="3.2" fill="#3b82f6"/>' % (r1(px(h)), r1(py(v))))
# x tick labels (hours)
for h in range(5):
    parts.append('<text x="%s" y="172" text-anchor="middle" font-size="10" '
                 'fill="currentColor">%d</text>' % (r1(px(h)), h))
# y tick labels (km)
for v in (0, 12, 24, 36, 48):
    parts.append('<text x="37" y="%s" text-anchor="end" font-size="10" '
                 'fill="currentColor">%d</text>' % (r1(py(v) + 3.5), v))
# axis titles
parts.append('<text x="%s" y="189" text-anchor="middle" font-size="10.5" '
             'fill="currentColor">Time (hours)</text>' % r1((X0 + px(4)) / 2))
parts.append('<text x="12" y="%s" text-anchor="middle" font-size="10.5" '
             'fill="currentColor" transform="rotate(-90 12 %s)">Distance (km)</text>'
             % (r1((py(0) + py(48)) / 2), r1((py(0) + py(48)) / 2)))
parts.append('</svg>')
svg = "".join(parts)

d = json.load(io.open(LIVE, encoding="utf-8"))
pd = d[0]["practice_data"]

old_display = pd["guided"]["opener"]["display"]
# figure first, then the original scene text, per SPEC (SVG at START of display)
pd["guided"]["opener"]["display"] = svg + "<br>" + old_display

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("SVG length:", len(svg))
print("wrote", OUT)
