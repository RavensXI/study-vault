# -*- coding: utf-8 -*-
"""Generate exam-realism SVG tables for probability-statistics-L04 and inject
them at the START of each relevant display. Frequency / grouped / cumulative
tables only, matching each problem's own numbers exactly."""
import json, io

SRC = "_diag_L04_live.json"
OUT = "lesson_probability-statistics-L04_diagrams.json"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def table_svg(row1_label, cells1, row2_label, cells2, aria):
    """Two-row table. cells1 = header row (values/classes), cells2 = frequencies."""
    n = len(cells1)
    assert n == len(cells2)
    labelW = 84
    colW = 43
    rowH = 26
    W = labelW + n * colW
    H = 2 * rowH
    parts = []
    parts.append(
        '<svg viewBox="0 0 %d %d" role="img" aria-label="%s" '
        'style="max-width:280px;width:100%%;height:auto">'
        % (W, H, esc(aria)))
    parts.append('<g font-family="Inter, sans-serif" font-size="11" '
                 'fill="currentColor" text-anchor="middle">')
    # soft shade on the left label column
    parts.append('<rect x="0" y="0" width="%d" height="%d" fill="#60a5fa" fill-opacity="0.18"/>' % (labelW, H))
    # grid lines
    xs = [0, labelW] + [labelW + (i + 1) * colW for i in range(n)]
    for x in xs:
        parts.append('<line x1="%d" y1="0" x2="%d" y2="%d" stroke="currentColor" stroke-width="1"/>' % (x, x, H))
    for y in (0, rowH, 2 * rowH):
        parts.append('<line x1="0" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1"/>' % (y, W, y))
    # row labels
    parts.append('<text x="%d" y="%d" font-weight="600" dominant-baseline="central">%s</text>'
                 % (labelW // 2, rowH // 2, esc(row1_label)))
    parts.append('<text x="%d" y="%d" font-weight="600" dominant-baseline="central">%s</text>'
                 % (labelW // 2, rowH + rowH // 2, esc(row2_label)))
    # cells
    for i in range(n):
        cx = labelW + i * colW + colW // 2
        parts.append('<text x="%d" y="%d" dominant-baseline="central">%s</text>'
                     % (cx, rowH // 2, esc(cells1[i])))
        parts.append('<text x="%d" y="%d" dominant-baseline="central">%s</text>'
                     % (cx, rowH + rowH // 2, esc(cells2[i])))
    parts.append('</g></svg>')
    return "".join(parts)


pd = json.load(io.open(SRC, encoding="utf-8"))
added = []


def prepend(display, svg):
    return svg + display


# --- silver bank ---
silver = pd["problem_bank"]["silver"]

# silver[0] frequency table
svg = table_svg("x", ["1", "2", "3", "4"], "Frequency", ["4", "7", "5", "4"],
                "Frequency table. Values 1, 2, 3, 4 with frequencies 4, 7, 5, 4.")
silver[0]["display"] = prepend(silver[0]["display"], svg)
added.append({"tier": "silver", "index": 0, "kind": "svg", "what": "frequency table x=1-4, f=4,7,5,4"})

# silver[2] grouped data
svg = table_svg("Class", ["0-10", "10-20", "20-30"], "Frequency", ["5", "12", "8"],
                "Grouped frequency table. Classes 0 to 10, 10 to 20, 20 to 30 with frequencies 5, 12, 8.")
silver[2]["display"] = prepend(silver[2]["display"], svg)
added.append({"tier": "silver", "index": 2, "kind": "svg", "what": "grouped table 0-10,10-20,20-30 f=5,12,8"})

# silver[5] modal class grouped
svg = table_svg("Class", ["0-5", "5-10", "10-15", "15-20"], "Frequency", ["3", "8", "12", "7"],
                "Grouped frequency table. Classes 0 to 5, 5 to 10, 10 to 15, 15 to 20 with frequencies 3, 8, 12, 7.")
silver[5]["display"] = prepend(silver[5]["display"], svg)
added.append({"tier": "silver", "index": 5, "kind": "svg", "what": "grouped table 0-5..15-20 f=3,8,12,7 (modal class)"})

# silver[6] cumulative frequency
svg = table_svg("Value", ["<15", "<20", "<25", "<30"], "Cum. freq", ["8", "22", "38", "50"],
                "Cumulative frequency table. Values under 15, 20, 25, 30 with cumulative frequencies 8, 22, 38, 50.")
silver[6]["display"] = prepend(silver[6]["display"], svg)
added.append({"tier": "silver", "index": 6, "kind": "svg", "what": "cumulative frequency table <15..<30 = 8,22,38,50"})

# --- gold bank ---
gold = pd["problem_bank"]["gold"]
# gold[3] grouped data
svg = table_svg("Class", ["0-10", "10-30", "30-50"], "Frequency", ["6", "14", "10"],
                "Grouped frequency table. Classes 0 to 10, 10 to 30, 30 to 50 with frequencies 6, 14, 10.")
gold[3]["display"] = prepend(gold[3]["display"], svg)
added.append({"tier": "gold", "index": 3, "kind": "svg", "what": "grouped table 0-10,10-30,30-50 f=6,14,10"})

# --- teach walks ---
teach = pd["guided"]["teach"]
# silver teach: dice frequency table
svg = table_svg("Score", ["1", "2", "3"], "Frequency", ["2", "3", "5"],
                "Frequency table. Dice scores 1, 2, 3 with frequencies 2, 3, 5.")
teach["silver"]["display"] = prepend(teach["silver"]["display"], svg)
added.append({"tier": "teach.silver", "index": -1, "kind": "svg", "what": "dice frequency table 1,2,3 f=2,3,5"})

# gold teach: grouped data
svg = table_svg("Class", ["0-10", "10-20", "20-30"], "Frequency", ["3", "5", "2"],
                "Grouped frequency table. Classes 0 to 10, 10 to 20, 20 to 30 with frequencies 3, 5, 2.")
teach["gold"]["display"] = prepend(teach["gold"]["display"], svg)
added.append({"tier": "teach.gold", "index": -1, "kind": "svg", "what": "grouped table 0-10,10-20,20-30 f=3,5,2"})

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", OUT, "with", len(added), "figures")
for a in added:
    print(" ", a["tier"], a["index"], a["what"])
