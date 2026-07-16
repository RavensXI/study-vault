# -*- coding: utf-8 -*-
"""Generate exam-realism figures (SVG Venn / tree) for probability-statistics-L02
from each problem's own numbers, and prepend them to the relevant displays."""
import json, io

SRC = "_L02_live.json"
OUT = "lesson_probability-statistics-L02_diagrams.json"

BLUE = "#60a5fa"; AMBER = "#f59e0b"; GREEN = "#34d399"

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def venn2(aria, aLabel, bLabel, mid="", aOnly="", bOnly="", neither="",
          universe="", caption=""):
    """Two-circle Venn. Region texts are strings ('' = blank)."""
    p = []
    p.append('<svg viewBox="0 0 250 172" role="img" aria-label="%s" '
             'style="display:block;margin:0 auto 0.4rem;max-width:270px;width:100%%">' % esc(aria))
    p.append('<rect x="5" y="5" width="240" height="162" rx="6" fill="none" '
             'stroke="currentColor" stroke-width="1" opacity="0.6"/>')
    p.append('<circle cx="95" cy="90" r="56" fill="%s" fill-opacity="0.3" '
             'stroke="currentColor" stroke-width="1.2"/>' % BLUE)
    p.append('<circle cx="155" cy="90" r="56" fill="%s" fill-opacity="0.3" '
             'stroke="currentColor" stroke-width="1.2"/>' % AMBER)
    p.append('<text x="52" y="50" text-anchor="middle" font-family="Inter,sans-serif" '
             'font-size="11" font-weight="600" fill="currentColor">%s</text>' % esc(aLabel))
    p.append('<text x="198" y="50" text-anchor="middle" font-family="Inter,sans-serif" '
             'font-size="11" font-weight="600" fill="currentColor">%s</text>' % esc(bLabel))
    def reg(x, t):
        return ('<text x="%d" y="95" text-anchor="middle" font-family="Inter,sans-serif" '
                'font-size="12" fill="currentColor">%s</text>' % (x, esc(t))) if t != "" else ""
    p.append(reg(60, aOnly)); p.append(reg(125, mid)); p.append(reg(190, bOnly))
    if universe != "":
        p.append('<text x="12" y="20" font-family="Inter,sans-serif" font-size="10" '
                 'fill="currentColor" opacity="0.85">n = %s</text>' % esc(universe))
    if neither != "":
        p.append('<text x="236" y="160" text-anchor="end" font-family="Inter,sans-serif" '
                 'font-size="11" fill="currentColor">%s</text>' % esc(neither))
    if caption != "":
        p.append('<text x="125" y="162" text-anchor="middle" font-family="Inter,sans-serif" '
                 'font-size="10" fill="currentColor" opacity="0.85">%s</text>' % esc(caption))
    p.append('</svg>')
    return "".join(p)

def venn_complement(aria, aLabel, inside, outside, universe=""):
    p = []
    p.append('<svg viewBox="0 0 250 150" role="img" aria-label="%s" '
             'style="display:block;margin:0 auto 0.4rem;max-width:250px;width:100%%">' % esc(aria))
    p.append('<rect x="5" y="5" width="240" height="140" rx="6" fill="%s" fill-opacity="0.18" '
             'stroke="currentColor" stroke-width="1" opacity="0.9"/>' % AMBER)
    p.append('<circle cx="125" cy="75" r="52" fill="%s" fill-opacity="0.35" '
             'stroke="currentColor" stroke-width="1.2"/>' % BLUE)
    p.append('<text x="125" y="79" text-anchor="middle" font-family="Inter,sans-serif" '
             'font-size="13" fill="currentColor">%s</text>' % esc(inside))
    p.append('<text x="125" y="42" text-anchor="middle" font-family="Inter,sans-serif" '
             'font-size="11" font-weight="600" fill="currentColor">%s</text>' % esc(aLabel))
    p.append('<text x="20" y="26" font-family="Inter,sans-serif" font-size="11" '
             'fill="currentColor">%s</text>' % esc(outside))
    if universe != "":
        p.append('<text x="232" y="138" text-anchor="end" font-family="Inter,sans-serif" '
                 'font-size="10" fill="currentColor" opacity="0.85">total = %s</text>' % esc(universe))
    p.append('</svg>')
    return "".join(p)

def venn3(aria, aOnly, bOnly, cOnly, ab, ac, bc, centre, none, universe):
    p = []
    p.append('<svg viewBox="0 0 250 205" role="img" aria-label="%s" '
             'style="display:block;margin:0 auto 0.4rem;max-width:270px;width:100%%">' % esc(aria))
    p.append('<rect x="5" y="5" width="240" height="195" rx="6" fill="none" '
             'stroke="currentColor" stroke-width="1" opacity="0.6"/>')
    p.append('<circle cx="90" cy="80" r="56" fill="%s" fill-opacity="0.28" '
             'stroke="currentColor" stroke-width="1.2"/>' % BLUE)
    p.append('<circle cx="160" cy="80" r="56" fill="%s" fill-opacity="0.28" '
             'stroke="currentColor" stroke-width="1.2"/>' % AMBER)
    p.append('<circle cx="125" cy="128" r="56" fill="%s" fill-opacity="0.28" '
             'stroke="currentColor" stroke-width="1.2"/>' % GREEN)
    def lab(x, y, t, fs=11, w="600"):
        return ('<text x="%d" y="%d" text-anchor="middle" font-family="Inter,sans-serif" '
                'font-size="%d" font-weight="%s" fill="currentColor">%s</text>'
                % (x, y, fs, w, esc(t)))
    p.append(lab(50, 40, "A")); p.append(lab(200, 40, "B")); p.append(lab(125, 192, "C"))
    def reg(x, y, t):
        return lab(x, y, t, 12, "400") if t != "" else ""
    p.append(reg(62, 68, aOnly)); p.append(reg(188, 68, bOnly)); p.append(reg(125, 168, cOnly))
    p.append(reg(125, 52, ab)); p.append(reg(92, 120, ac)); p.append(reg(158, 120, bc))
    p.append(reg(125, 96, centre))
    p.append('<text x="20" y="24" font-family="Inter,sans-serif" font-size="10" '
             'fill="currentColor" opacity="0.85">n = %s</text>' % esc(universe))
    p.append('<text x="236" y="193" text-anchor="end" font-family="Inter,sans-serif" '
             'font-size="11" fill="currentColor">none = %s</text>' % esc(none))
    p.append('</svg>')
    return "".join(p)

def tree(aria, l1, l2):
    """l1 = [(name,prob),(name,prob)] ; l2 = [[(n,p),(n,p)],[(n,p),(n,p)]]."""
    p = []
    p.append('<svg viewBox="0 0 270 180" role="img" aria-label="%s" '
             'style="display:block;margin:0 auto 0.4rem;max-width:290px;width:100%%">' % esc(aria))
    sx, sy = 18, 90
    n1 = [(120, 46), (120, 134)]
    n2 = [[(224, 24), (224, 68)], [(224, 112), (224, 156)]]
    def line(x1, y1, x2, y2):
        return ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" '
                'stroke-width="1.2" opacity="0.75"/>' % (x1, y1, x2, y2))
    def txt(x, y, t, anchor="middle", fs=10, w="400"):
        return ('<text x="%d" y="%d" text-anchor="%s" font-family="Inter,sans-serif" '
                'font-size="%d" font-weight="%s" fill="currentColor">%s</text>'
                % (x, y, anchor, fs, w, esc(t)))
    for k in (0, 1):
        p.append(line(sx, sy, n1[k][0] - 12, n1[k][1]))
        mx, my = (sx + n1[k][0] - 12) // 2, (sy + n1[k][1]) // 2 - 3
        p.append(txt(mx, my, l1[k][1], fs=10, w="600"))
        p.append(txt(n1[k][0], n1[k][1] + 4, l1[k][0], fs=12, w="600"))
        for j in (0, 1):
            a = (n1[k][0] + 8, n1[k][1]); b = (n2[k][j][0] - 14, n2[k][j][1])
            p.append(line(a[0], a[1], b[0], b[1]))
            mx2, my2 = (a[0] + b[0]) // 2, (a[1] + b[1]) // 2 - 2
            p.append(txt(mx2, my2, l2[k][j][1], fs=10, w="600"))
            p.append(txt(n2[k][j][0], n2[k][j][1] + 4, l2[k][j][0], anchor="start", fs=11))
    p.append('</svg>')
    return "".join(p)

# ---- build ----
pd = json.load(io.open(SRC, encoding="utf-8"))
added = []

def prepend(display, svg):
    return svg + display

pb = pd["problem_bank"]

# OPENER: 10 friends, pizza 7, burgers 5, both 3 ; box1 finds pizza-only (do not spoil)
op = pd["guided"]["opener"]
op_svg = venn2("Venn diagram: 10 friends, 7 like pizza, 5 like burgers, 3 like both",
               "Pizza 7", "Burgers 5", mid="3", aOnly="?", bOnly="", neither="", universe="10")
op["display"] = op_svg + op["display"]
added.append({"tier": "opener", "index": 0, "kind": "svg",
              "what": "two-circle Venn, overlap 3, pizza total 7, burger total 5, n=10, pizza-only marked ?"})

# BRONZE
b = pb["bronze"]
# b0: 40; tea 25, coffee 18, both 8 -> neither ?
b[0]["display"] = prepend(b[0]["display"], venn2(
    "Venn diagram: 40 people, 25 like tea, 18 like coffee, 8 like both, neither unknown",
    "Tea 25", "Coffee 18", mid="8", neither="? outside", universe="40"))
added.append({"tier": "bronze", "index": 0, "kind": "svg", "what": "Venn overlap 8, tea 25, coffee 18, n=40, neither marked ?"})
# b1: same, P(T only) -> T-only ?
b[1]["display"] = prepend(b[1]["display"], venn2(
    "Venn diagram: 40 people, 25 like tea, 18 like coffee, 8 like both, tea-only unknown",
    "Tea 25", "Coffee 18", mid="8", aOnly="?", universe="40"))
added.append({"tier": "bronze", "index": 1, "kind": "svg", "what": "Venn overlap 8, totals 25/18, n=40, tea-only marked ?"})
# b2 & b3: element sets A={1,2,3,4,5} B={3,4,5,6,7}
elem_svg = venn2("Venn diagram of sets A equals 1 2 3 4 5 and B equals 3 4 5 6 7",
                 "A", "B", mid="3, 4, 5", aOnly="1, 2", bOnly="6, 7")
b[2]["display"] = prepend(b[2]["display"], elem_svg)
added.append({"tier": "bronze", "index": 2, "kind": "svg", "what": "element Venn: A-only {1,2}, overlap {3,4,5}, B-only {6,7}"})
b[3]["display"] = prepend(b[3]["display"], elem_svg)
added.append({"tier": "bronze", "index": 3, "kind": "svg", "what": "element Venn (same sets) for A union B count"})
# b4: P(A)=0.5,P(B)=0.4, overlap 0.2 -> union
b[4]["display"] = prepend(b[4]["display"], venn2(
    "Venn diagram: P(A)=0.5, P(B)=0.4, overlap 0.2, find the union",
    "A 0.5", "B 0.4", mid="0.2", caption="P(A ∪ B) = ?"))
added.append({"tier": "bronze", "index": 4, "kind": "svg", "what": "probability Venn overlap 0.2, totals 0.5/0.4, union asked"})
# b5: 60; maths 35 science 28 both 15 -> maths only ?
b[5]["display"] = prepend(b[5]["display"], venn2(
    "Venn diagram: 60 students, 35 maths, 28 science, 15 both, maths-only unknown",
    "Maths 35", "Science 28", mid="15", aOnly="?", universe="60"))
added.append({"tier": "bronze", "index": 5, "kind": "svg", "what": "Venn overlap 15, maths 35, science 28, n=60, maths-only ?"})
# b6: same -> neither ?
b[6]["display"] = prepend(b[6]["display"], venn2(
    "Venn diagram: 60 students, 35 maths, 28 science, 15 both, neither unknown",
    "Maths 35", "Science 28", mid="15", neither="? outside", universe="60"))
added.append({"tier": "bronze", "index": 6, "kind": "svg", "what": "Venn overlap 15, totals 35/28, n=60, neither ?"})
# b7: complement P(A')=0.35 -> P(A) ?
b[7]["display"] = prepend(b[7]["display"], venn_complement(
    "Rectangle for the whole sample space with event A inside; outside region is 0.35",
    "A", inside="?", outside="A' = 0.35", universe="1"))
added.append({"tier": "bronze", "index": 7, "kind": "svg", "what": "complement diagram: outside A = 0.35, inside A marked ?"})

# SILVER
s = pb["silver"]
# s0: P(A)=0.7,P(B)=0.5, overlap 0.35 -> P(A|B)
s[0]["display"] = prepend(s[0]["display"], venn2(
    "Venn diagram: P(A)=0.7, P(B)=0.5, overlap 0.35",
    "A 0.7", "B 0.5", mid="0.35", caption="P(A|B) = ?"))
added.append({"tier": "silver", "index": 0, "kind": "svg", "what": "probability Venn overlap 0.35, totals 0.7/0.5"})
# s1: 80; French 50 German 30 both 15 -> P(G|F)
s[1]["display"] = prepend(s[1]["display"], venn2(
    "Venn diagram: 80 people, 50 speak French, 30 speak German, 15 both",
    "French 50", "German 30", mid="15", universe="80", caption="P(G|F) = ?"))
added.append({"tier": "silver", "index": 1, "kind": "svg", "what": "Venn overlap 15, French 50, German 30, n=80"})
# s2: independent P(A)=0.6,P(B)=0.4 -> overlap ?
s[2]["display"] = prepend(s[2]["display"], venn2(
    "Venn diagram: P(A)=0.6, P(B)=0.4, independent events, overlap unknown",
    "A 0.6", "B 0.4", mid="?", caption="A, B independent"))
added.append({"tier": "silver", "index": 2, "kind": "svg", "what": "Venn totals 0.6/0.4, independent, overlap marked ?"})
# s3: P(A)=0.5, overlap 0.15, union 0.75 -> P(B)
s[3]["display"] = prepend(s[3]["display"], venn2(
    "Venn diagram: P(A)=0.5, overlap 0.15, union 0.75, find P(B)",
    "A 0.5", "B = ?", mid="0.15", caption="P(A ∪ B) = 0.75"))
added.append({"tier": "silver", "index": 3, "kind": "svg", "what": "Venn overlap 0.15, A=0.5, union 0.75, B marked ?"})
# s4: 100; sport 60 music 45 both 20 -> P(music|sport)
s[4]["display"] = prepend(s[4]["display"], venn2(
    "Venn diagram: 100 students, 60 play sport, 45 play music, 20 both",
    "Sport 60", "Music 45", mid="20", universe="100", caption="P(music | sport) = ?"))
added.append({"tier": "silver", "index": 4, "kind": "svg", "what": "Venn overlap 20, sport 60, music 45, n=100"})
# s6: independence check P(A)=0.3,P(B)=0.4,overlap 0.12
s[6]["display"] = prepend(s[6]["display"], venn2(
    "Venn diagram: P(A)=0.3, P(B)=0.4, overlap 0.12",
    "A 0.3", "B 0.4", mid="0.12", caption="Independent?"))
added.append({"tier": "silver", "index": 6, "kind": "svg", "what": "Venn overlap 0.12, totals 0.3/0.4, independence check"})

# GOLD
g = pb["gold"]
# g0: P(A)=0.55,P(B)=0.4, neither 0.25 -> overlap ?
g[0]["display"] = prepend(g[0]["display"], venn2(
    "Venn diagram: P(A)=0.55, P(B)=0.4, neither region 0.25, overlap unknown",
    "A 0.55", "B 0.4", mid="?", neither="neither = 0.25"))
added.append({"tier": "gold", "index": 0, "kind": "svg", "what": "probability Venn totals 0.55/0.4, neither 0.25, overlap ?"})
# g1: three-set. totals A70 B55 C45; AB30 BC20 AC25 triple10; none?
# pure regions (verified): A-only25 B-only15 C-only10 AB-only20 AC-only15 BC-only10 centre10
g[1]["display"] = prepend(g[1]["display"], venn3(
    "Three-circle Venn: sets A, B, C with all overlaps filled, none region unknown",
    aOnly="25", bOnly="15", cOnly="10", ab="20", ac="15", bc="10", centre="10",
    none="?", universe="120"))
added.append({"tier": "gold", "index": 1, "kind": "svg", "what": "three-circle Venn, pure regions 25/15/10/20/15/10/10 (verified from totals), none marked ?, n=120"})
# g2: medical test tree
g[2]["display"] = prepend(g[2]["display"], tree(
    "Probability tree: disease 0.01 or none 0.99, each branching to positive or negative",
    [("Disease", "0.01"), ("No dis.", "0.99")],
    [[("Positive", "0.95"), ("Negative", "0.05")],
     [("Positive", "0.05"), ("Negative", "0.95")]]))
added.append({"tier": "gold", "index": 2, "kind": "svg", "what": "tree: D 0.01 / D' 0.99; +|D 0.95, +|D' 0.05 (negatives 0.05/0.95 follow)"})
# g3: A/B tree
g[3]["display"] = prepend(g[3]["display"], tree(
    "Probability tree: A 0.3 or not-A 0.7, each branching to B or not-B",
    [("A", "0.3"), ("A'", "0.7")],
    [[("B", "0.5"), ("B'", "0.5")],
     [("B", "0.2"), ("B'", "0.8")]]))
added.append({"tier": "gold", "index": 3, "kind": "svg", "what": "tree: A 0.3 / A' 0.7; B|A 0.5, B|A' 0.2 (complements follow)"})
# g4: mutually exclusive check; union 0.8, P(A)=0.5, P(B)=0.6 -> overlap ?
g[4]["display"] = prepend(g[4]["display"], venn2(
    "Venn diagram: P(A)=0.5, P(B)=0.6, union 0.8, overlap unknown",
    "A 0.5", "B 0.6", mid="?", caption="P(A ∪ B) = 0.8"))
added.append({"tier": "gold", "index": 4, "kind": "svg", "what": "Venn totals 0.5/0.6, union 0.8, overlap marked ? (mutually exclusive check)"})

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("figures added:", len(added))
print(json.dumps(added, ensure_ascii=False, indent=1))
