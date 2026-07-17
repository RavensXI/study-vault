# -*- coding: utf-8 -*-
"""SVG figure generators for probability-statistics-L01 (maths-ocr).
Theme-safe: text + outline strokes use currentColor; region fills soft + opacity.
Every number is passed in from the problem, so figures match the maths."""

def _frac(n, d):
    return "%d/%d" % (n, d)

def tree2(total, a_lab, a_ct, b_lab, b_ct, wor, highlight, aria):
    """Two-stage tree. wor=without replacement. highlight=set of leaf codes
    like {'AA'} or {'AB','BA'} (A=a_lab, B=b_lab). Returns SVG string."""
    # translate real-letter highlight codes (e.g. 'RR','RB') into positional AA/AB
    trans = {a_lab: 'A', b_lab: 'B'}
    highlight = {trans[c[0]] + trans[c[1]] for c in highlight}
    t2 = total - 1 if wor else total
    # stage-1 fractions
    s1a = _frac(a_ct, total); s1b = _frac(b_ct, total)
    # stage-2 fractions from A
    aa = _frac(a_ct - 1 if wor else a_ct, t2); ab = _frac(b_ct, t2)
    # from B
    ba = _frac(a_ct, t2); bb = _frac(b_ct - 1 if wor else b_ct, t2)
    root = (16, 100)
    A1 = (118, 54); B1 = (118, 146)
    AA = (250, 30); AB = (250, 78); BA = (250, 122); BB = (250, 170)
    leaves = {'AA': (AA, a_lab + a_lab, aa, s1a),
              'AB': (AB, a_lab + b_lab, ab, s1a),
              'BA': (BA, b_lab + a_lab, ba, s1b),
              'BB': (BB, b_lab + b_lab, bb, s1b)}
    parts = []
    parts.append('<svg viewBox="0 0 280 200" role="img" aria-label="%s" '
                 'style="max-width:280px" font-family="Inter,sans-serif">' % aria)
    # highlight rects behind chosen leaves
    for code in highlight:
        (lx, ly), _, _, _ = leaves[code]
        parts.append('<rect x="%d" y="%d" width="26" height="18" rx="4" '
                     'fill="#34d399" fill-opacity="0.32"/>' % (lx - 2, ly - 13))
    # stage-1 branches
    def line(x1, y1, x2, y2, hot):
        w = '2.4' if hot else '1'
        return ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" '
                'stroke-width="%s"/>' % (x1, y1, x2, y2, w))
    hotA = any(c[0] == 'A' for c in highlight)
    hotB = any(c[0] == 'B' for c in highlight)
    parts.append(line(root[0]+8, root[1], A1[0]-4, A1[1], hotA))
    parts.append(line(root[0]+8, root[1], B1[0]-4, B1[1], hotB))
    # stage-2 branches
    parts.append(line(A1[0]+6, A1[1], AA[0]-4, AA[1], 'AA' in highlight))
    parts.append(line(A1[0]+6, A1[1], AB[0]-4, AB[1], 'AB' in highlight))
    parts.append(line(B1[0]+6, B1[1], BA[0]-4, BA[1], 'BA' in highlight))
    parts.append(line(B1[0]+6, B1[1], BB[0]-4, BB[1], 'BB' in highlight))
    # branch fraction labels
    def flab(x, y, s):
        return ('<text x="%d" y="%d" font-size="10" fill="currentColor" '
                'text-anchor="middle">%s</text>' % (x, y, s))
    parts.append(flab(62, 68, s1a))
    parts.append(flab(62, 132, s1b))
    parts.append(flab(190, 36, aa))
    parts.append(flab(190, 76, ab))
    parts.append(flab(190, 124, ba))
    parts.append(flab(190, 164, bb))
    # node dots
    for (x, y) in (root, A1, B1):
        parts.append('<circle cx="%d" cy="%d" r="3" fill="currentColor"/>' % (x, y))
    # leaf labels
    for code, ((lx, ly), name, _, _) in leaves.items():
        parts.append('<text x="%d" y="%d" font-size="11" fill="currentColor" '
                     'font-weight="600">%s</text>' % (lx, ly, name))
    parts.append('</svg>')
    return ''.join(parts)

def tree3_redspine(total, red, blue, aria):
    """Three-stage 'all red' spine tree. red draws along the top spine with
    fractions red/total, (red-1)/(total-1), (red-2)/(total-2); blue branch-offs
    shown at each node. Highlights the RRR leaf."""
    f1 = _frac(red, total)
    f2 = _frac(red - 1, total - 1)
    f3 = _frac(red - 2, total - 2)
    b1 = _frac(blue, total)
    b2 = _frac(blue, total - 1)
    b3 = _frac(blue, total - 2)
    nodes = [(16, 60), (98, 60), (180, 60), (262, 60)]
    parts = ['<svg viewBox="0 0 300 130" role="img" aria-label="%s" '
             'style="max-width:280px" font-family="Inter,sans-serif">' % aria]
    parts.append('<rect x="256" y="48" width="34" height="18" rx="4" '
                 'fill="#34d399" fill-opacity="0.32"/>')
    # spine (red-red-red), hot
    for i in range(3):
        x1, y1 = nodes[i]; x2, y2 = nodes[i+1]
        parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" '
                     'stroke-width="2.4"/>' % (x1+6, y1, x2-6, y2))
    # blue branch-offs going down
    blue_targets = [(98, 112), (180, 112), (262, 112)]
    blue_fracs = [b1, b2, b3]
    for i in range(3):
        x1, y1 = nodes[i]; x2, y2 = blue_targets[i]
        parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" '
                     'stroke-width="1"/>' % (x1+4, y1+3, x2-2, y2-8))
        parts.append('<text x="%d" y="%d" font-size="10" fill="currentColor" '
                     'text-anchor="middle">%s</text>' % ((x1+x2)//2 - 6, (y1+y2)//2 + 4, blue_fracs[i]))
    # red spine fraction labels
    spine_fracs = [f1, f2, f3]
    for i in range(3):
        x1, y1 = nodes[i]; x2, y2 = nodes[i+1]
        parts.append('<text x="%d" y="%d" font-size="10" fill="currentColor" '
                     'text-anchor="middle">%s</text>' % ((x1+x2)//2, y1-6, spine_fracs[i]))
    # node dots + red labels
    for i, (x, y) in enumerate(nodes):
        parts.append('<circle cx="%d" cy="%d" r="3" fill="currentColor"/>' % (x, y))
        if 0 < i < 3:
            parts.append('<text x="%d" y="%d" font-size="11" fill="currentColor" '
                         'font-weight="600">R</text>' % (x-3, y+4))
    for i, (x, y) in enumerate(blue_targets):
        parts.append('<text x="%d" y="%d" font-size="11" fill="currentColor">B</text>' % (x-3, y+4))
    parts.append('<text x="272" y="63" font-size="11" fill="currentColor" font-weight="600">R</text>')
    parts.append('</svg>')
    return ''.join(parts)

def dice_grid(aria):
    """6x6 sample space of two dice; highlights the six cells where d1+d2=7."""
    cell = 26; ox = 34; oy = 30
    parts = ['<svg viewBox="0 0 224 224" role="img" aria-label="%s" '
             'style="max-width:280px" font-family="Inter,sans-serif">' % aria]
    # highlight r+c=7 cells
    for d1 in range(1, 7):
        for d2 in range(1, 7):
            if d1 + d2 == 7:
                x = ox + (d2 - 1) * cell; y = oy + (d1 - 1) * cell
                parts.append('<rect x="%d" y="%d" width="%d" height="%d" '
                             'fill="#34d399" fill-opacity="0.32"/>' % (x, y, cell, cell))
    # grid lines
    for i in range(7):
        parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" '
                     'stroke-width="0.8"/>' % (ox + i*cell, oy, ox + i*cell, oy + 6*cell))
        parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" '
                     'stroke-width="0.8"/>' % (ox, oy + i*cell, ox + 6*cell, oy + i*cell))
    # axis labels
    for d in range(1, 7):
        parts.append('<text x="%d" y="%d" font-size="10" fill="currentColor" '
                     'text-anchor="middle">%d</text>' % (ox + (d-1)*cell + cell//2, oy - 8, d))
        parts.append('<text x="%d" y="%d" font-size="10" fill="currentColor" '
                     'text-anchor="middle">%d</text>' % (ox - 12, oy + (d-1)*cell + cell//2 + 3, d))
    parts.append('<text x="%d" y="14" font-size="10" fill="currentColor" '
                 'text-anchor="middle">Die 2</text>' % (ox + 3*cell))
    parts.append('<text x="10" y="%d" font-size="10" fill="currentColor" '
                 'text-anchor="middle" transform="rotate(-90 10 %d)">Die 1</text>'
                 % (oy + 3*cell, oy + 3*cell))
    parts.append('</svg>')
    return ''.join(parts)

def bag(reds, blues, aria):
    """A drawstring bag holding `reds` red and `blues` blue balls."""
    parts = ['<svg viewBox="0 0 200 150" role="img" aria-label="%s" '
             'style="max-width:220px" font-family="Inter,sans-serif">' % aria]
    # bag body
    parts.append('<path d="M55 55 Q40 60 45 110 Q48 138 100 138 Q152 138 155 110 '
                 'Q160 60 145 55 Z" fill="#a78bfa" fill-opacity="0.18" '
                 'stroke="currentColor" stroke-width="1.5"/>')
    # neck / tie
    parts.append('<path d="M62 55 Q100 42 138 55" fill="none" stroke="currentColor" '
                 'stroke-width="1.5"/>')
    parts.append('<line x1="62" y1="55" x2="58" y2="40" stroke="currentColor" stroke-width="1.5"/>')
    parts.append('<line x1="138" y1="55" x2="142" y2="40" stroke="currentColor" stroke-width="1.5"/>')
    # balls
    positions = [(80, 88), (112, 82), (95, 112), (128, 108), (70, 112), (120, 128)]
    total = reds + blues
    for i in range(total):
        cx, cy = positions[i % len(positions)]
        col = '#f87171' if i < reds else '#60a5fa'
        parts.append('<circle cx="%d" cy="%d" r="11" fill="%s" fill-opacity="0.55" '
                     'stroke="currentColor" stroke-width="1"/>' % (cx, cy, col))
    parts.append('</svg>')
    return ''.join(parts)

if __name__ == "__main__":
    import io, sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    for name, s in [
        ("bag", bag(1, 3, "A bag with 1 red and 3 blue balls")),
        ("s2", tree2(8, 'R', 5, 'B', 3, False, {'RR'}, "Tree with replacement")),
        ("s3", tree2(8, 'R', 5, 'B', 3, True, {'RR'}, "Tree without replacement")),
        ("s7", tree2(10, 'R', 6, 'B', 4, True, {'RB','BR'}, "Tree one of each")),
        ("g5", tree2(12, 'R', 7, 'B', 5, True, {'BB'}, "Tree both blue")),
        ("g1", tree3_redspine(12, 8, 4, "Three stage tree all red")),
        ("grid", dice_grid("Sample space grid for two dice totalling 7")),
        ("ts", tree2(10, 'R', 4, 'B', 6, True, {'RR'}, "Teach tree")),
        ("tg", tree2(9, 'R', 5, 'B', 4, True, {'RB','BR'}, "Teach gold tree")),
    ]:
        print(name, len(s), "chars")
