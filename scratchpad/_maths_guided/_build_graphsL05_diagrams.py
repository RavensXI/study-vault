# -*- coding: utf-8 -*-
import json

SRC = "_live_graphs_l05.json"
OUT = "lesson_graphs-L05_diagrams.json"

pd = json.load(open(SRC, encoding="utf-8"))
pb = pd["problem_bank"]

BLUE = "#3b82f6"
AMBER = "#f59e0b"


def ds(points, colour, tension=0.35, width=2):
    return {
        "type": "line",
        "data": [{"x": round(x, 4), "y": round(y, 4)} for x, y in points],
        "tension": tension,
        "fill": False,
        "borderColor": colour,
        "borderWidth": width,
        "pointRadius": 0,
    }


def chart(datasets, xmin, xmax, ymin, ymax, xstep=1, ystep=1):
    return {
        "type": "scatter",
        "data": {"datasets": datasets},
        "options": {
            "plugins": {"legend": {"display": False}},
            "scales": {
                "x": {"min": xmin, "max": xmax,
                      "ticks": {"stepSize": xstep},
                      "grid": {"color": "rgba(128,128,128,0.15)"},
                      "title": {"text": "x", "display": True}},
                "y": {"min": ymin, "max": ymax,
                      "ticks": {"stepSize": ystep},
                      "grid": {"color": "rgba(128,128,128,0.15)"},
                      "title": {"text": "y", "display": True}},
            },
        },
    }


def recip(coeff, xs):
    return [(x, coeff / x) for x in xs]


def frange(a, b, step):
    out = []
    x = a
    while x <= b + 1e-9:
        out.append(round(x, 4))
        x += step
    return out


# reciprocal x-samples (avoid |x|<0.25 to keep the spike bounded)
neg_x = [-5, -4, -3, -2, -1.5, -1, -0.75, -0.5, -0.35, -0.25]
pos_x = [0.25, 0.35, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5]

# bronze[3]  y = 1/x  (asymptotes x=0 and y=0)
pb["bronze"][3]["chart"] = chart(
    [ds(recip(1, neg_x), BLUE), ds(recip(1, pos_x), BLUE)],
    -5, 5, -5, 5)

# bronze[5]  y = x^3  (gradient sign at x=1)
cub = [(x, x ** 3) for x in frange(-2, 2, 0.2)]
pb["bronze"][5]["chart"] = chart([ds(cub, BLUE)], -2, 2, -8, 8, 1, 2)

# bronze[6]  y = 1/x  (behaviour as x -> large)
neg_wide = [-10, -8, -6, -4, -3, -2, -1, -0.5, -0.35, -0.25]
pos_wide = [0.25, 0.35, 0.5, 1, 2, 3, 4, 6, 8, 10]
pb["bronze"][6]["chart"] = chart(
    [ds(recip(1, neg_wide), BLUE), ds(recip(1, pos_wide), BLUE)],
    -10, 10, -5, 5, 2, 1)

# silver[4]  y = -1/x  (which quadrants: 2nd and 4th)
pb["silver"][4]["chart"] = chart(
    [ds(recip(-1, neg_x), BLUE), ds(recip(-1, pos_x), BLUE)],
    -5, 5, -5, 5)

# silver[6]  y = x^3 and y = -x^3  (reflection in x-axis)
cub2 = [(x, x ** 3) for x in frange(-2, 2, 0.2)]
ncub2 = [(x, -(x ** 3)) for x in frange(-2, 2, 0.2)]
pb["silver"][6]["chart"] = chart(
    [ds(cub2, BLUE), ds(ncub2, AMBER)], -2, 2, -8, 8, 1, 2)

# gold[4]  y = 1/x and y = 4x  (intersection in 1st quadrant, x=0.5)
line = [(-1.75, 4 * -1.75), (1.75, 4 * 1.75)]
neg_g = [-3, -2, -1.5, -1, -0.75, -0.5, -0.35, -0.25]
pos_g = [0.25, 0.35, 0.5, 0.75, 1, 1.5, 2, 3]
pb["gold"][4]["chart"] = chart(
    [ds(recip(1, neg_g), BLUE), ds(recip(1, pos_g), BLUE),
     ds(line, AMBER, tension=0, width=2)],
    -3, 3, -8, 8, 1, 2)

json.dump(pd, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

# sanity: recompute a few points against the equations
checks = [
    ("bronze3 1/x @2", 1 / 2, 0.5),
    ("bronze5 x^3 @1", 1 ** 3, 1),
    ("silver4 -1/x @-2 -> +", -1 / -2, 0.5),
    ("silver6 -x^3 @2", -(2 ** 3), -8),
    ("gold4 4x @0.5", 4 * 0.5, 2.0),
    ("gold4 1/x @0.5", 1 / 0.5, 2.0),
]
for name, got, exp in checks:
    assert abs(got - exp) < 1e-9, (name, got, exp)
print("charts added to 6 problems; point checks OK ->", OUT)
