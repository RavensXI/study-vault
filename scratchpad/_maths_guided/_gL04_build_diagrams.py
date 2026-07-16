# -*- coding: utf-8 -*-
"""Diagram pass for graphs-L04 (Real-Life Graphs). Adds Chart.js configs to
bank problems that describe a graph, and inline SVG to teach-walk displays
that claim 'a graph shows'. Purely additive: no solutions/steps touched."""
import json, io

SRC = "_gL04_live.json"
OUT = "lesson_gL04_diagrams.json"

pd = json.load(io.open(SRC, encoding="utf-8"))
pb = pd["problem_bank"]

added = []

# ---------- Chart.js builder (mirrors the lesson's existing chart style) ----------
def chart(labels, data, xtitle, ytitle, xstep, ystep, color, fill=False, bg=None):
    ds = {
        "data": data, "fill": fill, "tension": 0,
        "borderColor": color, "pointRadius": 4, "pointBackgroundColor": color,
    }
    if fill and bg:
        ds["backgroundColor"] = bg
    return {
        "type": "line",
        "data": {"labels": labels, "datasets": [ds]},
        "options": {"scales": {
            "x": {"grid": {"color": "rgba(0,0,0,0.05)"}, "ticks": {"stepSize": xstep},
                  "title": {"text": xtitle, "display": True}},
            "y": {"grid": {"color": "rgba(0,0,0,0.08)"}, "ticks": {"stepSize": ystep},
                  "title": {"text": ytitle, "display": True}, "beginAtZero": True},
        }},
    }

# tier, index -> chart. Only for problems whose text describes/implies a graph.
CHARTS = {
    ("gold", 0): chart([0,5,10,15], [0,10,10,10], "Time (seconds)", "Speed (m/s)", 5, 2,
                       "#dc2626", True, "rgba(220,38,38,0.15)"),
    ("gold", 1): chart([0,3,6,9,12], [30,22.5,15,7.5,0], "Time (seconds)", "Speed (m/s)", 3, 5,
                       "#8b5cf6", True, "rgba(139,92,246,0.15)"),
    ("gold", 3): chart([0,2,4,6,8], [5,10,15,20,25], "Time (seconds)", "Speed (m/s)", 2, 5, "#059669"),
    ("gold", 4): chart([0,2,4,6,8,10,12,14], [0,10,20,20,20,20,10,0], "Time (seconds)", "Speed (m/s)", 2, 5,
                       "#dc2626", True, "rgba(220,38,38,0.15)"),
    ("bronze", 4): chart([0,1,2,3,4], [0,5,10,15,20], "Time (hours)", "Distance (km)", 1, 5, "#06b6d4"),
    ("silver", 1): chart([0,2,4,6,8,10], [0,4,8,12,16,20], "Time (seconds)", "Speed (m/s)", 2, 5,
                        "#8b5cf6", True, "rgba(139,92,246,0.15)"),
    ("silver", 2): chart([0,0.5,1,1.5,2,2.5], [0,30,60,60,80,100], "Time (hours)", "Distance (km)", 0.5, 20, "#059669"),
    ("silver", 3): chart([0,1,2,3,4,5,6], [0,5,10,15,20,25,30], "Time (seconds)", "Speed (m/s)", 1, 5, "#dc2626"),
}

for (tier, idx), cfg in CHARTS.items():
    prob = pb[tier][idx]
    if "chart" in prob:
        continue  # never overwrite an existing figure
    prob["chart"] = cfg
    added.append({"tier": tier, "index": idx, "kind": "chart",
                  "what": "%s speed/distance-time graph matching the problem numbers" % tier})

# ---------- inline SVG line-graph generator (programmatic from points) ----------
def line_svg(points, xlabel, ylabel, aria, xticks, yticks, fill=False):
    # plot box
    L, R, T, B = 44, 250, 14, 140
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    xmax = max(xs); ymax = max(ys)
    def px(x): return round(L + (x / xmax) * (R - L), 1)
    def py(y): return round(B - (y / ymax) * (B - T), 1)
    parts = ['<svg viewBox="0 0 262 168" role="img" aria-label="%s" '
             'font-family="Inter, sans-serif">' % aria]
    # axes
    parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1"/>' % (L, T, L, B))
    parts.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1"/>' % (L, B, R, B))
    poly = " ".join("%s,%s" % (px(x), py(y)) for x, y in points)
    if fill:
        area = "%s,%s %s %s,%s" % (px(points[0][0]), B, poly, px(points[-1][0]), B)
        parts.append('<polygon points="%s" fill="#60a5fa" fill-opacity="0.3"/>' % area)
    parts.append('<polyline points="%s" fill="none" stroke="currentColor" stroke-width="2"/>' % poly)
    for x, y in points:
        parts.append('<circle cx="%s" cy="%s" r="2.5" fill="currentColor"/>' % (px(x), py(y)))
    for x, t in xticks:
        parts.append('<text x="%s" y="%s" font-size="10" fill="currentColor" text-anchor="middle">%s</text>'
                     % (px(x), B + 13, t))
    for y, t in yticks:
        parts.append('<text x="%s" y="%s" font-size="10" fill="currentColor" text-anchor="end">%s</text>'
                     % (L - 5, py(y) + 3, t))
    parts.append('<text x="%s" y="164" font-size="10" fill="currentColor" text-anchor="middle">%s</text>'
                 % ((L + R) / 2, xlabel))
    parts.append('<text x="11" y="%s" font-size="10" fill="currentColor" text-anchor="middle" '
                 'transform="rotate(-90 11 %s)">%s</text>' % ((T + B) / 2, (T + B) / 2, ylabel))
    parts.append('</svg>')
    return "".join(parts)

teach = pd["guided"]["teach"]

# teach.bronze: distance-time, 12 km in 3 h then rest (flat)
svg_b = line_svg([(0,0),(3,12),(5,12)], "Time (hours)", "Distance (km)",
    "Distance-time graph rising steadily to 12 km at 3 hours, then flat while the hiker rests.",
    [(3,"3"),(5,"5")], [(12,"12")], fill=False)
teach["bronze"]["display"] = svg_b + teach["bronze"]["display"]
added.append({"tier": "teach.bronze", "index": None, "kind": "svg",
              "what": "distance-time graph: 12 km over 3 h then a flat rest"})

# teach.silver: speed-time, 12 m/s in 4 s then hold 12 for 6 s (to 10 s)
svg_s = line_svg([(0,0),(4,12),(10,12)], "Time (seconds)", "Speed (m/s)",
    "Speed-time graph rising to 12 m/s at 4 seconds then holding 12 m/s to 10 seconds.",
    [(4,"4"),(10,"10")], [(12,"12")], fill=True)
teach["silver"]["display"] = svg_s + teach["silver"]["display"]
added.append({"tier": "teach.silver", "index": None, "kind": "svg",
              "what": "speed-time graph: triangle to 12 m/s at 4 s, rectangle to 10 s"})

# teach.gold: speed-time trapezium 0->20 in 4 s, hold to 14 s, down to 0 at 20 s
svg_g = line_svg([(0,0),(4,20),(14,20),(20,0)], "Time (seconds)", "Speed (m/s)",
    "Speed-time graph: up to 20 m/s at 4 s, holding to 14 s, then down to 0 at 20 s.",
    [(4,"4"),(14,"14"),(20,"20")], [(20,"20")], fill=True)
teach["gold"]["display"] = svg_g + teach["gold"]["display"]
added.append({"tier": "teach.gold", "index": None, "kind": "svg",
              "what": "speed-time trapezium: 0-20 in 4 s, hold to 14 s, 0 at 20 s"})

# ---------- qualitative SVG for the two multiple-choice graph problems ----------
def mc_svg(aria, inner):
    L, R, T, B = 40, 250, 14, 140
    head = ('<svg viewBox="0 0 262 168" role="img" aria-label="%s" font-family="Inter, sans-serif">'
            '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1"/>'
            '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1"/>'
            % (aria, L, T, L, B, L, B, R, B))
    return head + inner + '</svg>'

# bronze[5]: rise (positive gradient) then horizontal. No numbers in the problem.
b5 = pb["bronze"][5]
if "chart" not in b5 and "<svg" not in (b5.get("display") or ""):
    inner = ('<polyline points="40,140 140,44 250,44" fill="none" stroke="currentColor" stroke-width="2"/>'
             '<circle cx="140" cy="44" r="2.5" fill="currentColor"/>'
             '<text x="90" y="164" font-size="10" fill="currentColor" text-anchor="middle">Time</text>'
             '<text x="11" y="77" font-size="10" fill="currentColor" text-anchor="middle" '
             'transform="rotate(-90 11 77)">Speed</text>')
    b5["display"] = mc_svg("Speed-time graph: a straight line sloping upward, then becoming horizontal.", inner) + b5["display"]
    added.append({"tier": "bronze", "index": 5, "kind": "svg",
                  "what": "qualitative speed-time graph: sloping up then horizontal"})

# silver[6]: distance-time, Section A gradient 15, Section B gradient 25 (B steeper).
s6 = pb["silver"][6]
if "chart" not in s6 and "<svg" not in (s6.get("display") or ""):
    # A: (40,140)->(150,95) shallow; B: (150,95)->(250,20) steeper
    inner = ('<polyline points="40,140 150,95 250,20" fill="none" stroke="currentColor" stroke-width="2"/>'
             '<circle cx="150" cy="95" r="2.5" fill="currentColor"/>'
             '<text x="92" y="108" font-size="11" fill="currentColor" text-anchor="middle">A</text>'
             '<text x="204" y="52" font-size="11" fill="currentColor" text-anchor="middle">B</text>'
             '<text x="145" y="164" font-size="10" fill="currentColor" text-anchor="middle">Time</text>'
             '<text x="11" y="77" font-size="10" fill="currentColor" text-anchor="middle" '
             'transform="rotate(-90 11 77)">Distance</text>')
    s6["display"] = mc_svg("Distance-time graph: section A rising gently, then section B rising more steeply.", inner) + s6["display"]
    added.append({"tier": "silver", "index": 6, "kind": "svg",
                  "what": "distance-time graph: gentle section A then steeper section B"})

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("figures added:", len(added))
for a in added:
    print(" ", a["tier"], a["index"], a["kind"], "-", a["what"])

# save changes summary
changes = {
    "key": "graphs-L04",
    "figures_added": added,
    "opener_touched": False,
    "notes": "Pure additive diagram pass on Real-Life Graphs. 8 Chart.js line graphs on "
             "bank problems that describe a distance/speed-time graph; 3 inline SVG graphs on the "
             "teach-walk displays (which claim 'a graph shows'); 2 qualitative SVGs on the two "
             "multiple-choice graph problems. Existing charts (gold[2], bronze[0-2], silver[0], "
             "silver[4]) verified correct and left byte-for-byte. No solutions, steps, hints or "
             "misconceptions changed; all 21 stored answers were fresh-solved and already correct."
}
json.dump(changes, io.open("changes_gL04_diagrams.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote changes_gL04_diagrams.json")
