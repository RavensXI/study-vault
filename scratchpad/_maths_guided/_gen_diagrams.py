# -*- coding: utf-8 -*-
"""Generate exam-realism SVG figures for probability-statistics-L01 from each
problem's own numbers, and prepend them to the relevant displays."""
import json, io, math

SRC = "_DIAG_L01_live.json"
OUT = "lesson_probability-statistics-L01_diagrams.json"

def f(x):
    # compact float
    s = ("%.2f" % x).rstrip("0").rstrip(".")
    return s if s else "0"

def pt(cx, cy, r, deg):
    # angle from top (12 o'clock), clockwise
    a = math.radians(deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)

def sector(cx, cy, r, a0, a1, fill):
    x0, y0 = pt(cx, cy, r, a0)
    x1, y1 = pt(cx, cy, r, a1)
    large = 1 if (a1 - a0) > 180 else 0
    return ('<path d="M%s %s L%s %s A%s %s 0 %d 1 %s %s Z" fill="%s" '
            'fill-opacity="0.3" stroke="currentColor" stroke-width="1.3"/>'
            % (f(cx), f(cy), f(x0), f(y0), f(r), f(r), large, f(x1), f(y1), fill))

def spinner(sections, aria, radius=62):
    # sections: list of (label, sweep_degrees, fill)
    cx = cy = 74
    parts = []
    a = 0.0
    fills = ["#60a5fa", "#f59e0b", "#34d399", "#f87171", "#a78bfa"]
    for i, (label, sweep, fill) in enumerate(sections):
        a1 = a + sweep
        parts.append(sector(cx, cy, radius, a, a1, fill))
        mid = (a + a1) / 2
        lx, ly = pt(cx, cy, radius * 0.58, mid)
        parts.append('<text x="%s" y="%s" font-family="Inter,sans-serif" '
                     'font-size="11" text-anchor="middle" dominant-baseline="middle" '
                     'fill="currentColor">%s</text>' % (f(lx), f(ly), label))
        a = a1
    # pointer arrow at top pointing to centre
    parts.append('<path d="M74 4 L69 18 L79 18 Z" fill="currentColor"/>')
    parts.append('<circle cx="74" cy="74" r="3" fill="currentColor"/>')
    body = "".join(parts)
    return ('<svg viewBox="0 0 148 152" role="img" aria-label="%s" '
            'style="display:block;margin:0 auto 0.4rem;max-width:170px;width:100%%">'
            '%s</svg>' % (aria, body))

def dice_grid(aria):
    cell = 26
    ox = oy = 30
    gx0, gy0 = ox, oy
    gx1, gy1 = ox + 6 * cell, oy + 6 * cell
    lines = []
    for k in range(7):
        x = ox + k * cell
        lines.append("M%d %d V%d" % (x, gy0, gy1))
        y = oy + k * cell
        lines.append("M%d %d H%d" % (gx0, y, gx1))
    grid = '<path d="%s" fill="none" stroke="currentColor" stroke-width="0.8"/>' % " ".join(lines)
    txt = []
    txt.append('<text x="%d" y="%d">+</text>' % (ox - cell // 2, oy - cell // 2))
    for d in range(1, 7):
        txt.append('<text x="%d" y="%d">%d</text>' % (ox + (d - 1) * cell + cell // 2, oy - cell // 2, d))
        txt.append('<text x="%d" y="%d">%d</text>' % (ox - cell // 2, oy + (d - 1) * cell + cell // 2, d))
    for r in range(6):      # die 2 (row)
        for c in range(6):  # die 1 (col)
            s = (r + 1) + (c + 1)
            txt.append('<text x="%d" y="%d">%d</text>'
                       % (ox + c * cell + cell // 2, oy + r * cell + cell // 2, s))
    group = ('<g font-family="Inter,sans-serif" font-size="10" text-anchor="middle" '
             'dominant-baseline="middle" fill="currentColor">%s</g>' % "".join(txt))
    W = ox + 6 * cell + 4
    H = oy + 6 * cell + 4
    return ('<svg viewBox="0 0 %d %d" role="img" aria-label="%s" '
            'style="display:block;margin:0 auto 0.4rem;max-width:230px;width:100%%">'
            '%s%s</svg>' % (W, H, aria, grid, group))

def tree(p1_top, p1_bot, s2_top, s2_bot, ends, aria):
    # first-stage labels p1_top/p1_bot (strings), second-stage labels lists
    # s2_top=[topR,topB], s2_bot=[botR,botB]; ends=[e1..e4] endpoint labels
    rootx, rooty = 16, 84
    n1x = 96
    ny = [40, 128]      # first-stage node y (top, bottom)
    n2x = 176
    ey = [22, 66, 102, 146]  # endpoint y
    parts = []
    def line(x0, y0, x1, y1):
        return ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" '
                'stroke-width="1.2"/>' % (x0, y0, x1, y1))
    def blab(x0, y0, x1, y1, txt):
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - 4
        return ('<text x="%s" y="%s" font-family="Inter,sans-serif" font-size="10" '
                'text-anchor="middle" fill="currentColor">%s</text>' % (f(mx), f(my), txt))
    # stage 1
    parts.append(line(rootx, rooty, n1x, ny[0]))
    parts.append(line(rootx, rooty, n1x, ny[1]))
    parts.append(blab(rootx, rooty, n1x, ny[0], p1_top))
    parts.append(blab(rootx, rooty, n1x, ny[1], p1_bot))
    # node letters at stage1
    parts.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" '
                 'text-anchor="middle" fill="currentColor">R</text>' % (n1x + 6, ny[0] + 4))
    parts.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" '
                 'text-anchor="middle" fill="currentColor">B</text>' % (n1x + 6, ny[1] + 4))
    # stage 2 from top node
    parts.append(line(n1x, ny[0], n2x, ey[0]))
    parts.append(line(n1x, ny[0], n2x, ey[1]))
    parts.append(blab(n1x, ny[0], n2x, ey[0], s2_top[0]))
    parts.append(blab(n1x, ny[0], n2x, ey[1], s2_top[1]))
    # stage 2 from bottom node
    parts.append(line(n1x, ny[1], n2x, ey[2]))
    parts.append(line(n1x, ny[1], n2x, ey[3]))
    parts.append(blab(n1x, ny[1], n2x, ey[2], s2_bot[0]))
    parts.append(blab(n1x, ny[1], n2x, ey[3], s2_bot[1]))
    # endpoint labels
    for i, e in enumerate(ends):
        parts.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" '
                     'text-anchor="start" dominant-baseline="middle" fill="currentColor">%s</text>'
                     % (n2x + 5, ey[i], e))
    body = "".join(parts)
    return ('<svg viewBox="0 0 210 168" role="img" aria-label="%s" '
            'style="display:block;margin:0 auto 0.4rem;max-width:250px;width:100%%">'
            '%s</svg>' % (aria, body))

def sweets_bag(aria):
    # 3 red + 1 green sweets inside a bag outline
    parts = []
    # bag
    parts.append('<path d="M40 30 L104 30 L114 118 Q72 130 30 118 Z" fill="none" '
                 'stroke="currentColor" stroke-width="1.4"/>')
    parts.append('<path d="M40 30 Q72 20 104 30" fill="none" stroke="currentColor" '
                 'stroke-width="1.4"/>')
    reds = [(56, 62), (86, 66), (68, 92)]
    for (x, y) in reds:
        parts.append('<circle cx="%d" cy="%d" r="11" fill="#f87171" fill-opacity="0.35" '
                     'stroke="currentColor" stroke-width="1.1"/>' % (x, y))
    parts.append('<circle cx="46" cy="92" r="11" fill="#34d399" fill-opacity="0.35" '
                 'stroke="currentColor" stroke-width="1.1"/>')
    body = "".join(parts)
    return ('<svg viewBox="20 12 108 126" role="img" aria-label="%s" '
            'style="display:block;margin:0 auto 0.4rem;max-width:150px;width:100%%">'
            '%s</svg>' % (aria, body))


def main():
    pd = json.load(io.open(SRC, encoding="utf-8"))
    added = []

    # --- opener: bag of 3 red + 1 green sweets ---
    op = pd["guided"]["opener"]
    svg = sweets_bag("A bag containing 3 red sweets and 1 green sweet")
    op["display"] = svg + op["display"]
    added.append({"tier": "opener", "index": None, "kind": "svg",
                  "what": "bag showing 3 red + 1 green sweets"})

    pb = pd["problem_bank"]

    # --- bronze[0]: spinner 1-5 equal sections ---
    secs = [(str(n), 72.0, None) for n in range(1, 6)]
    fills = ["#60a5fa", "#f59e0b", "#34d399", "#f87171", "#a78bfa"]
    secs = [(str(n + 1), 72.0, fills[n]) for n in range(5)]
    svg = spinner(secs, "A five-section spinner numbered 1 to 5, equally likely")
    pb["bronze"][0]["display"] = svg + pb["bronze"][0]["display"]
    added.append({"tier": "bronze", "index": 0, "kind": "svg",
                  "what": "spinner with five equal sections 1 to 5"})

    # --- bronze[7]: spinner A 0.45, B 0.35, C ? ---
    secs = [("A 0.45", 0.45 * 360, "#60a5fa"),
            ("B 0.35", 0.35 * 360, "#f59e0b"),
            ("C ?", 0.20 * 360, "#34d399")]
    svg = spinner(secs, "A three-section spinner: A probability 0.45, B probability 0.35, C unknown")
    pb["bronze"][7]["display"] = svg + pb["bronze"][7]["display"]
    added.append({"tier": "bronze", "index": 7, "kind": "svg",
                  "what": "spinner A 0.45, B 0.35, C marked ?"})

    # --- gold[2]: two-dice sample space grid ---
    svg = dice_grid("Sample space grid of the totals when two dice are rolled")
    pb["gold"][2]["display"] = svg + pb["gold"][2]["display"]
    added.append({"tier": "gold", "index": 2, "kind": "svg",
                  "what": "6 by 6 sample space grid of two-dice totals"})

    # --- silver[0]: tree, WITH replacement, 3 red 7 blue ---
    svg = tree("3/10", "7/10", ["3/10", "7/10"], ["3/10", "7/10"],
               ["RR", "RB", "BR", "BB"],
               "Two-stage probability tree, with replacement, bag of 3 red and 7 blue")
    pb["silver"][0]["display"] = svg + pb["silver"][0]["display"]
    added.append({"tier": "silver", "index": 0, "kind": "svg",
                  "what": "two-stage tree with replacement, branches 3/10 and 7/10"})

    # --- silver[2]: tree, WITHOUT replacement, 5 red 3 blue, 2nd stage ? ---
    svg = tree("5/8", "3/8", ["?", "?"], ["?", "?"],
               ["RR", "RB", "BR", "BB"],
               "Two-stage probability tree, without replacement, bag of 5 red and 3 blue, second stage unknown")
    pb["silver"][2]["display"] = svg + pb["silver"][2]["display"]
    added.append({"tier": "silver", "index": 2, "kind": "svg",
                  "what": "two-stage tree without replacement, stage 1 = 5/8, 3/8; stage 2 marked ?"})

    # --- silver[5]: tree, WITHOUT replacement, 6 red 4 blue, 2nd stage ? ---
    svg = tree("6/10", "4/10", ["?", "?"], ["?", "?"],
               ["RR", "RB", "BR", "BB"],
               "Two-stage probability tree, without replacement, bag of 6 red and 4 blue, second stage unknown")
    pb["silver"][5]["display"] = svg + pb["silver"][5]["display"]
    added.append({"tier": "silver", "index": 5, "kind": "svg",
                  "what": "two-stage tree without replacement, stage 1 = 6/10, 4/10; stage 2 marked ?"})

    # --- silver[6]: spinner A 0.5, B 0.3, C 0.2 ---
    secs = [("A 0.5", 0.5 * 360, "#60a5fa"),
            ("B 0.3", 0.3 * 360, "#f59e0b"),
            ("C 0.2", 0.2 * 360, "#34d399")]
    svg = spinner(secs, "A three-section spinner: A probability 0.5, B probability 0.3, C probability 0.2")
    pb["silver"][6]["display"] = svg + pb["silver"][6]["display"]
    added.append({"tier": "silver", "index": 6, "kind": "svg",
                  "what": "spinner A 0.5, B 0.3, C 0.2"})

    json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("wrote", OUT, "figures:", len(added))
    for a in added:
        print(" ", a["tier"], a["index"], "-", a["what"])

if __name__ == "__main__":
    main()
