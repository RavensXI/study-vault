# -*- coding: utf-8 -*-
import json, io, math

pd = json.load(io.open("_DIAG_L07_live.json", encoding="utf-8"))

BLUE = "#3b82f6"
AMBER = "#f59e0b"

def parabola_chart():
    # base curve y = x^2, the GIVEN curve the student transforms.
    # vertex (0,0) highlighted (a known fact, not the answer).
    pts = [{"x": x, "y": x * x} for x in range(-3, 4)]
    return {
        "type": "scatter",
        "data": {"datasets": [
            {"type": "line", "data": pts, "tension": 0.4, "fill": False,
             "borderColor": BLUE, "pointRadius": 3, "pointBackgroundColor": BLUE},
            {"type": "scatter", "data": [{"x": 0, "y": 0}], "pointRadius": 5,
             "pointBackgroundColor": AMBER, "borderColor": AMBER}
        ]},
        "options": {"plugins": {"legend": {"display": False}},
            "scales": {
                "x": {"min": -4, "max": 4, "ticks": {"stepSize": 1},
                      "grid": {"color": "rgba(128,128,128,0.15)"},
                      "title": {"text": "x", "display": True}},
                "y": {"min": -1, "max": 10, "ticks": {"stepSize": 2},
                      "grid": {"color": "rgba(128,128,128,0.15)"},
                      "title": {"text": "y", "display": True}}}}
    }

def sine_chart():
    # y = sin x, the given curve to be reflected. Degrees on x-axis.
    pts = [{"x": d, "y": round(math.sin(math.radians(d)), 3)} for d in range(0, 361, 15)]
    return {
        "type": "scatter",
        "data": {"datasets": [
            {"type": "line", "data": pts, "tension": 0.4, "fill": False,
             "borderColor": BLUE, "pointRadius": 0, "borderWidth": 2.4}
        ]},
        "options": {"plugins": {"legend": {"display": False}},
            "scales": {
                "x": {"min": 0, "max": 360, "ticks": {"stepSize": 90},
                      "grid": {"color": "rgba(128,128,128,0.15)"},
                      "title": {"text": "x (degrees)", "display": True}},
                "y": {"min": -1.2, "max": 1.2, "ticks": {"stepSize": 0.5},
                      "grid": {"color": "rgba(128,128,128,0.15)"},
                      "title": {"text": "y", "display": True}}}}
    }

# Opener reflection-in-the-x-axis SVG: duck 5cm above the water line, its
# reflection the same distance below marked ? (the box answer, -5).
opener_svg = (
    '<svg viewBox="0 0 200 180" role="img" aria-label="A dot 5 cm above a '
    'horizontal water line, and its mirror reflection the same distance below '
    'the line, marked with a question mark." '
    'style="max-width:280px;width:100%;font-family:Inter,sans-serif">'
    '<rect x="20" y="90" width="160" height="70" fill="#60a5fa" fill-opacity="0.18"/>'
    '<line x1="20" y1="90" x2="180" y2="90" stroke="currentColor" stroke-width="1.4"/>'
    '<text x="176" y="86" font-size="10" fill="currentColor" text-anchor="end">water</text>'
    '<line x1="100" y1="40" x2="100" y2="140" stroke="currentColor" stroke-width="0.8" '
    'stroke-dasharray="3 3" opacity="0.6"/>'
    '<circle cx="100" cy="40" r="5" fill="#f59e0b"/>'
    '<text x="110" y="43" font-size="10" fill="currentColor">duck</text>'
    '<text x="70" y="68" font-size="10" fill="currentColor" text-anchor="end">5 cm</text>'
    '<circle cx="100" cy="140" r="5" fill="none" stroke="currentColor" stroke-width="1.2" '
    'stroke-dasharray="2 2"/>'
    '<text x="110" y="143" font-size="11" fill="currentColor">?</text>'
    '<text x="70" y="118" font-size="10" fill="currentColor" text-anchor="end">5 cm</text>'
    '</svg>'
    '<div style="margin-top:6px">Reflection in the water line</div>'
)

# ---- apply ----
gold = pd["problem_bank"]["gold"]
silver = pd["problem_bank"]["silver"]

# gold[0]: y = x^2 -> y = (x+1)^2 - 4 (vertex question)
assert "y = x^2" in gold[0]["display"], gold[0]["display"]
gold[0]["chart"] = parabola_chart()

# gold[1]: y = sin x reflected in x-axis (multiple choice)
assert "sin x" in gold[1]["display"], gold[1]["display"]
gold[1]["chart"] = sine_chart()

# silver[3]: y = x^2 -> y = (x-3)^2 + 1 (translation vector)
assert "(x - 3)^2 + 1" in silver[3]["display"], silver[3]["display"]
silver[3]["chart"] = parabola_chart()

# opener figure
pd["guided"]["opener"]["display"] = opener_svg

with io.open("lesson_graphs-L07_diagrams.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)

print("wrote lesson_graphs-L07_diagrams.json")
print("opener svg chars:", len(opener_svg))
