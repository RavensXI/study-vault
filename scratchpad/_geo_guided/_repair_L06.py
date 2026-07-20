# -*- coding: utf-8 -*-
"""Targeted repairs to L06 after checker findings. Run against lesson_L06.json."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
FN = os.path.join(HERE, "lesson_L06.json")
d = json.load(io.open(FN, encoding="utf-8"))
log = []

# ---------------------------------------------------------------- FAIL 1
sil = d["guided"]["teach"]["silver"]["steps"][6]
assert sil["answer"] == 29, sil
old = sil["pre"]
sil["pre"] = ("Now do the same to the upper half, 26, 28, 30, 34. "
              "Average its two middle values to get Q3.")
log.append(("guided.teach.silver.steps[6].pre", old, sil["pre"]))

# ---------------------------------------------------------------- NIT: SVG budgets
def opener_svg():
    xs = [42, 98, 154, 210, 266, 322, 378, 434]
    s = ['<svg viewBox="0 0 480 118" role="img" aria-label="A queue of eight people '
         'standing one behind the other, numbered 1 at the front to 8 at the back">'
         '<rect x="0" y="0" width="480" height="118" rx="10" fill="#faf6ee" stroke="#e3dccd"/>']
    s.append('<g fill="#e6d7b4" stroke="#8a7a55" stroke-width="2">')
    s += ['<circle cx="%d" cy="38" r="12"/>' % x for x in xs]
    s.append('</g><g fill="#cddbe6" stroke="#5c7a94" stroke-width="2">')
    s += ['<rect x="%d" y="54" width="20" height="30" rx="9"/>' % (x - 10) for x in xs]
    s.append('</g><g font-size="13" text-anchor="middle" fill="#5a5348">')
    s += ['<text x="%d" y="104">%d</text>' % (x, i + 1) for i, x in enumerate(xs)]
    s.append('</g><text x="42" y="16" font-size="11" text-anchor="middle" '
             'fill="#8a7a55">front</text></svg>')
    return "".join(s)

def gold_svg():
    def plot(colour, rgba, y, lo, q1, med, q3, hi):
        g = ['<g stroke="%s" stroke-width="2" fill="none">' % colour,
             '<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (lo, y, q1, y),
             '<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (q3, y, hi, y),
             '<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (lo, y - 10, lo, y + 10),
             '<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (hi, y - 10, hi, y + 10),
             '<rect x="%d" y="%d" width="%d" height="28" fill="%s"/>' % (q1, y - 14, q3 - q1, rgba),
             '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="3"/>' % (med, y - 14, med, y + 14),
             '</g>']
        return "".join(g)
    s = ['<svg viewBox="0 0 560 232" role="img" aria-label="Two horizontal box plots of '
         'river width in metres. The upper plot, River Aln, has a box from 2.0 to 4.5 with a '
         'median line at 3.0 and whiskers from 1.0 to 5.5. The lower plot, River Coquet, has a '
         'box from 2.5 to 4.0 with a median line at 3.0 and whiskers from 1.5 to 5.0.">'
         '<rect x="0" y="0" width="560" height="232" rx="10" fill="#faf6ee" stroke="#e3dccd"/>'
         '<g font-size="13" fill="#5a5348"><text x="60" y="30">River Aln</text>'
         '<text x="60" y="108">River Coquet</text></g>']
    s.append(plot("#3b82f6", "rgba(59,130,246,0.22)", 60, 132, 204, 276, 384, 456))
    s.append(plot("#ef4444", "rgba(239,68,68,0.22)", 138, 168, 240, 276, 348, 420))
    s.append('<g stroke="#8a7a55" stroke-width="1">'
             '<line x1="60" y1="180" x2="492" y2="180" stroke-width="2"/>')
    for i in range(7):
        x = 60 + 72 * i
        s.append('<line x1="%d" y1="180" x2="%d" y2="188"/>' % (x, x))
        if i < 6:
            s.append('<line x1="%d" y1="180" x2="%d" y2="184"/>' % (x + 36, x + 36))
    s.append('</g><g font-size="12" text-anchor="middle" fill="#5a5348">')
    for i in range(7):
        s.append('<text x="%d" y="204">%d</text>' % (60 + 72 * i, i))
    s.append('<text x="276" y="224">River width (m)</text></g></svg>')
    return "".join(s)

op = d["guided"]["opener"]
old_len = len(op["display"])
op["display"] = ('<p>Eight people are queuing at a bus stop. You want to split the queue into '
                 'four equal groups, front to back.</p>' + opener_svg())
log.append(("guided.opener.display", "svg %d bytes" % (old_len - 132),
            "svg %d bytes" % (len(op["display"]) - 132)))

gt = d["guided"]["teach"]["gold"]
old_len = len(gt["display"])
gt["display"] = ('<p>Two box plots show river width at two survey sites.</p>' + gold_svg() +
                 '<p>How much wider is the middle half of the River Aln widths than the middle '
                 'half of the River Coquet widths?</p>')
log.append(("guided.teach.gold.display", "%d chars" % old_len, "%d chars" % len(gt["display"])))

# ---------------------------------------------------------------- NIT: final CHECK steps
pb = d["problem_bank"]

def retrim(tier, idx, step_idx, new_pre):
    st = pb[tier][idx]["guided_steps"][step_idx]
    log.append(("%s[%d].guided_steps[%d].pre" % (tier, idx, step_idx), st["pre"], new_pre))
    st["pre"] = new_pre

def add_check(tier, idx, pre, answer, hint, done):
    p = pb[tier][idx]
    p["guided_steps"].append({"pre": pre, "answer": answer, "hint": hint, "done": done})
    log.append(("%s[%d].guided_steps" % (tier, idx), "no separate final check box",
                "check box appended (answer %s)" % answer))

retrim("bronze", 7, 5, "Subtract Q1 from Q3 to get the IQR.")
add_check("bronze", 7,
          "Check: how many of the seven wind speeds sit between Q1 and Q3?", 3,
          "Count the speeds above 12 and below 25.",
          "Three days sit inside the middle half with two cut off at each end, and the IQR of 13 "
          "is comfortably below the full range of 23.")

retrim("silver", 6, 5, "Subtract Q1 from Q3 to get the IQR.")
add_check("silver", 6,
          "Check: subtract the IQR from the full range of 14 to see how much spread the extreme "
          "sites were adding.", 6,
          "Range minus IQR.",
          "The best and worst sites account for 6 points of spread on their own, which is why the "
          "middle half is so much tighter than the range.")

add_check("gold", 0,
          "Check: add your difference back onto the River Dart interquartile range. Does it "
          "return the River Exe figure, in metres?", 2.1,
          "Dart IQR plus the difference.",
          "It lands back on the width of the Exe box, and the Exe box is the wider of the two on "
          "the chart, so a small positive difference is what the picture shows.")

retrim("gold", 2, 5, "Subtract Q1 from Q3 to get the IQR.")
add_check("gold", 2,
          "Check: how many of the thirteen pH values sit between Q1 and Q3?", 7,
          "Count the values above 4.95 and below 6.65.",
          "Seven values sit inside with three cut off at each end, and the IQR of 1.7 is well "
          "below the full range of 3.2.")

retrim("gold", 3, 7, "Add that to Q3 to get the boundary.")
add_check("gold", 3,
          "Check: how far below the boundary does the largest figure of 15.8 sit?", 8.45,
          "Boundary minus 15.8.",
          "The largest park figure sits 8.45 below the boundary, so it is nowhere near being an "
          "outlier.")

add_check("gold", 4,
          "Check: divide the IQR of 79 by 4 to see roughly what a quarter of it is, in thousands.",
          19.75, "IQR divided by 4.",
          "A quarter of the IQR is 19.75 and the median of 25 is a little bigger than that, so an "
          "answer a little above 25 per cent is the right size.")

# ---------------------------------------------------------------- NIT: gold[3] display
g3 = pb["gold"][3]
old = g3["display"]
g3["display"] = ("Tourism visitor numbers (millions) for 9 UK national parks: 1.2, 2.4, 3.6, "
                 "4.8, 7.5, 9.1, 10.3, 12.7, 15.8. An outlier is defined as more than "
                 "1.5 × IQR above Q3. Work out the outlier boundary, Q3 + 1.5 × IQR.")
log.append(("gold[3].display", old, g3["display"]))
for st in g3["guided_steps"]:
    if "in thousands" in str(st.get("pre") or ""):
        st["pre"] = st["pre"].replace("in thousands", "in millions")

# ---------------------------------------------------------------- NIT: directional nudges
m = pb["silver"][2]["misconceptions"][0]
old = m["message"]
m["message"] = ("Site A was picked before Site B's spread was worked out. A pair of quartiles is "
                "all an IQR needs, so both sites can be compared.")
log.append(("silver[2].misconceptions[0].message", old, m["message"]))

m = pb["silver"][5]["misconceptions"][0]
old = m["message"]
m["message"] = ("That is the region with the wider middle half. A wider IQR means the monthly "
                "totals are more spread out, which is the opposite of consistent.")
log.append(("silver[5].misconceptions[0].message", old, m["message"]))

json.dump(d, io.open(FN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for a, b, c in log:
    print("*", a)
    print("   -", (b[:110] + "...") if len(str(b)) > 110 else b)
    print("   +", (c[:110] + "...") if len(str(c)) > 110 else c)
print("edits:", len(log))
