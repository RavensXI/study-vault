# -*- coding: utf-8 -*-
"""Add exam-realism figures to graphs-L06 (Trigonometric Graphs).
Figures generated programmatically from each problem's own numbers.
- Opener: inline SVG sine wave (show-what-you-say on the reveal step).
- silver[2], gold[0], gold[1], gold[3]: Chart.js trig curve + reference line
  for exact-value / non-quarter-angle SOLVE problems (curve shows quadrants;
  exact angle still needs the method, intersections not marked).
Skipped: all value-recall problems (sin/cos/tan at 0/90/180/270, periods,
first asymptote, counts) where reading the printed curve would hand over the
answer without exercising the recall skill (same rule as graphs-L05 pass).
"""
import json, math, io

SRC = "_L06_diag_live.json"
OUT = "lesson_graphs-L06_diagrams.json"

pd = json.load(io.open(SRC, encoding="utf-8"))

BLUE = "#3b82f6"
AMBER = "#f59e0b"
GRID = "rgba(128,128,128,0.15)"

def curve(fn, x0=0, x1=360, step=5):
    pts = []
    for i in range(int((x1 - x0) / step) + 1):
        x = x0 + i * step
        y = fn(x)
        pts.append({"x": x, "y": y})
    return pts

def sin_pts():
    return [{"x": p["x"], "y": round(math.sin(math.radians(p["x"])), 4)} for p in curve(lambda x: 0)]

def cos_pts():
    return [{"x": p["x"], "y": round(math.cos(math.radians(p["x"])), 4)} for p in curve(lambda x: 0)]

def tan_pts():
    out = []
    for i in range(0, 361, 5):
        c = math.cos(math.radians(i))
        if abs(c) < 1e-9:
            out.append({"x": i, "y": None})
            continue
        y = math.tan(math.radians(i))
        out.append({"x": i, "y": (round(y, 4) if abs(y) <= 6 else None)})
    return out

def ref_line(k, color=AMBER):
    return {"data": [{"x": 0, "y": k}, {"x": 360, "y": k}], "type": "line",
            "fill": False, "tension": 0, "borderColor": color, "borderDash": [6, 4],
            "pointRadius": 0, "borderWidth": 2}

def wave_scales(ymin=-1.2, ymax=1.2, ystep=0.5):
    return {"scales": {
        "x": {"min": 0, "max": 360, "grid": {"color": GRID}, "ticks": {"stepSize": 90},
              "title": {"text": "x (degrees)", "display": True}},
        "y": {"min": ymin, "max": ymax, "grid": {"color": GRID}, "ticks": {"stepSize": ystep},
              "title": {"text": "y", "display": True}}}}

def wave_dataset(pts, color=BLUE):
    return {"data": pts, "type": "line", "fill": False, "tension": 0.35,
            "borderColor": color, "pointRadius": 0, "borderWidth": 2, "spanGaps": False}

def chart(datasets, scales):
    return {"type": "scatter", "data": {"datasets": datasets}, "options": scales}

# --- silver[2]: sin x = 0.5, one solution 30 given, find other (150) ---
# sine curve + line y=0.5 + a single marked point at the GIVEN solution (30, 0.5).
pt_given = {"data": [{"x": 30, "y": 0.5}], "type": "scatter", "borderColor": BLUE,
            "backgroundColor": BLUE, "pointRadius": 5, "pointBackgroundColor": BLUE, "showLine": False}
pd["problem_bank"]["silver"][2]["chart"] = chart(
    [wave_dataset(sin_pts()), ref_line(0.5), pt_given], wave_scales())

# --- gold[0]: cos x = 0.5, larger solution (300) ---
pd["problem_bank"]["gold"][0]["chart"] = chart(
    [wave_dataset(cos_pts()), ref_line(0.5)], wave_scales())

# --- gold[1]: sin x = -sqrt2/2 (=-0.7071), smaller solution (225) ---
k = round(-math.sqrt(2) / 2, 4)
pd["problem_bank"]["gold"][1]["chart"] = chart(
    [wave_dataset(sin_pts()), ref_line(k)], wave_scales())

# --- gold[3]: tan x = 1, sum of both solutions (45 + 225 = 270) ---
pd["problem_bank"]["gold"][3]["chart"] = chart(
    [wave_dataset(tan_pts()), ref_line(1)],
    wave_scales(ymin=-6, ymax=6, ystep=2))

# --- Opener: add sine-wave SVG to the final reveal say (show-what-you-say) ---
# build a smooth sine path in an SVG viewBox 0..240 x 0..120
W, H = 240, 120
mx0, mx1 = 24, 224          # x pixels for 0..360 degrees
midy = 62                    # middle line y-pixel
amp = 40                     # pixel amplitude
def sx(deg):
    return mx0 + (mx1 - mx0) * deg / 360.0
def sy(val):
    return midy - amp * val
path = "M " + " L ".join("%.1f %.1f" % (sx(d), sy(math.sin(math.radians(d))))
                          for d in range(0, 361, 5))
svg = (
    '<svg viewBox="0 0 %d %d" role="img" '
    'aria-label="The graph of y = sin x: a smooth wave rising from 0 to a peak of 1 at 90 degrees, '
    'back to 0 at 180, down to a trough of -1 at 270, and back to 0 at 360 degrees." '
    'style="max-width:280px;width:100%%;height:auto;margin:8px 0;color:currentColor">'
    '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-opacity="0.35" stroke-width="1"/>'
    '<line x1="%.1f" y1="14" x2="%.1f" y2="110" stroke="currentColor" stroke-opacity="0.35" stroke-width="1"/>'
    '<path d="%s" fill="none" stroke="%s" stroke-width="2.5"/>'
    '<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">90</text>'
    '<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">180</text>'
    '<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">270</text>'
    '<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">360</text>'
    '<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="end">1</text>'
    '<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="end">-1</text>'
    '</svg>'
) % (
    W, H,
    mx0, midy, mx1, midy,          # middle line
    mx0, mx0,                       # y-axis vertical
    path, BLUE,
    sx(90), 110.0,
    sx(180), 110.0,
    sx(270), 110.0,
    sx(360), 110.0,
    mx0 - 3, sy(1) + 3,
    mx0 - 3, sy(-1) + 3,
)

opener_steps = pd["guided"]["opener"]["steps"]
reveal = opener_steps[-1]
assert "answer" not in reveal, "last opener step should be the say-only reveal"
reveal["say"] = reveal["say"] + "<br>" + svg

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# sanity: verify plotted reference points satisfy the equations
assert abs(math.sin(math.radians(30)) - 0.5) < 1e-9
assert abs(math.cos(math.radians(60)) - 0.5) < 1e-9 and abs(math.cos(math.radians(300)) - 0.5) < 1e-9
assert abs(math.sin(math.radians(225)) - k) < 1e-3 and abs(math.sin(math.radians(315)) - k) < 1e-3
assert abs(math.tan(math.radians(45)) - 1) < 1e-9 and abs(math.tan(math.radians(225)) - 1) < 1e-9
print("Wrote", OUT, "| svg bytes:", len(svg))
